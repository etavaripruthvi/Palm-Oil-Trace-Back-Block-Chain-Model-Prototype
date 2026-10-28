#!/usr/bin/env python3
"""
Palm Oil Traceability Capstone  --  CP-45 (Unilever / Nestle / Wilmar)
=====================================================================
Reproducible model: market analytics + cost-benefit (NPV) + Monte Carlo + sensitivity.

WHAT CHANGED vs. the draft notebook
  * Synthetic "Supplier_01..50" data removed. Inputs are the Bloomberg screens you captured
    (15-Oct-2026) plus clearly-labelled ASSUMPTIONS (the ones Bloomberg cannot supply).
  * Three options compared, not two:  Status quo  vs  Central database  vs  Permissioned blockchain.
    (Most of the benefit comes from traceability itself, not from the ledger; the model isolates
    the *incremental* value of the blockchain over a plain database -- the real RQ4.)
  * Base / Adverse / Severe scenarios + a mixed-regime Monte Carlo (common random numbers across options).
  * Closed-form break-even (what regulatory-risk level makes the programme pay back).

Run:   python3 src/palm_oil_traceability_model.py       (prints tables, writes CSVs to data/derived/)
Needs: numpy, pandas
Every number marked ASSUMPTION below is a placeholder to calibrate -- change it, rerun.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
N_SIMS = 20_000

# --------------------------------------------------------------------------------------
# 1. MARKET DATA  (transcribed from Bloomberg HP / Historical Price Table screens)
#    CPO = KOZ6 Comdty (Bursa Malaysia crude palm oil, Dec-26 contract, MYR/tonne)
#    WIL SP (SGD), NESN SW (CHF), ULVR LN (GBp).  Blank = no print on that day.
# --------------------------------------------------------------------------------------
def _d(s):  # "MM/DD" -> 2026 date
    m, d = s.split("/")
    return pd.Timestamp(2026, int(m), int(d))

CPO = {"10/15": 4666, "10/14": 4700, "10/13": 4682, "10/12": 4637, "10/09": 4592, "10/08": 4661,
       "10/07": 4524, "10/06": 4560, "10/05": 4578, "10/02": 4535, "10/01": 4554, "09/30": 4610,
       "09/29": 4624, "09/28": 4664, "09/25": 4672, "09/24": 4772, "09/23": 4768, "09/22": 4810,
       "09/21": 4857, "09/18": 4898, "09/17": 4936, "09/15": 4998, "09/14": 4958, "09/11": 4944,
       "09/10": 5033, "09/09": 5109, "09/08": 5115, "09/07": 5110, "09/04": 5054, "09/03": 5018,
       "09/02": 5065, "09/01": 5072, "08/28": 4988, "08/27": 4907, "08/26": 4931, "08/24": 5013,
       "08/21": 5077, "08/20": 5025, "08/19": 4972, "08/18": 4943, "08/17": 4903}
WIL = {"10/09": 3.55, "10/08": 3.53, "10/07": 3.60, "10/06": 3.60, "10/05": 3.48, "10/02": 3.47,
       "10/01": 3.51, "09/30": 3.61, "09/29": 3.58, "09/28": 3.61, "09/25": 3.68, "09/24": 3.65,
       "09/23": 3.67, "09/22": 3.65, "09/21": 3.65, "09/18": 3.68, "09/17": 3.73, "09/16": 3.71,
       "09/15": 3.70, "09/14": 3.72, "09/11": 3.71, "09/10": 3.71, "09/09": 3.73, "09/08": 3.73,
       "09/07": 3.80, "09/04": 3.82, "09/03": 3.84, "09/02": 3.84, "09/01": 3.76, "08/31": 3.84,
       "08/28": 3.81, "08/27": 3.77, "08/26": 3.75, "08/25": 3.75, "08/24": 3.76, "08/21": 3.71,
       "08/20": 3.66, "08/19": 3.64, "08/18": 3.70, "08/17": 3.67}
NESN = {"10/09": 76.04, "10/08": 76.00, "10/07": 75.56, "10/06": 75.20, "10/05": 74.48, "10/02": 74.78,
        "10/01": 74.63, "09/30": 76.02, "09/29": 76.26, "09/28": 77.00, "09/25": 77.17, "09/24": 77.94,
        "09/23": 77.10, "09/22": 77.09, "09/21": 77.10, "09/18": 76.27, "09/17": 78.33, "09/16": 77.66,
        "09/15": 77.89, "09/14": 79.20, "09/11": 77.54, "09/10": 77.74, "09/09": 77.73, "09/08": 80.39,
        "09/07": 78.76, "09/04": 78.31, "09/03": 77.84, "09/02": 78.63, "09/01": 78.51, "08/31": 78.82,
        "08/28": 78.62, "08/27": 78.52, "08/26": 79.87, "08/25": 79.82, "08/24": 80.46, "08/21": 79.68,
        "08/20": 79.40, "08/19": 79.34, "08/18": 79.20, "08/17": 78.71}
ULVR = {"10/14": 4829.0, "10/13": 4710.5, "10/12": 4738.0, "10/09": 4673.5, "10/08": 4626.0,
        "10/07": 4623.0, "10/06": 4569.0, "10/05": 4500.5, "10/02": 4483.5, "10/01": 4494.0,
        "09/30": 4603.5, "09/29": 4615.5, "09/28": 4671.0, "09/25": 4664.5, "09/24": 4708.5,
        "09/23": 4677.0, "09/22": 4698.0, "09/21": 4642.5, "09/18": 4621.0, "09/17": 4632.5,
        "09/16": 4640.0, "09/15": 4641.5, "09/14": 4697.0, "09/11": 4551.5, "09/10": 4559.0,
        "09/09": 4621.0, "09/08": 4695.5, "09/07": 4693.5, "09/04": 4763.0, "09/03": 4733.0,
        "09/02": 4782.5, "09/01": 4811.0, "08/28": 4776.0, "08/27": 4752.0, "08/26": 4772.0,
        "08/25": 4761.5, "08/24": 4782.5, "08/21": 4681.0, "08/20": 4649.0, "08/19": 4638.5,
        "08/18": 4578.0, "08/17": 4512.5}


def price_frame() -> pd.DataFrame:
    idx = pd.bdate_range("2026-08-17", "2026-10-15")
    df = pd.DataFrame(index=idx)
    for name, ser in (("CPO", CPO), ("WIL", WIL), ("NESN", NESN), ("ULVR", ULVR)):
        df[name] = pd.Series({_d(k): v for k, v in ser.items()})
    return df


def market_analytics(df: pd.DataFrame) -> pd.DataFrame:
    """Log returns only across consecutive rows with prints on both days (same rule as the workbook)."""
    ret = pd.DataFrame(index=df.index)
    for c in df.columns:
        prev = df[c].shift(1)
        ret[c] = np.where(df[c].notna() & prev.notna(), np.log(df[c] / prev), np.nan)
    rows = []
    for c in ("CPO", "WIL", "NESN", "ULVR"):
        r = ret[c].dropna()
        row = {"series": c, "n_returns": len(r), "ann_vol_%": r.std(ddof=1) * np.sqrt(252) * 100}
        if c != "CPO":
            pair = ret[[c, "CPO"]].dropna()
            row["n_pairs_vs_CPO"] = len(pair)
            row["corr_vs_CPO"] = pair[c].corr(pair["CPO"])
            row["beta_vs_CPO"] = np.polyfit(pair["CPO"], pair[c], 1)[0]
        rows.append(row)
    return pd.DataFrame(rows).set_index("series")


CPO_SIGMA = market_analytics(price_frame()).loc["CPO", "ann_vol_%"] / 100  # annualised, ~8 week sample (!)

# --------------------------------------------------------------------------------------
# 2. COST-BENEFIT MODEL INPUTS
#    Bloomberg-sourced: revenue, COGS (FY2025).  Everything else = ASSUMPTION (calibrate).
# --------------------------------------------------------------------------------------
G = dict(
    r=0.08,        # ASSUMPTION  discount rate (use each firm's WACC from Bloomberg WACC <GO>)
    g=0.02,        # ASSUMPTION  nominal growth of revenue / COGS / programme opex
    horizon=7,     # years of benefits after the year-0 build
    fine=0.02,     # ASSUMPTION  realised fine as share of EU turnover when non-compliant. EUDR cap is "at least 4%"
    q=0.30,        # ASSUMPTION  share of non-traceable EU-bound palm volume that must be excluded / re-sourced
    pi=0.06,       # ASSUMPTION  price premium paid on re-sourced (compliant) volume
    c0=0.30,       # ASSUMPTION  traceable share today (RSPO / NDPE style partial coverage)
    EURUSD=1.15,   # ASSUMPTION  replace with Bloomberg FX on the data date
    CHFUSD=1.25,   # ASSUMPTION  replace with Bloomberg FX on the data date
)

SCEN = {  # multipliers on the base inputs
    "Base":    dict(p_reg=1.0, p_ctrv=1.0, pi=1.0, cpo=1.00),
    "Adverse": dict(p_reg=2.0, p_ctrv=1.5, pi=1.5, cpo=1.00),
    "Severe":  dict(p_reg=4.0, p_ctrv=2.5, pi=2.5, cpo=1.30),
}

PROFILES = {  # revenue / COGS from Bloomberg FA (FY2025, reporting currency millions); rest ASSUMPTION
    "ULVR": dict(name="Unilever", rev=50503.0, cogs=26794.0, fx="EURUSD",
                 a=0.25, ps=0.030, eu=0.25, p_reg=0.03, p_ctrv=0.10, rev_loss=0.005,
                 cost={"DB": (8.0, 3.0), "BC": (14.0, 4.5)}),
    "NESN": dict(name="Nestle", rev=89885.0, cogs=48694.0, fx="CHFUSD",
                 a=0.15, ps=0.015, eu=0.25, p_reg=0.03, p_ctrv=0.10, rev_loss=0.005,
                 cost={"DB": (7.0, 2.5), "BC": (12.0, 4.0)}),
    "WIL":  dict(name="Wilmar", rev=70415.7, cogs=64619.9, fx=None,
                 a=0.40, ps=0.300, eu=0.08, p_reg=0.05, p_ctrv=0.15, rev_loss=0.010,
                 cost={"DB": (25.0, 10.0), "BC": (40.0, 14.0)}),
}
# a=palm-linked revenue share, ps=palm spend / COGS, eu=EU-regulated revenue share,
# p_reg=annual prob. of a regulatory/market-access event, p_ctrv=annual prob. of a controversy,
# rev_loss=revenue lost on palm-linked sales in a controversy. cost = (capex $m, annual opex $m).

OPTIONS = {  # cmax = steady-state traceable share, ramp = years to get there, eff = assurance value of that coverage
    "SQ": dict(cmax=None, ramp=1.0, eff=0.60),       # cmax -> c0
    "DB": dict(cmax=0.80, ramp=3.0, eff=0.80),       # central / cloud database + satellite + audits
    "BC": dict(cmax=0.90, ramp=4.0, eff=0.90),       # permissioned ledger consortium (slower to coordinate, higher trust)
}


def usd(profile, key):
    fx = G[profile["fx"]] if profile["fx"] else 1.0
    return profile[key] * fx


# --------------------------------------------------------------------------------------
# 3. CORE ENGINE  (vectorised: parameters may be scalars or arrays of length n)
# --------------------------------------------------------------------------------------
def pv_total(pf, opt, prm, price_idx=None):
    """PV of (expected losses + programme costs) for one option. Returns dict of arrays."""
    T = G["horizon"]
    t = np.arange(1, T + 1)
    growth = (1 + G["g"]) ** t
    rev, cogs = usd(pf, "rev") * growth, usd(pf, "cogs") * growth
    c0 = prm.get("c0", G["c0"])
    cmax = c0 if opt == "SQ" else prm["cmax"]
    ramp = 1.0 if opt == "SQ" else prm["ramp"]
    eff = prm["eff"]
    col = lambda x: np.asarray(x)[:, None] if np.ndim(x) == 1 else np.asarray(x)
    cov = col(c0) + (col(cmax) - col(c0)) * np.minimum(1.0, t / col(ramp))
    m = cov * col(eff)
    P = 1.0 if price_idx is None else price_idx
    reg = col(prm["p_reg"]) * col(prm["fine"]) * pf["eu"] * rev * (1 - m)
    spend = cogs * pf["ps"] * P
    sub = spend * pf["eu"] * (1 - cov) * col(prm["q"]) * col(prm["pi"])
    rep = col(prm["p_ctrv"]) * pf["rev_loss"] * pf["a"] * rev * (1 - m)
    capex, opex = (0.0, 0.0) if opt == "SQ" else pf["cost"][opt]
    if opt != "SQ":
        capex = prm.get(f"capex_{opt}", capex)
        opex = prm.get(f"opex_{opt}", opex)
    opex_t = col(opex) * growth
    df_ = 1.0 / (1 + col(prm["r"])) ** t
    sumd = lambda x: np.sum(x * df_, axis=-1)
    shape = np.shape(sumd(reg))
    out = dict(pv_reg=sumd(reg), pv_sub=sumd(sub), pv_rep=sumd(rep),
               pv_opex=sumd(opex_t * np.ones_like(reg)), capex=np.asarray(capex) * np.ones(shape))
    out["pv_loss"] = out["pv_reg"] + out["pv_sub"] + out["pv_rep"]
    out["pv_prog"] = out["pv_opex"] + out["capex"]
    out["pv_total"] = out["pv_loss"] + out["pv_prog"]
    return out


def deterministic(profile_key, scn="Base", overrides=None):
    pf = PROFILES[profile_key]
    s = SCEN[scn]
    price = np.full(G["horizon"], s["cpo"])
    res = {}
    for opt in OPTIONS:
        prm = dict(r=G["r"], fine=G["fine"], q=G["q"], pi=G["pi"] * s["pi"], c0=G["c0"],
                   p_reg=pf["p_reg"] * s["p_reg"], p_ctrv=pf["p_ctrv"] * s["p_ctrv"],
                   eff=OPTIONS[opt]["eff"], cmax=OPTIONS[opt]["cmax"], ramp=OPTIONS[opt]["ramp"])
        if overrides:  # {"all": {...shared...}, "BC": {...only that option...}}
            prm.update(overrides.get("all", {}))
            prm.update(overrides.get(opt, {}))
        res[opt] = pv_total(pf, opt, prm, price)
    sq = res["SQ"]["pv_total"]
    out = {}
    for opt in ("DB", "BC"):
        r = res[opt]
        avoided = res["SQ"]["pv_loss"] - r["pv_loss"]
        reg_av = res["SQ"]["pv_reg"] - r["pv_reg"]
        ben = sq - r["pv_total"]
        out[opt] = dict(benefit=float(ben), avoided=float(avoided), prog=float(r["pv_prog"]),
                        bcr=float(avoided / r["pv_prog"]), breakeven_k=float(max(0.0, 1 - ben / reg_av)))
    out["BC_minus_DB"] = out["BC"]["benefit"] - out["DB"]["benefit"]
    return out


# --------------------------------------------------------------------------------------
# 4. MONTE CARLO  (common random numbers: every option sees the same world)
# --------------------------------------------------------------------------------------
def tri(rng, lo, mode, hi, n):
    return rng.triangular(lo, mode, hi, n)


def monte_carlo(profile_key, regime="Mixed", n=N_SIMS, seed=SEED):
    rng = np.random.default_rng(seed)
    pf = PROFILES[profile_key]
    T = G["horizon"]
    # --- regime: fixed scenario, or mixed (25% benign / 50% base / 25% severe-enforcement) -------------
    if regime == "Mixed":
        pick = rng.choice(3, size=n, p=[0.25, 0.50, 0.25])
        mult = np.array([[0.4, 0.6, 1.0, 1.0], [1, 1, 1, 1.0], [4, 2.5, 2.5, 1.3]])[pick]
        m_reg, m_ctrv, m_pi, m_cpo = mult.T
    else:
        s = SCEN[regime]
        m_reg = np.full(n, s["p_reg"]); m_ctrv = np.full(n, s["p_ctrv"])
        m_pi = np.full(n, s["pi"]); m_cpo = np.full(n, s["cpo"])
    # --- shared risk parameters ---------------------------------------------------------------------------
    shared = dict(
        p_reg=pf["p_reg"] * m_reg * rng.lognormal(0, 0.5, n),
        p_ctrv=pf["p_ctrv"] * m_ctrv * rng.lognormal(0, 0.4, n),
        fine=rng.uniform(0.005, 0.04, n),
        q=tri(rng, 0.10, G["q"], 0.50, n),
        pi=G["pi"] * m_pi * rng.lognormal(0, 0.3, n),
        r=tri(rng, 0.06, G["r"], 0.11, n),
        c0=tri(rng, 0.15, G["c0"], 0.45, n),
    )
    # CPO price index: GBM, zero drift, sample vol (+ severe shock level)
    z = rng.standard_normal((n, T))
    logp = np.cumsum(-0.5 * CPO_SIGMA ** 2 + CPO_SIGMA * z, axis=1)
    price = m_cpo[:, None] * np.exp(logp)
    # --- option-specific parameters ----------------------------------------------------------------------
    opts = {
        "SQ": dict(eff=tri(rng, 0.45, OPTIONS["SQ"]["eff"], 0.70, n)),
        "DB": dict(cmax=tri(rng, 0.60, 0.80, 0.92, n), ramp=tri(rng, 2.0, 3.0, 5.0, n),
                   eff=tri(rng, 0.55, 0.80, 0.92, n)),
        "BC": dict(cmax=tri(rng, 0.65, 0.90, 0.97, n), ramp=tri(rng, 3.0, 4.0, 7.0, n),
                   eff=tri(rng, 0.65, 0.90, 0.98, n)),
    }
    overrun = {"DB": rng.lognormal(0, 0.30, n), "BC": rng.lognormal(0, 0.35, n)}
    res = {}
    for opt in OPTIONS:
        prm = dict(shared); prm.update(opts[opt])
        if opt != "SQ":
            cap, opx = pf["cost"][opt]
            prm["capex_" + opt] = cap * overrun[opt]
            prm["opex_" + opt] = opx * overrun[opt]
        res[opt] = pv_total(pf, opt, prm, price)
    sq = res["SQ"]["pv_total"]
    ben = {o: sq - res[o]["pv_total"] for o in ("DB", "BC")}
    return ben


def mc_summary():
    rows = []
    for pk in PROFILES:
        for regime in ("Base", "Adverse", "Severe", "Mixed"):
            b = monte_carlo(pk, regime)
            for opt in ("DB", "BC"):
                x = b[opt]
                rows.append(dict(profile=pk, regime=regime, option=opt, mean=x.mean(), p5=np.percentile(x, 5),
                                 median=np.median(x), p95=np.percentile(x, 95), p_positive=(x > 0).mean(),
                                 p_BC_beats_DB=(b["BC"] > b["DB"]).mean() if opt == "BC" else np.nan,
                                 mean_BC_minus_DB=(b["BC"] - b["DB"]).mean() if opt == "BC" else np.nan))
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------------------
# 5. SENSITIVITY (one-at-a-time)  and  COVERAGE x EXCLUSION GRID (traceability + substitution simulation)
# --------------------------------------------------------------------------------------
def tornado(profile_key="ULVR", opt="BC"):
    pf0 = PROFILES[profile_key]
    base = deterministic(profile_key)[opt]["benefit"]
    cases = [
        ("Regulatory event probability (x0.5 / x2)", {"all": dict(p_reg=pf0["p_reg"] * 0.5)}, {"all": dict(p_reg=pf0["p_reg"] * 2)}),
        ("Realised fine rate (1% / 4%)", {"all": dict(fine=0.01)}, {"all": dict(fine=0.04)}),
        ("Controversy probability (x0.5 / x2)", {"all": dict(p_ctrv=pf0["p_ctrv"] * 0.5)}, {"all": dict(p_ctrv=pf0["p_ctrv"] * 2)}),
        ("Substitution premium (3% / 12%)", {"all": dict(pi=0.03)}, {"all": dict(pi=0.12)}),
        ("Share excluded / re-sourced (15% / 50%)", {"all": dict(q=0.15)}, {"all": dict(q=0.50)}),
        ("Blockchain effectiveness (0.75 / 0.97)", {opt: dict(eff=0.75)}, {opt: dict(eff=0.97)}),
        ("Steady-state coverage (0.75 / 0.95)", {opt: dict(cmax=0.75)}, {opt: dict(cmax=0.95)}),
        ("Ramp-up years (7 / 3)", {opt: dict(ramp=7.0)}, {opt: dict(ramp=3.0)}),
        ("Discount rate (12% / 6%)", {"all": dict(r=0.12)}, {"all": dict(r=0.06)}),
        ("Baseline coverage today (45% / 15%)", {"all": dict(c0=0.45)}, {"all": dict(c0=0.15)}),
        ("Programme cost (x1.6 / x0.7)", {opt: dict(capex_BC=pf0["cost"]["BC"][0] * 1.6, opex_BC=pf0["cost"]["BC"][1] * 1.6)}, {opt: dict(capex_BC=pf0["cost"]["BC"][0] * 0.7, opex_BC=pf0["cost"]["BC"][1] * 0.7)}),
    ]
    rows = []
    for label, lo, hi in cases:
        def run(ov):
            # overrides that must only hit the chosen option are applied through deterministic() generically
            return deterministic(profile_key, overrides=ov)[opt]["benefit"]
        rows.append(dict(driver=label, low_case=run(lo) - base, high_case=run(hi) - base))
    df = pd.DataFrame(rows)
    df["swing"] = (df.high_case - df.low_case).abs()
    return base, df.sort_values("swing", ascending=False).reset_index(drop=True)


def coverage_exclusion_grid(profile_key="ULVR", pi_mult=1.0):
    """PV (USD m) of supplier-substitution cost for a given steady traceable share and exclusion share."""
    pf = PROFILES[profile_key]
    T = G["horizon"]; t = np.arange(1, T + 1)
    growth = (1 + G["g"]) ** t
    cogs = usd(pf, "cogs") * growth
    dfac = 1 / (1 + G["r"]) ** t
    covs = np.arange(0.2, 1.01, 0.1)
    qs = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    grid = np.zeros((len(covs), len(qs)))
    for i, c in enumerate(covs):
        for j, q in enumerate(qs):
            sub = cogs * pf["ps"] * pf["eu"] * (1 - c) * q * G["pi"] * pi_mult
            grid[i, j] = np.sum(sub * dfac)
    return pd.DataFrame(grid, index=[f"{c:.0%}" for c in covs], columns=[f"{q:.0%}" for q in qs])


# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    out = Path(__file__).resolve().parents[1] / "data" / "derived"
    out.mkdir(parents=True, exist_ok=True)
    pd.set_option("display.width", 200, "display.float_format", lambda x: f"{x:,.2f}")
    print("== Market analytics (8-week sample -- indicative only) ==")
    print(market_analytics(price_frame()))
    print(f"\nCPO annualised vol used in simulation: {CPO_SIGMA:.1%}")
    print("\n== Deterministic NPV benefit vs status quo (USD m, PV) ==")
    rows = []
    for pk in PROFILES:
        for scn in SCEN:
            d = deterministic(pk, scn)
            rows.append(dict(profile=pk, scenario=scn,
                             DB_benefit=d["DB"]["benefit"], BC_benefit=d["BC"]["benefit"],
                             BC_minus_DB=d["BC_minus_DB"], DB_BCR=d["DB"]["bcr"], BC_BCR=d["BC"]["bcr"],
                             BC_breakeven_k=d["BC"]["breakeven_k"]))
    det = pd.DataFrame(rows); print(det)
    det.to_csv(out / "deterministic_results.csv", index=False)
    print("\n== Monte Carlo (n=%d, seed=%d) ==" % (N_SIMS, SEED))
    mc = mc_summary(); print(mc)
    mc.to_csv(out / "monte_carlo_summary.csv", index=False)
    base, tor = tornado()
    print(f"\n== Tornado: Unilever blockchain, base benefit {base:,.1f} ==")
    print(tor)
    tor.to_csv(out / "tornado_ULVR_BC.csv", index=False)
    print("\n== Coverage x exclusion grid (Unilever, PV substitution cost, USD m) ==")
    print(coverage_exclusion_grid())
