from wb_common import *
import wb_a, wb_b1, wb_b2, wb_c1, wb_c2

def build_front(wb):
    # ---------------- Summary ----------------
    ws = wb.create_sheet("Summary")
    title(ws, "CP-45 Blockchain Sustainable Palm Oil Traceability — Unilever · Nestlé · Wilmar",
          "Headline results (live links; scenario = Assumptions!B13). Model inputs marked ASSUMPTION are placeholders: read the numbers as decision logic, not forecasts.")
    put(ws, "A4", "Active scenario", f_bold); put(ws, "B4", "=Assumptions!B13", f_link, fill=fill_key)
    hdr(ws, 6, ["Headline metric", "Unilever", "Nestlé", "Wilmar", "Where it comes from"], height=24)
    O = wb_c1.ROIOUT; RS = wb_b2.RI["score_rows"]["Base weights"]; S = wb_b1.SC
    def row(r, lab, f, fmt, src, bold=False):
        put(ws, (r, 1), lab, f_bold if bold else f_norm)
        for j, co in enumerate(("ULVR", "NESN", "WIL")):
            put(ws, (r, 2 + j), f(co, j), f_link, fmt)
        put(ws, (r, 5), src, f_sub, border=False)
    sec(ws, 7, "Cost-benefit (USD m, PV over 7 years vs status quo)", 5)
    row(8, "NPV benefit — central database", lambda co, j: f"=ROI_{co}!E{O[co]['DB']}", NUM, "ROI_ sheets", True)
    row(9, "NPV benefit — permissioned blockchain", lambda co, j: f"=ROI_{co}!E{O[co]['BC']}", NUM, "ROI_ sheets", True)
    row(10, "Blockchain minus database (NPV)", lambda co, j: f"=ROI_{co}!E{O[co]['diff']}", NUM, "Negative = a plain database is the better buy at these inputs")
    row(11, "Benefit / programme cost — database", lambda co, j: f"=ROI_{co}!G{O[co]['DB']}", MULT, "")
    row(12, "Benefit / programme cost — blockchain", lambda co, j: f"=ROI_{co}!G{O[co]['BC']}", MULT, "")
    row(13, "Discounted payback (yrs) — database", lambda co, j: f"=ROI_{co}!I{O[co]['DB']}", '0', "")
    row(14, "Discounted payback (yrs) — blockchain", lambda co, j: f"=ROI_{co}!I{O[co]['BC']}", '0', "")
    row(15, "Break-even regulatory-risk multiplier — blockchain", lambda co, j: f"=ROI_{co}!H{O[co]['BC']}", '0.00"x"', "Factor on p_reg at which NPV = 0 (0 = pays even with no regulatory risk)")
    sec(ws, 17, "Monte Carlo, mixed enforcement regimes (static, from Python)", 5)
    for r, lab, col, fmt in ((18, "P(NPV > 0) — database", 8, '0%'), (19, "P(NPV > 0) — blockchain", 8, '0%'), (20, "P(blockchain beats database)", 9, '0%')):
        put(ws, (r, 1), lab)
        for j, co in enumerate(("ULVR", "NESN", "WIL")):
            opt = "DB" if "database" in lab and "beats" not in lab else "BC"
            put(ws, (r, 2 + j), f"=MC_Results!{L(col)}{wb_c2.MCROW[(co,'Mixed',opt)]}", f_link, fmt)
    sec(ws, 22, "Risk & visibility evidence (live)", 5)
    row(23, "Composite traceability risk index (0–100, base weights)", lambda co, j: f"=Risk_Index!{'HIJ'[j]}{RS}", NUM, "Risk_Index (relative ranking of 3 firms only)", True)
    put(ws, (24, 1), "Palm/plantation nodes visible in SPLC top suppliers")
    put(ws, (24, 2), f"=Supply_Chain!B{S['u_palmn']}", f_link, '0'); put(ws, (24, 3), f"=Supply_Chain!B{S['n_palmn']}", f_link, '0'); put(ws, (24, 4), f"=Supply_Chain!B{S['w_palmn']}", f_link, '0')
    put(ws, (24, 5), "Visible = shown on the captured screens (Wilmar: of 24 visible suppliers)", f_sub, border=False)
    put(ws, (25, 1), "Visible supplier cost as % of COGS (lower bound)")
    put(ws, (25, 2), f"=Supply_Chain!B{S['u_cov']}", f_link, PCT); put(ws, (25, 3), f"=Supply_Chain!B{S['n_cov']}", f_link, PCT); put(ws, (25, 4), f"=Supply_Chain!B{S['w_cov']}", f_link, '0.0%')
    put(ws, (26, 1), "Adverse news severity, last 12M (hand-coded)")
    for j, co in enumerate(("ULVR", "NESN", "WIL")): put(ws, (26, 2 + j), f"=News_Events!C{wb_b2.NEWSROW[co]}", f_link, '0')
    put(ws, (26, 5), "Different screen filters per firm — see News_Events warning", f_sub, border=False)
    sec(ws, 28, "What the evidence says (default inputs, base scenario)", 5)
    finds = [
     "1. Traceability pays in most simulated worlds (central database positive in 79–93% of mixed-regime draws); the technology choice is the close call. A central database + satellite/audit stack captures most of the benefit. At base inputs the blockchain only matches the database if its assurance value reaches ~0.88 (Nestlé), ~0.92 (Wilmar) or ~0.96 (Unilever) versus 0.80 for the database; under Adverse enforcement the parity points fall to ~0.82–0.87. In the mixed Monte Carlo the blockchain wins in roughly 35–42% of worlds. That is the honest answer to RQ4 — and a stronger capstone than 'blockchain always helps'.",
     "2. Bloomberg SPLC cannot see the palm chain. None of Unilever's or Nestlé's top-24 suppliers is a palm trader or plantation, Wilmar is not in either list, and the plantation nodes visible for Wilmar are ~0.4% of its cost base. The draft's 'mill → Wilmar → Unilever/Nestlé' chain is an assumption, not an SPLC finding (your Nestlé news screen shows Musim Mas and AAK as Nestlé's palm partners). This opacity IS the problem the blockchain would solve — use it as your motivating evidence, and add company mill lists as a second source.",
     "3. Wilmar ranks highest-risk on the composite index, driven by interest cover (~2.1x vs 8–9x), supplier conduct-risk flags (37% of listed suppliers) and the news record: the May-2026 Indonesian export under-invoicing probe, a corruption conviction of a unit executive, and the Russian asset-seizure report. Note these are governance/legal events, not deforestation events — the 'traceability' narrative must be separated from the 'governance' one.",
     "4. Wilmar's BESG score more than doubled (2.71 → 6.15) while reported Scope 1 emissions rose 2.6x: scores track disclosure, not footprint. Do not use a BESG score alone as a traceability-risk predictor (RQ1).",
     "5. KOZ6 palm oil sits ~9% below its 8-Sep-26 high (MYR 5,115 → 4,666) after a +18% rise over the range. With only ~8 weeks of aligned prices, correlations with the three equities are statistically zero (|ρ| < 0.35 band) — pull ≥5 years of data before claiming any price–equity link (RQ2).",
    ]
    r = 29
    for t in finds:
        put(ws, (r, 1), t, f_norm, align=wrap, border=False); ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=5); ws.row_dimensions[r].height = 78; r += 1
    widths(ws, {"A": 58, "B": 16, "C": 16, "D": 16, "E": 70})
    ws.freeze_panes = "B7"

    # ---------------- Start_Here ----------------
    st = wb.create_sheet("Start_Here")
    title(st, "Start here — what this workbook is, what changed, and what still needs your data",
          "CP-45 (row 46 of 'MBA_GEN_60_Bloomberg_Capstone_Projects'). Built from your 15-Oct-2026 Bloomberg screenshots, your draft plan, and the project brief.")
    sec(st, 4, "Colour legend", 4)
    put(st, "A5", "Blue text", f_in); put(st, "B5", "Value typed from a Bloomberg screenshot, or an assumption you can change")
    put(st, "A6", "Black text", f_calc); put(st, "B6", "Formula")
    put(st, "A7", "Green text", f_link); put(st, "B7", "Link to another sheet")
    put(st, "A8", "Yellow fill", f_norm, fill=fill_key); put(st, "B8", "Key assumption or headline output")
    sec(st, 10, "Sheet map", 4)
    smap = [("Summary", "Headline results and findings (live)"), ("Assumptions", "All judgement inputs + scenario switch (Base / Adverse / Severe)"),
            ("ROI_ULVR / ROI_NESN / ROI_WIL", "Year-by-year cost-benefit: status quo vs central database vs permissioned blockchain"),
            ("MC_Results", "Monte Carlo (20,000 draws × 4 regimes) — static from Python"), ("Sensitivity", "Tornado + coverage × substitution heat map — static from Python"),
            ("Risk_Index", "Composite risk index built on real indicators, three weight sets"), ("Supply_Chain", "SPLC panels, Wilmar supplier table, brand-owner supplier tables, HHI, coverage"),
            ("News_Events", "Hand-coded controversy log (12M window)"), ("ESG", "BESG scores and GHG scopes"), ("Fundamentals", "Income statement, balance sheet and cash-flow extracts + ratios"),
            ("Market_Data", "Snapshot and CPO futures stats"), ("Price_Analytics", "Aligned daily prices, returns, volatility, correlation, beta"), ("Next_Steps", "Data still to pull and how")]
    for i, (a, b) in enumerate(smap): put(st, (11 + i, 1), a, f_bold); put(st, (11 + i, 2), b)
    r = 11 + len(smap) + 1
    sec(st, r, "Review of the draft plan — what I changed and why", 4); r += 1
    hdr(st, r, ["Issue in the draft", "Why it matters", "Fix applied here", "Still for you to do"], height=24); r += 1
    items = [
     ("The Python code is cut off mid-formula ('+ 0.20 *') and the simulation / ROI code it promises is not in the file.", "Nothing runs; RQ3/RQ4 have no engine.", "Rebuilt end-to-end: palm_oil_traceability_model.py (market stats, NPV model, Monte Carlo, tornado, grid) and this workbook; Excel and Python NPVs tie exactly.", "Run the script after changing any assumption; paste refreshed tables into MC_Results/Sensitivity."),
     ("50 synthetic suppliers with random ESG, news hits and RSPO flags.", "Random inputs cannot answer RQ1–RQ3; an examiner will ask for the Bloomberg evidence.", "Replaced with the real Bloomberg data you captured (fundamentals, ESG, SPLC suppliers, news, prices).", "Pull the full SPLC lists and 5Y history (Next_Steps)."),
     ("The risk index weights (0.35 / 0.25 / 0.20 …) are chosen by hand and then a model is 'validated' against it.", "Circular: the model can only rediscover the weights you typed.", "Weights are explicit, editable, tested under three weight sets; ranking-stability check added.", "Calibrate against an outcome (forward drawdown, controversy count after events) once you have more firms and 5Y data."),
     ("The chain 'mill → Wilmar → Unilever/Nestlé' is presented as given.", "SPLC does not show it; your own news screen shows Nestlé's palm partners as Musim Mas and AAK.", "Flagged with evidence on Supply_Chain; opacity used as a finding.", "Search SPLC for Wilmar / IOI / Musim Mas / AAK / Cargill; add each brand owner's published mill list."),
     ("Only 'with vs without blockchain' is compared.", "Most of the benefit comes from traceability itself; the blockchain's value is the increment over a central database.", "Three options modelled; incremental NPV and P(blockchain beats database) reported.", "Defend the effectiveness gap (Assumptions!C43 vs D43) with evidence — it decides the answer."),
     ("Price series called 'KOA Comdty'.", "Your screens use KOZ6 Comdty (single Dec-26 contract, MYR).", "Documented on Market_Data; all stats use KOZ6.", "Use a continuous series (KO1 Comdty — confirm) and state the roll rule."),
     ("No regulatory timeline in the model.", "EU Deforestation Regulation obligations for large/medium operators apply from 30-Dec-2026 (per the European Commission's trade site, as fetched 22-Oct-2026).", "Regulatory loss channel with fine rate, EU share, scenarios (Adverse/Severe = stricter enforcement).", "Confirm palm oil's scope, the penalty ceiling and any further delay in the final regulation text before quoting."),
     ("Zero-knowledge proofs + Hyperledger Fabric/Corda in the architecture box.", "ZKPs add cost and complexity; the brief needs the economics, not a build.", "Not modelled; architecture cost is one capex/opex line.", "Keep ZKPs as an optional extension (selective disclosure of supplier prices); compare Fabric / Corda / permissioned EVM qualitatively."),
     ("ESG score used as a predictor.", "Wilmar's BESG score rose while its emissions rose — scores follow disclosure.", "Scored alongside conduct-risk, distress, news and balance-sheet indicators.", "Add disclosure-quality and certification-coverage variables."),
     ("Data comparability.", "Unilever FY24–25 restated for the ice-cream demerger; Unilever Scope 3 has series breaks; different news filters per firm; EUR/CHF/USD.", "Caveats on each sheet; FX is an explicit assumption; ratios not levels.", "Re-run all three firms with identical filters; replace illustrative FX with Bloomberg FX."),
    ]
    for it in items:
        for j, v in enumerate(it): put(st, (r, 1 + j), v, f_norm, align=wrap)
        st.row_dimensions[r].height = 92; r += 1
    widths(st, {"A": 44, "B": 48, "C": 52, "D": 52})

    # ---------------- Next_Steps ----------------
    ns = wb.create_sheet("Next_Steps")
    title(ns, "Next steps — data to pull and checks to run", "Confirm every field mnemonic with FLDS <GO> before relying on it; syntax below is the standard Excel add-in form.")
    hdr(ns, 4, ["Task", "Bloomberg route", "Why / feeds which RQ"], height=24)
    tasks = [
     ("Daily prices, 5–10 years: WIL SP, NESN SW, ULVR LN, palm oil continuous", 'Excel add-in: =BDH("WIL SP Equity","PX_LAST","10/15/2021","10/15/2026","Dir=V","Days=A") — repeat per ticker; palm oil: generic first-month KO1 Comdty (confirm)', "RQ2: volatility, correlation, beta with n in the thousands; event studies"),
     ("Event study around 28-May-2026 (Indonesia export probe) and 03-Mar-2026 (bribery sentence)", "Daily returns of WIL SP vs STI Index; abnormal return = actual − beta × market; cumulative over [-1,+5] days", "Calibrates rev_loss / p_reg with an observed event instead of a guess"),
     ("Full SPLC supplier / customer lists; search for Wilmar, IOI, Musim Mas, AAK, Cargill, Sime Darby Plantation", "SPLC <GO> → Suppliers/Customers → export; use the Export button to Excel", "RQ1: tests the 'mill → trader → brand owner' chain"),
     ("Same-query news screen for all firms", "CN <GO>: company AND (palm oil OR deforestation OR supply chain) with ESG/controversy tags; export counts by month", "Makes the news indicator comparable"),
     ("Scope 3 and certification coverage (% RSPO / % traceable to mill)", "ESG <GO> tabs + company sustainability reports (Unilever, Nestlé, Wilmar)", "Replace assumed c0 and ps with disclosed values"),
     ("FX and WACC", "EURUSD Curncy, USDCHF Curncy; WACC <GO>", "Replace illustrative FX and the 8% discount rate"),
     ("Extend the peer set to 10–15 firms", "Add IOI, Musim Mas (if covered), AAK, Cargill (private; use disclosures), P&G, Mondelez, Colgate, Sime Darby Plantation", "Gives the risk index and any regression real degrees of freedom"),
     ("Spot-check transcription", "Re-read ~10 numbers per sheet against the Terminal (revenue, BESG, Scope 3, SPLC counts, 10 prices)", "These values were typed from screenshots"),
    ]
    for i, t in enumerate(tasks):
        for j, v in enumerate(t): put(ns, (5 + i, 1 + j), v, f_norm, align=wrap)
        ns.row_dimensions[5 + i].height = 58
    r = 5 + len(tasks) + 1
    sec(ns, r, "Source used in this review", 3)
    put(ns, (r + 1, 1), "European Commission, Access2Markets: 'Delay until December 2026 and other developments in the implementation of the EUDR Regulation'", f_norm, border=False)
    put(ns, (r + 2, 1), "https://trade.ec.europa.eu/access-to-markets/en/news/delay-until-december-2026-and-other-developments-implementation-eudr-regulation", f_sub, border=False)
    widths(ns, {"A": 60, "B": 80, "C": 60})
    # order
    order = ["Start_Here", "Summary", "Assumptions", "ROI_ULVR", "ROI_NESN", "ROI_WIL", "MC_Results", "Sensitivity", "Risk_Index", "Supply_Chain",
             "News_Events", "ESG", "Fundamentals", "Market_Data", "Price_Analytics", "Next_Steps"]
    wb._sheets = [wb[n] for n in order]
    wb.active = 0
