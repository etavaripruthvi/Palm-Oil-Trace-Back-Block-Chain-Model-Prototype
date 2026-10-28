from lib import *

def build(doc):
    h1(doc, "Chapter 7  Conclusion")
    h2(doc, "7.1  Summary of findings")
    para(doc, "Table 7.1 restates what the evidence says about each research question, with an honest confidence rating.", after=4)
    table_cap(doc, 7, "Answers to the research questions")
    table(doc, ["RQ", "Answer", "Confidence"], [
        ["RQ1  Which Bloomberg-derived indicators best explain or predict traceability risk?", "Among observable indicators, the ones that separate the firms most are **financial resilience (interest cover), supplier conduct flags, adverse news and Scope 3 intensity**. ESG *disclosure* scores point the wrong way: Wilmar has the highest BESG score and the highest SPOEI. Predictive power is untested (no labelled panel).", "Medium for the index drivers; **none** for prediction"],
        ["RQ2  How do ESG, supply links, palm prices and news interact under normal and stressed conditions?", "Visibility is the common thread: SPLC sees none of the palm chain, so ESG and news are the only signals. Price links cannot be established on eight weeks of data (|ρ| < 0.34 band). Under stress (Severe: enforcement ×4, controversy ×2.5, palm +30%) untraced losses rise roughly three- to three-and-a-half-fold and the ledger overtakes the database.", "Medium (descriptive); low for price links"],
        ["RQ3  Does the predictive model beat a simple benchmark?", "**Not answered.** The model, benchmarks, success rule and sample-size requirement (≈ 85 observations, ≥ 17 events) are specified and the code is ready; the data are not yet held.", "Open"],
        ["RQ4  Which intervention gives the best risk–cost trade-off?", "Traceability pays for all three firms in every scenario. A **database-first, ledger-ready** path has the best balance of expected value and downside; the blockchain adds value under adverse/severe enforcement, at lower cost (3–11%), or at assurance above 0.82–0.96.", "Medium, conditional on ASSUMPTIONS"],
    ], [4.2, 9.2, 3.0], 8.3, ["l", "l", "l"], bold_first_col=True, highlight={2: "FFF9C4"})
    para(doc, "Three messages matter most to a manager. First, **the visibility gap is the risk**: for the brand owners the palm chain is invisible to Bloomberg, and for Wilmar the visible plantation nodes are 0.4% of the cost base. Second, **the largest value comes from traceability itself**, not from the ledger; the blockchain’s premium over a database is a close call that tips only under stress or with cost reductions. Third, **ESG scores are not a substitute for verification**: they measured disclosure, and a sourcing rule built on them would have missed Wilmar’s real risks.")
    h2(doc, "7.2  Limitations of the study")
    h3(doc, "Data")
    bullets(doc, [
        "**Tier-2 and Tier-3 are invisible.** Private mills and smallholder farms are not listed on Bloomberg. SPLC shows Tier-1 relationships only, and the rows we captured (24 suppliers per firm) are lower bounds.",
        "**Screens, not an API.** Values were transcribed from Terminal screens on one date (15 October 2026) and spot-checked, not pulled by script; transcription errors are possible. Unilever FY2024–25 are restated for the ice-cream demerger and its Scope 3 series has breaks.",
        "**Short price window.** Eight weeks of daily prices cannot establish price–equity or price–margin links; a multi-year KO1 series is required.",
        "**News coding is hand-made and unequal.** Severity was coded by the authors from headlines, and search filters differ by firm; no Bloomberg sentiment series was available.",
        "**Currencies and FX.** Revenues are converted at illustrative rates (EUR 1.15, CHF 1.25 per USD).",
    ], 10, False, 2)
    h3(doc, "Method")
    bullets(doc, [
        "**SPOEI is a screening index.** Floors, caps and weights are judgement-based, only three firms are scored, and the index has not been validated against outcomes.",
        "**No classifier results.** RQ3 and SHAP-based importance remain open until a labelled panel of at least ≈ 85 firm-periods is available.",
        "**Monte Carlo assumptions.** Probabilities, fines, premia, coverage, effectiveness and programme costs are ASSUMPTIONS; inputs are drawn independently except through the regime mix, which understates correlation between enforcement, controversy and price. Only losses avoided are valued: not financing benefits, price premia for certified product, or the option value of market access.",
        "**Oracle risk is a parameter.** Data-integrity failures at the source enter only through the effectiveness values; consortium failure, cyber-risk and regulatory acceptance of ledger evidence are not modelled.",
        "**A moving regulation.** The EUDR’s scope, simplification and benchmarking are still changing; the dates and penalties in Chapter 1 reflect the Commission’s position as read in July 2026.",
    ], 10, False, 2)
    h2(doc, "7.3  Future outlook")
    para(doc, "Over the next five years we expect the framework in Chapter 5 to be strengthened rather than replaced, by two technologies, and we flag what could go wrong. These are projections, not forecasts.")
    bullets(doc, [
        "**Generative AI as the reading layer.** Language models can read mill lists, land-title scans, audit reports and CN headlines, extract plot and lot records into the ledger’s schema, summarise supplier risk for the SPOEI, and draft due-diligence statements for human review. The caution is that a model can be wrong with confidence: every AI-extracted record should carry a source link and a human sign-off before it becomes a ledger event.",
        "**IoT and remote sensing as the data layer.** Weighbridge scales, RFID/QR lot tags, GPS-tagged trucks and combined optical and radar satellites reduce the oracle problem by providing independent, frequent measurements, and radar sees through cloud cover. They also lower the cost of verification per tonne, which is the parameter to which Chapter 5’s results are most sensitive.",
        "**Interoperability and digital product passports.** The value of a consortium ledger grows with the number of participants; open data standards and links to EU information systems would reduce migration cost, which is the practical condition for the staged path recommended here.",
        "**Risks.** Poisoned or spoofed sensor data, concentration of satellite providers, energy and cost of consortium infrastructure, and unequal access for smallholders, who may be excluded by cost unless mills and buyers co-fund onboarding.",
    ], 10, False, 3)
    para(doc, "**Next steps for the research.** (1) Pull the Terminal panel specified in Appendix A.3 and estimate the classifier; (2) locate Wilmar, IOI, Musim Mas, AAK and Cargill in the full SPLC lists; (3) replace ASSUMPTION inputs with firm WACC, Bloomberg FX and company disclosures; (4) extend the news coding with a consistent filter and a Bloomberg sentiment series; (5) backtest rules R1–R7.", 10.5, 6)
