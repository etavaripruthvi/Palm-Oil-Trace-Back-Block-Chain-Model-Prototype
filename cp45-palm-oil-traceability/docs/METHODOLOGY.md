# Methodology

This note documents what the code computes. Every equation below is implemented in `src/palm_oil_traceability_model.py`
(cost-benefit engine, Monte Carlo) or in `scripts/compute_numbers.py` / `scripts/compute_extras.py` (SPOEI, parity, staged strategy).
Evidence status: inputs typed from Bloomberg screens are marked **[BBG]**; everything else is an **[ASSUMPTION]** chosen by the authors.

## 1. Research questions

| | Question | Where answered |
|---|---|---|
| RQ1 | How visible is the palm oil chain in Bloomberg SPLC for the three brand owners / traders, and what does that say about traceability? | workbook `Supply_Chain`; report Ch. 3 |
| RQ2 | What do fundamentals, ESG, news and prices say about each firm's exposure? | workbook `Fundamentals`, `ESG`, `News_Events`, `Price_Analytics`; report Ch. 3 |
| RQ3 | Can supply-chain, ESG, news and balance-sheet indicators be combined into a transparent risk index (SPOEI), and is the ranking stable? | workbook `Risk_Index`; report Ch. 4 |
| RQ4 | Does a permissioned ledger beat a central database on risk-adjusted economics, and when? | workbook `ROI_*`, `MC_Results`, `Sensitivity`; report Ch. 5-6 |

## 2. SPOEI - Supply-chain Palm Oil Exposure Index

Ten indicators, each rescaled to 0-100 and combined with explicit weights.

    S_i = 100 * clip( (x_i - floor_i) / (cap_i - floor_i), 0, 1 )          SPOEI = sum_i w_i * S_i

(`floor > cap` is allowed: interest cover is inverted, so *low* cover scores *high*.)

| # | Indicator | Floor -> cap | Base | Equal | E-S-heavy |
|---|---|---|---|---|---|
| 1 | BESG gap (10 - BESG score) [BBG] | 0 -> 10 | .15 | .10 | .15 |
| 2 | Social-pillar gap [BBG] | 0 -> 10 | .15 | .10 | .20 |
| 3 | Scope 3 intensity (kt CO2e per USD bn revenue) [BBG] | 0 -> 3000 | .15 | .10 | .20 |
| 4 | Supplier business-conduct flags (% of listed suppliers) [BBG SPLC] | 0 -> 0.4 | .10 | .10 | .10 |
| 5 | High-GHG suppliers (%) [BBG SPLC] | 0 -> 0.25 | .05 | .10 | .10 |
| 6 | ESG-laggard suppliers (%) [BBG SPLC] | 0 -> 0.10 | .05 | .10 | .05 |
| 7 | Sanctioned + distressed suppliers (%) [BBG SPLC] | 0 -> 0.05 | .10 | .10 | .05 |
| 8 | Adverse news severity, 12 months [BBG CN, hand-coded] | 0 -> 20 | .10 | .10 | .05 |
| 9 | Equity volatility, 90 days [BBG] | 10 -> 40 | .05 | .10 | 0 |
| 10 | Interest cover (inverse) [BBG FA] | 12 -> 2 | .10 | .10 | .10 |

Floors/caps and weights are judgement **[ASSUMPTION]**: they are stated up front rather than fitted, to avoid the circularity of
"validating" a model against weights the authors typed. A fourth variant, "Base, ex-news" (base weights with the news indicator dropped), is reported alongside the three weight sets.
**Base-weight results:** Wilmar 63.5, Unilever 53.0, Nestle 39.9.

Robustness (report Ch. 4): the rank order Wilmar > Unilever > Nestle holds under all four weightings, under all 10 leave-one-indicator-out
runs, and in 78% of 20,000 random Dirichlet(1,...,1) weight vectors. The weakest link is Unilever vs Wilmar (10.5-point gap).

## 3. Cost-benefit engine (RQ4)

Three options are compared for each firm: **SQ** status quo, **DB** central database (+ satellite checks + audits), **BC** permissioned
blockchain consortium. Years t = 1..7 (`horizon`); build capex at t = 0.

**Coverage and assurance.**

    cov_t = c0 + (cmax - c0) * min(1, t / ramp)          m_t = cov_t * eff

`c0` is today's traceable share (SQ keeps `cmax = c0`); `cmax`, `ramp` (years to reach it) and `eff` (assurance value of that coverage)
differ by option.

| Option | cmax | ramp (yrs) | eff |
|---|---|---|---|
| SQ | = c0 (0.30) | 1 | 0.60 |
| DB | 0.80 | 3 | 0.80 |
| BC | 0.90 | 4 | 0.90 |

**Three loss channels** (all in USD m; revenue and COGS grow at `g` = 2%; EUR/CHF converted at 1.15 / 1.25):

    Reg_t = p_reg  * fine * eu * Rev_t * (1 - m_t)                          regulatory / market-access event (EUDR)
    Sub_t = COGS_t * ps * P_t * eu * (1 - cov_t) * q * pi                   substitution: excluded volume re-sourced at a premium
    Rep_t = p_ctrv * rev_loss * a * Rev_t * (1 - m_t)                        reputational controversy on palm-linked revenue

`p_reg`, `p_ctrv` = annual event probabilities; `fine` = fine as share of EU turnover (2%; the EUDR cap is "at least 4%"); `eu` = EU-regulated
revenue share; `ps` = palm spend / COGS; `P_t` = CPO price index; `q` = share of non-traceable EU-bound volume that must be excluded; `pi` = price
premium on re-sourced volume; `a` = palm-linked revenue share; `rev_loss` = revenue lost in a controversy. Firm-level values are in `PROFILES`
(revenue and COGS are **[BBG]** FY2025; the rest **[ASSUMPTION]**).

**Programme cost.** `PV_prog = capex + sum_t opex*(1+g)^t / (1+r)^t`, with (capex, opex) USD m: Unilever DB 8/3, BC 14/4.5; Nestle DB 7/2.5, BC 12/4;
Wilmar DB 25/10, BC 40/14 **[ASSUMPTION]**. Discount rate r = 8%.

**Outputs.**

    PV_total(opt) = sum_t d_t * (Reg_t + Sub_t + Rep_t) + PV_prog          d_t = (1 + r)^-t
    NPV(opt)      = PV_total(SQ) - PV_total(opt)                          (positive = the option beats doing nothing)
    BCR(opt)      = PV(avoided losses) / PV_prog
    break-even k  = max(0, 1 - NPV / PV(regulatory loss avoided))          (share of the modelled regulatory-loss reduction that must be real for NPV = 0)

**Deterministic scenarios** multiply the base inputs: Base (1, 1, 1, 1), Adverse (p_reg x2, p_ctrv x1.5, pi x1.5), Severe (p_reg x4, p_ctrv x2.5,
pi x2.5, CPO x1.3).

| NPV, USD m | Base | Adverse | Severe |
|---|---|---|---|
| Unilever - DB / BC | 20 / 16 | 52 / 56 | 124 / 143 |
| Nestle - DB / BC | 44 / 47 | 96 / 111 | 206 / 247 |
| Wilmar - DB / BC | 90 / 86 | 182 / 197 | 414 / 471 |

## 4. Monte Carlo

20,000 draws, `numpy.random.default_rng(42)`. **Common random numbers**: SQ, DB and BC are evaluated in the *same* simulated world, so differences
between options are not noise. Regimes: Base, Adverse, Severe, or **Mixed** (25% benign / 50% base / 25% severe; benign = p_reg x0.4, p_ctrv x0.6).

| Parameter | Distribution |
|---|---|
| p_reg, p_ctrv | base x regime multiplier x LogNormal(0, 0.5) and LogNormal(0, 0.4) |
| fine | Uniform(0.5%, 4%) |
| q | Triangular(0.10, 0.30, 0.50) |
| pi | base x regime multiplier x LogNormal(0, 0.3) |
| r | Triangular(6%, 8%, 11%) |
| c0 | Triangular(0.15, 0.30, 0.45) |
| CPO price index | GBM, zero drift, sigma = annualised volatility of KOZ6 Comdty from the 8-week sample (17.05%) |
| SQ eff | Triangular(0.45, 0.60, 0.70) |
| DB cmax / ramp / eff | Triangular(0.60, 0.80, 0.92) / (2, 3, 5) / (0.55, 0.80, 0.92) |
| BC cmax / ramp / eff | Triangular(0.65, 0.90, 0.97) / (3, 4, 7) / (0.65, 0.90, 0.98) |
| Cost overrun (multiplies capex and opex) | LogNormal(0, 0.30) for DB, LogNormal(0, 0.35) for BC |

**Headline (Mixed regimes):** P(BC beats DB) = 35% Unilever, 42% Nestle, 38% Wilmar. BC adds tail risk (5th-percentile NPV is more negative than DB's)
because it is dearer and slower to coordinate; its upside appears only in severe-enforcement worlds.

## 5. Parity points and staged strategy (`scripts/compute_extras.py`)

**Parity** (root-finding, Brent): the multiple of BC capex *and* opex at which NPV(BC) = NPV(DB) (`cost_mult`), and the multiple of `p_reg` (applied to
both options) at which they tie (`preg_mult`), base scenario.

| | cost_mult | preg_mult | Reading |
|---|---|---|---|
| Unilever | 0.893 | 1.82 | ledger cost must fall 10.7%, or regulatory risk be 1.8x the base case |
| Nestle | 1.066 | 0.77 | BC already ahead at base; it can cost 6.6% more and still tie |
| Wilmar | 0.970 | 2.09 | ledger cost must fall 3.0%, or regulatory risk be 2.1x the base case |

**"Database first, ledger-ready" staged strategy**: build the database, and switch to the ledger only in worlds where enforcement turns out severe.
*Upper bound* = the switch is free (NPV = BC in switch worlds, DB otherwise). *Conservative* = in switch worlds, subtract the deterministic
base-case PV of the database programme already spent. The truth lies between the two; the conservative figure still dominates BC outright on 5th-percentile
NPV and P(NPV > 0), at a mean NPV close to DB / BC.

## 6. Classifier protocol (specified, **not estimated**)

The Terminal screens give 21 firm-years and no labelled event history, so no classifier is fitted and no performance figure is reported as evidence.
The protocol (report Ch. 4.2) is fixed in advance: nine features (`data/panel/README.md`), target = any RSPO complaint / sanction, new ESG controversy flag or
severe deforestation-related headline in the next 12 months; expanding-window walk-forward test blocks (2022, 2023, 2024-01 to 2025-09) with a 13-month purge;
fixed hyper-parameters; ROC-AUC, PR-AUC, precision/recall at top-10% alerts, Brier score; DeLong tests against benchmark models; success only if AUC beats the best
benchmark by >= 0.05 at p < 0.05 and PR-AUC is also higher. Notebook Part 5 exercises this code on a **synthetic** panel
(every output tagged `SYNTHETIC - code test, NOT EVIDENCE`).

## 7. Limitations

* Bloomberg inputs were typed by hand from screenshots on one date (15-Oct-2026); 10 numbers per sheet should be spot-checked against the Terminal.
* Event probabilities, fine rate, programme costs, effectiveness (`eff`, `cmax`, `ramp`) and discount rate are assumptions. The ranking BC vs DB is decided by the
  effectiveness gap and the cost ratio - that is why parity points and the tornado are reported alongside NPVs.
* The CPO volatility comes from an 8-week sample of one Dec-26 contract (KOZ6); a longer continuous series (KO1) should replace it.
* The palm chain is largely invisible in SPLC (plantations are only 0.4% of Wilmar's visible cost base), so supplier-level indicators describe the *visible* chain only.
* Unilever FY2024-25 figures are restated for the ice-cream demerger; Scope 3 series have breaks; FX is an assumption.
* The 7-year horizon, constant probabilities and independent loss channels are simplifications.
