from lib import *
import json, numpy as np
N = J("nums.json"); det = N["det"]; comps = N["comps"]; par = J("parity2.json"); FR = J("fine_rob.json")
mc = {(r["profile"], r["regime"], r["option"]): r for r in N["mc"]}
NM = {"ULVR": "Unilever", "NESN": "Nestlé", "WIL": "Wilmar"}

def eqline(doc, text):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; pfmt(p, 1, 3, 1.1, False, WD_ALIGN_PARAGRAPH.CENTER); r = p.add_run(text); set_font(r, 10.5, False, True, INKC, name="Cambria")

def build(doc):
    h1(doc, "Chapter 5  Blockchain Architecture and Financial Stress Testing")
    h2(doc, "5.1  Proposed permissioned blockchain architecture")
    para(doc, "The design follows the minimum blockchain expectation of the course brief: it names the actors, the data objects, the permission model, the transaction flow, the oracle inputs, the governance and the measurable business value (Table 5.1). Figure 5.1 shows the physical flow of palm oil (plantation → mill → refinery → manufacturer → EU market) alongside the digital flow that records and verifies it.")
    figure(doc, 5, "f08_architecture.png", "Permissioned traceability architecture: physical flow, oracle inputs, ledger events and contracts", "Source: authors’ design. Raw data (polygons, imagery, audit files) stay off-chain; only hashes, lot identifiers and signed attestations are written on-chain.", width=15.6)
    table_cap(doc, 5, "Architecture specification")
    table(doc, ["Element", "Design choice", "Why"], [
        ["Actors (nodes)", "Brand owners (Unilever, Nestlé), refiners/traders (Wilmar-type), large mills, certifiers/auditors; read-only access for EU competent authorities and NGOs", "The parties that carry legal liability must be identifiable; mills and smallholders join through their mill group"],
        ["Data objects", "Plot record (polygon hash, owner ID, land-title reference); lot (FFB lot → CPO lot → RBD lot) with volume, date, location; verification attestation; due-diligence-statement reference", "One lot ID is split and merged but never created without an upstream parent"],
        ["Permission model", "Permissioned, role-based. Writers are the party that physically holds the lot; validators are consortium members; regulators read", "Commercial confidentiality plus regulator access"],
        ["Transaction flow", "(1) register plot → (2) satellite check against the 31-Dec-2020 cut-off → (3) mill batch event → (4) refinery split/merge under a mass-balance cap → (5) due-diligence statement → escrow release", "Maps to EUDR Articles 9–10: geolocation, risk assessment, statement"],
        ["Oracles / data inputs", "Satellite deforestation alerts, scale and sensor weights, QR/RFID lot tags, third-party audits, customs and EU information-system data", "The ledger is only as true as its inputs; two independent sources per critical claim"],
        ["Consensus and platform", "Crash- or Byzantine-fault-tolerant voting among 10–30 known nodes (e.g., Hyperledger Fabric-type); optional public hash anchoring for external time-stamps", "High throughput, no mining cost, auditable"],
        ["Smart contracts", "Escrow release only for lots with a passing step-2 check and a balanced step-4 ledger; auto-hold on a new satellite alert; per-refinery mass-balance cap; premium or penalty payout", "Converts verification into payment terms, which is where behaviour changes"],
        ["Governance", "Consortium charter: membership and exit, voting, upgrade control, dispute and oracle-challenge process, data-portability and wind-down terms", "Without governance a ledger is just a shared spreadsheet"],
        ["Measurable value", "Coverage (traceable share of volume), mitigation (reduction of fines and controversy loss), time to trace a lot, cost per verified tonne", "Feeds the parameters in Section 5.2"],
    ], [2.9, 8.2, 5.3], 8, ["l", "l", "l"], bold_first_col=True)
    h3(doc, "Where a ledger adds value, and where it does not")
    table(doc, ["Problem", "Does a permissioned ledger solve it?", "What is also needed"], [
        ["Same certified tonne claimed twice (double claiming)", "**Yes.** Unique lot IDs and a refinery mass-balance cap make over-claiming visible and block payment", "Complete participation by refineries"],
        ["Shared, tamper-evident record among competitors with no neutral intermediary", "**Yes.** Core strength of a consortium ledger", "Consortium governance"],
        ["Conditional payment on verified origin", "**Yes**, through escrow smart contracts", "Reliable verification event"],
        ["False data at the source (forged polygon, bribed auditor)", "**No.** The ledger preserves lies as faithfully as truths (oracle problem)", "Satellite and sensor data, independent audits, challenge rights"],
        ["Smallholder onboarding and cost", "**No.** It is an organisational and financing problem", "Mill-led registration, subsidy or premium"],
        ["Single company tracking its own supply", "**No.** A central database is cheaper and equivalent", "Nothing: do not use a blockchain"],
    ], [5.6, 6.2, 4.6], 8.3, ["l", "l", "l"])
    note(doc, "Source: authors’ analysis, building on Caldarelli (2020), Babich and Hilary (2020) and Cole et al. (2019).")
    para(doc, "The test for adding a ledger is therefore narrow: several mutually distrustful parties must share one state, no neutral operator can be trusted to hold it, and payments must depend on it. The cost-benefit analysis below asks whether that narrow advantage is worth its extra cost over a well-run central database.")

    h2(doc, "5.2  Simulation design")
    para(doc, "We compare three options over a seven-year horizon (year 0 build, years 1–7 benefits), for each firm: the **status quo** (fragmented, partly certified supply), a **central database** (one operator holds plot, lot and verification records; satellite checks and audits feed it) and a **permissioned blockchain** (the architecture above). For each option the model computes expected annual loss in three channels, adds programme cost and discounts at the firm’s rate. The **benefit** of an option is the present value (PV) of the status-quo total cost minus the PV of the option’s total cost.", after=3)
    eqline(doc, "Coverage:  c(t) = c₀ + (c_max − c₀) · min(1, t / ramp)          Mitigation:  m(t) = c(t) · eff")
    eqline(doc, "Regulatory loss:  Reg(t) = p_reg · fine · EU · Rev(t) · (1 − m(t))")
    eqline(doc, "Supplier substitution:  Sub(t) = PalmSpend(t) · EU · (1 − c(t)) · q · π · P(t)")
    eqline(doc, "Reputational loss:  Rep(t) = p_ctrv · rev_loss · a · Rev(t) · (1 − m(t))")
    eqline(doc, "Benefit = PV(total cost, status quo) − PV(total cost, option),   total cost = Reg + Sub + Rep + OpEx, plus CapEx in year 0")
    para(doc, "Here Rev and PalmSpend grow at 2% a year, P(t) is the palm-oil price index, p_reg and p_ctrv are annual probabilities of a regulatory event and a public controversy, *fine* is the realised fine as a share of EU turnover, EU the EU-regulated share of revenue, *a* the palm-linked share of revenue, *q* the share of untraced volume that must be excluded and re-sourced, and π the price premium on re-sourced compliant volume. The status quo has coverage c₀ and mitigation c₀ × 0.60. **Break-even** is solved in closed form: the factor k on p_reg at which the benefit is zero is k = max(0, 1 − Benefit / PV of regulatory loss avoided). The **benefit–cost ratio** is PV of losses avoided over PV of programme cost (CapEx plus discounted OpEx); **ROI** = ratio − 1. Tables 5.2–5.4 list the inputs and the three scenarios.", after=4)
    callout(doc, "Every parameter below except revenue and COGS is an ASSUMPTION", "Bloomberg supplies FY2025 revenue and COGS (Chapter 3). Probabilities, fines, premia, coverage, effectiveness and programme costs are not observable on the Terminal; they are placeholders chosen to be plausible, documented in the workbook sheet Assumptions and exposed to sensitivity analysis. Replace them with Wilmar-, Unilever- and Nestlé-specific estimates (and Bloomberg WACC and FX) before relying on absolute NPVs.", "warn")
    table_cap(doc, 5, "Global and option parameters (ASSUMPTION)")
    table(doc, ["Parameter", "Value", "Meaning"], [
        ["Discount rate r / growth g / horizon", "8% / 2% / 7 years", "Replace r with firm WACC from Bloomberg WACC <GO>"],
        ["Realised fine (share of EU turnover)", "2% (range 0.5–4%)", "EUDR cap is at least 4%; actual fining practice is unknown"],
        ["Untraced EU-bound volume excluded, q", "30%", "Share re-sourced when it cannot be shown compliant"],
        ["Price premium on re-sourced volume, π", "6%", "Compliant-supply premium"],
        ["Traceable share today, c₀", "30%", "RSPO/NDPE-style partial coverage"],
        ["Palm-oil price volatility", "17.05% a year", "Bloomberg KOZ6, 8-week window; used in Monte Carlo (geometric Brownian motion)"],
        ["FX to USD", "EUR 1.15; CHF 1.25", "Illustrative; replace with Bloomberg FX on the data date"],
        ["Status quo: effectiveness", "0.60", "Mitigation per unit of coverage"],
        ["Central database: steady coverage / ramp / effectiveness", "80% / 3 years / 0.80", "Central stack plus satellite and audits"],
        ["Permissioned blockchain: steady coverage / ramp / effectiveness", "90% / 4 years / 0.90", "Slower to coordinate, higher assurance"],
    ], [6.0, 3.6, 6.8], 8.3, ["l", "l", "l"], bold_first_col=True)
    table_cap(doc, 5, "Firm profiles and programme costs (ASSUMPTION except revenue and COGS)")
    table(doc, ["", "Unilever", "Nestlé", "Wilmar"], [
        ["FY2025 revenue / COGS (reporting currency, m) — Bloomberg", "EUR 50,503 / 26,794", "CHF 89,885 / 48,694", "USD 70,416 / 64,620"],
        ["Palm-linked revenue share, a", "25%", "15%", "40%"],
        ["Palm spend as share of COGS", "3.0%", "1.5%", "30%"],
        ["EU-regulated revenue share", "25%", "25%", "8% (indirect)"],
        ["Annual regulatory-event probability, p_reg", "3%", "3%", "5%"],
        ["Annual controversy probability, p_ctrv", "10%", "10%", "15%"],
        ["Revenue lost on palm-linked sales in a controversy", "0.5%", "0.5%", "1.0%"],
        ["Central database: CapEx / OpEx per year (USD m)", "8.0 / 3.0", "7.0 / 2.5", "25.0 / 10.0"],
        ["Permissioned blockchain: CapEx / OpEx per year (USD m)", "14.0 / 4.5", "12.0 / 4.0", "40.0 / 14.0"],
    ], [6.8, 3.2, 3.2, 3.2], 8.3, ["l", "c", "c", "c"], bold_first_col=False)
    note(doc, "Wilmar’s EU share is low because its sales are mostly in China and Asia; EUDR pressure reaches it through customers such as Unilever and Nestlé (Chapter 3).")
    table_cap(doc, 5, "Scenario definitions (multipliers on base risk inputs)")
    table(doc, ["Scenario", "Regulatory-event probability", "Controversy probability", "Substitution premium", "Palm price level", "Narrative"], [
        ["Base", "×1", "×1", "×1", "×1.0", "Enforcement as expected: low inspection intensity in year 1–2"],
        ["Adverse", "×2", "×1.5", "×1.5", "×1.0", "Active enforcement; NGO and press scrutiny rises"],
        ["Severe", "×4", "×2.5", "×2.5", "×1.3", "Strict enforcement, a high-profile case and a palm price spike"],
    ], [1.9, 3.0, 2.6, 2.5, 2.0, 4.4], 8.3, ["l", "c", "c", "c", "c", "l"], bold_first_col=True)
    para(doc, "**Monte Carlo.** To describe uncertainty we draw 20,000 worlds with a fixed seed (42). In each, regulatory and controversy probabilities are multiplied by log-normal noise (σ = 0.5 and 0.4), the realised fine is uniform on 0.5–4%, the exclusion share q is triangular (10%, 30%, 50%), the premium is log-normal (σ = 0.3), the discount rate is triangular (6%, 8%, 11%) and the baseline coverage triangular (15%, 30%, 45%). The palm price follows a geometric Brownian motion with the sample volatility. Programme cost overruns are log-normal (σ = 0.30 for the database and 0.35 for the ledger), and the options’ own coverage, ramp-up and effectiveness are triangular. *Mixed* runs draw an enforcement regime for each world (25% benign, 50% base, 25% severe). Every option is evaluated on **the same random draws** (common random numbers), so differences between options are not simulation noise.", after=4)

    h2(doc, "5.3  ROI and stress-test results")
    h3(doc, "Untraced cost versus traced cost")
    para(doc, "Figure 5.2 splits the PV of total cost in the base case into the three loss channels and the programme cost. **Untraced cost** is the status-quo bar: EUDR fines and market-access loss, emergency supplier substitution and brand damage. **Traced cost** is the option bar: the same losses reduced by coverage and mitigation, plus CapEx and OpEx. Both options cut total cost relative to the status quo in every firm, because the avoided losses exceed the programme cost.")
    figure(doc, 5, "f10_cost_decomp.png", "PV of total cost by option, base scenario (USD m)", "Source: palm_oil_traceability_model.py; workbook sheets ROI_ULVR, ROI_NESN, ROI_WIL. All risk inputs are ASSUMPTION.")
    rows = []
    for k in ("ULVR", "NESN", "WIL"):
        for s in ("Base", "Adverse", "Severe"):
            c = comps[f"{k}_{s}"]; d = det[f"{k}_{s}"]
            sq, bc, db = c["SQ"]["pv_total"], c["BC"]["pv_total"], c["DB"]["pv_total"]
            rows.append([NM[k] if s == "Base" else "", s, f"{sq:,.0f}", f"{bc:,.0f}", f"{c['BC']['pv_prog']:,.0f}", f"{d['BC']['benefit']:,.1f}", f"{(d['BC']['bcr']-1)*100:,.0f}%", f"{d['DB']['benefit']:,.1f}", f"{d['BC_minus_DB']:+,.1f}"])
    table_cap(doc, 5, "Base, adverse and severe results (PV over 7 years, USD m)")
    table(doc, ["Firm", "Scenario", "Untraced cost (status quo)", "Traced cost (blockchain)", "of which programme cost", "NPV benefit, blockchain", "ROI, blockchain", "NPV benefit, central DB", "Blockchain minus DB"], rows, [1.5, 1.5, 1.9, 1.8, 1.7, 1.9, 1.9, 1.9, 2.3], 8, ["l", "l", "r", "r", "r", "r", "r", "r", "r"], highlight={i: "EEF6FB" for i in range(0, 9, 3)})
    note(doc, "Source: authors’ calculations from the companion model. Untraced and traced costs are PV of expected losses plus programme cost; NPV benefit = untraced − traced. ROI = PV of losses avoided / PV of programme cost − 1.")
    figure(doc, 5, "f09_scenario_npv.png", "NPV benefit versus the status quo, by firm and scenario", "Source: authors’ calculations; companion model. USD m, PV over seven years.")
    para(doc, "Three results stand out (Table 5.5, Figure 5.3). **First, traceability pays in every scenario**: the NPV benefit of the blockchain ranges from USD 16 m (Unilever, base) to USD 471 m (Wilmar, severe), and the central database is positive everywhere too. **Second, the technology choice is close in the base case and tips to the ledger under stress.** At base inputs the central database is better for Unilever (+USD 4.2 m) and Wilmar (+USD 3.6 m), and the blockchain better for Nestlé (+USD 2.3 m). In the adverse and severe cases the ledger leads by USD 3–56 m, because its higher coverage and assurance reduce the larger expected losses by more than its extra cost. **Third, scale matters**: Wilmar’s absolute benefits are largest because palm is 30% of its COGS and 40% of its revenue; Unilever’s are smallest.")
    table_cap(doc, 5, "Discounted payback and break-even in the base scenario")
    table(doc, ["", "Unilever", "Nestlé", "Wilmar"], [
        ["Discounted payback, central database (years)", "3", "2", "3"],
        ["Discounted payback, blockchain (years)", "5", "3", "4"],
        ["Break-even multiple on regulatory-event probability, blockchain (NPV = 0)", "0.34×", "0.01×", "0×"],
        ["Blockchain assurance value needed to match the database (database = 0.80), base", f"{N['parity']['ULVR_Base']:.2f}", f"{N['parity']['NESN_Base']:.2f}", f"{N['parity']['WIL_Base']:.2f}"],
        ["… same, adverse scenario", f"{N['parity']['ULVR_Adverse']:.2f}", f"{N['parity']['NESN_Adverse']:.2f}", f"{N['parity']['WIL_Adverse']:.2f}"],
        ["Blockchain cost multiple at which it ties with the database, base", f"{par['ULVR']['cost_mult']:.2f}× (cost 11% lower)", f"{par['NESN']['cost_mult']:.2f}× (can cost 7% more)", f"{par['WIL']['cost_mult']:.2f}× (cost 3% lower)"],
        ["Regulatory-event probability multiple at which blockchain ties with database", f"{par['ULVR']['preg_mult']:.2f}×", f"{par['NESN']['preg_mult']:.2f}×", f"{par['WIL']['preg_mult']:.2f}×"],
    ], [8.2, 2.7, 2.8, 2.7], 8.3, ["l", "c", "c", "c"])
    note(doc, "Source: workbook sheet Summary; authors’ root-finding on the companion model (parity points).")
    para(doc, "The parity points (Table 5.6) express the same message in decision-ready form. A blockchain with 0.90 assurance value clears the 0.80 database in the adverse case for all three firms (parity 0.82–0.87), but at base inputs it needs 0.88 to 0.96. Equivalently, a consortium that lowers the ledger’s programme cost by 3% (Wilmar) to 11% (Unilever), or an enforcement climate in which the regulatory-event probability is 1.8–2.1 times the base rate, is enough to tip the choice.")
    h3(doc, "Monte Carlo: how often does each option pay?")
    rows = []
    for k in ("ULVR", "NESN", "WIL"):
        for o, on in (("DB", "Central database"), ("BC", "Blockchain")):
            m = mc[(k, "Mixed", o)]; b = mc[(k, "Mixed", "BC")]
            rows.append([NM[k] if o == "DB" else "", on, f"{m['mean']:.0f}", f"{m['p5']:.0f}", f"{m['p95']:.0f}", f"{m['p_positive']*100:.0f}%", "—" if o == "DB" else f"{b['p_BC_beats_DB']*100:.0f}%"])
    table_cap(doc, 5, "Monte Carlo, mixed enforcement regimes (20,000 draws, USD m)")
    table(doc, ["Firm", "Option", "Mean NPV benefit", "5th percentile", "95th percentile", "P(NPV > 0)", "P(blockchain beats DB)"], rows, [2.2, 3.2, 2.3, 2.2, 2.2, 2.0, 2.3], 8.3, ["l", "l", "r", "r", "r", "r", "r"], highlight={i: "EEF6FB" for i in (0, 1, 4, 5)})
    note(doc, "Source: authors’ calculations; seed 42; common random numbers. P(beats DB) is the share of worlds in which the blockchain NPV exceeds the database NPV.")
    figure(doc, 5, "f11_mc.png", "Distribution of NPV benefit across 20,000 mixed-regime worlds", "Source: authors’ calculations; companion model.")
    para(doc, "In Table 5.7 and Figure 5.4, the database pays in 79% (Unilever), 93% (Nestlé) and 89% (Wilmar) of simulated worlds, the blockchain in 62%, 83% and 76%. The blockchain has the higher *mean* only for Nestlé and has a **fatter lower tail** (5th percentile −USD 33 m, −17 m and −70 m, against −13 m, −2 m and −23 m for the database) because of its larger sunk cost and longer ramp-up, while its upper tail is fatter in the severe regime. By regime, the blockchain beats the database in 32–40% of base-regime worlds, 41–51% of adverse worlds and 51–59% of severe worlds. Figure 5.5 plots the risk–return trade-off.")
    figure(doc, 5, "f15_risk_return.png", "Expected benefit versus downside (5th percentile) of each intervention", "Source: authors’ calculations; mixed-regime Monte Carlo.")
    h3(doc, "Sensitivity and substitution")
    figure(doc, 5, "f12_tornado.png", "One-at-a-time sensitivity of the Unilever blockchain NPV", "Source: authors’ calculations. Regulatory-event probability and fine rate enter the formula as a product, so they have identical effect and are shown as one bar.")
    para(doc, "For Unilever’s blockchain case (Figure 5.6) the most influential assumptions are the **expected regulatory loss rate** (event probability × fine; swing USD 37 m), the **programme cost** (35 m), the **controversy probability** (30 m) and the **ramp-up time** (18 m). The discount rate matters least (8 m). Two implications follow: the value case is mostly a bet on enforcement intensity, which a company cannot control but can monitor (Chapter 6.3), and cost discipline in the ledger programme is as valuable as any increase in its effectiveness.")
    figure(doc, 5, "f13_cov_excl.png", "Coverage and substitution simulation: PV of supplier-substitution cost", "Source: authors’ calculations. Rows: steady-state traceable share; columns: share of untraced volume excluded and re-sourced. Unilever and Wilmar, USD m.", width=12.4)
    para(doc, "At 30% traceable supply (today’s assumption) and half of untraced volume excluded, Unilever’s PV substitution cost is USD 27 m and Wilmar’s USD 183 m; at 90% coverage they fall to USD 4 m and USD 26 m. Wilmar’s larger exposure (30% palm share of COGS) means each point of coverage is worth about seven times as much as for Unilever, which is why the high-coverage option is a strategic necessity there rather than a compliance choice.")
    h3(doc, "Robustness: fine rate and ledger cost")
    rows = []
    for k in ("ULVR", "NESN", "WIL"):
        for s in ("Base", "Adverse", "Severe"):
            a = next(r for r in FR if r["fine"] == 0.02 and r["firm"] == k and r["scn"] == s); b = next(r for r in FR if r["fine"] == 0.04 and r["firm"] == k and r["scn"] == s)
            rows.append([NM[k] if s == "Base" else "", s, f"{a['BC']:.0f}", f"{a['diff']:+.1f}", f"{b['BC']:.0f}", f"{b['diff']:+.1f}"])
    table_cap(doc, 5, "Effect of the realised fine rate (2% versus the 4% statutory floor for the maximum)")
    table(doc, ["Firm", "Scenario", "Blockchain NPV, fine 2%", "Blockchain minus DB, fine 2%", "Blockchain NPV, fine 4%", "Blockchain minus DB, fine 4%"], rows, [2.2, 2.2, 3.0, 3.2, 3.0, 3.2], 7.8, ["l", "l", "r", "r", "r", "r"], highlight={i: "EEF6FB" for i in range(0, 9, 3)}, pad=12)
    note(doc, "Source: authors’ calculations; USD m.", 4)
    para(doc, "A 4% realised fine is the pessimistic end (Article 25 sets 4% only as the floor of the maximum). In Table 5.8, doubling the fine to 4% lifts Unilever’s and Wilmar’s base-case difference from negative to about zero (+0.9 and −0.3) and widens Nestlé’s edge to USD 12 m. A heavier ledger cost case (CapEx USD 25 m, OpEx USD 5 m a year, five-year horizon, Unilever) gives a blockchain NPV of −USD 8 m at a 2% fine in the base scenario (benefit–cost ratio 0.8), +USD 8.5 m at 4%, and +USD 79 m to +USD 146 m in the severe scenario: **in the base case the ledger does not pay unless the realised fine is high**, but it protects against the severe case.")
    callout(doc, "Answer to RQ4 (conditional on the assumptions)", "Traceability is worth doing for all three firms. The *best risk–cost intervention* is a **staged programme**: a central traceability stack now (satellite checks, audits), built so that its records can be anchored on a permissioned ledger later. The ledger earns its extra cost when enforcement is adverse or severe, when competing refiners must share one balance sheet of lots, or when consortium financing lowers its cost by roughly 3–11%. On its own, a blockchain does not create value: most of the benefit comes from coverage and verification, which a database also delivers.", "ok")
