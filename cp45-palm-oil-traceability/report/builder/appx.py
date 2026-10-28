from lib import *
import re
MODEL = (ROOT / "src" / "palm_oil_traceability_model.py").read_text()

def split_code(text, n=62):
    lines = text.rstrip("\n").split("\n"); return ["\n".join(lines[i:i + n]) for i in range(0, len(lines), n)]

def build(doc):
    h1(doc, "Appendix A  Bloomberg Data Capture and Query Scripts")
    para(doc, "**What was actually run.** The Bloomberg data in this report were captured from Terminal screens on 15 October 2026 at the Woxsen Bloomberg Lab (the function, security and fields are logged in Table A.1). **No BQL or BDH script was executed for this report.** The queries in A.2 reproduce the same fields programmatically and extend them to the 10-year panel the classifier needs; they have not been run and each field mnemonic must be confirmed on the Terminal with FLDS <GO> before use (mnemonics can differ by entitlement).", 10.5, 6)
    h2(doc, "A.1  Capture log (screens used)")
    table_cap(doc, "A", "Screens captured on 15-Oct-2026")
    table(doc, ["Function", "Security / filter", "Content captured", "Used in"], [
        ["SPLC <GO>", "WIL SP, NESN SW, ULVR LN Equity", "Supplier and customer counts; ESG/sanction/distress flags; geography; commodity exposures; top-24 suppliers by cost share (name, % supplier revenue, % cost, type, 3M price change); top-10 customers", "Ch. 3.1, 4.1"],
        ["FA <GO>", "Same three; annual FY2019–FY2025", "Income statement, balance sheet and cash-flow lines: revenue, COGS, operating income, interest expense, inventory, cash, receivables, PP&E, goodwill, net income, D&A, CFO, capex, dividends", "Ch. 3.2, 4.1, 5"],
        ["ESG <GO>", "Same three; 2016–2025", "BESG overall and E/S/G pillar scores; Scope 1, 2 and 3 emissions", "Ch. 3.3, 4.1"],
        ["CN <GO>", "“Wilmar + Palm Oil”, “Wilmar + ESG”, “Nestlé + Palm Oil”, “Unilever + ESG”, “Unilever + Palm Oil + deforestation”", "Headline, date and category of 22 stories; hand-coded sentiment and severity", "Ch. 3.3, 4.1"],
        ["HP / GP <GO>", "KOZ6 Comdty; WIL SP, NESN SW, ULVR LN; 17-Aug to 15-Oct-2026 daily; equities 5-year table", "Daily closes; 5-year high, low, average, net change", "Ch. 3.2, 5"],
        ["DES <GO>", "Same three equities", "Market cap, P/E, estimates, dividend yield, beta, employees, 52-week range, 12M total return, 30/90-day volatility", "Ch. 1.4, 4.1"],
    ], [2.2, 4.4, 7.2, 2.6], 8, ["l", "l", "l", "l"], bold_first_col=True)
    note(doc, "All captured values are in the workbook sheets Supply_Chain, Fundamentals, ESG, News_Events and Market_Data. Rows visible on screen only; SPLC lists hold more records.")
    h2(doc, "A.2  Reproduction and extension queries (templates, not executed)")
    para(doc, "Excel add-in (BDH) templates. Replace the placeholders marked <…> after looking up the exact mnemonic with FLDS <GO>.", after=3)
    code(doc, """' --- 10-year monthly palm oil and equity prices (needed for Ch. 3.2 overlay and the panel's X4 feature) ---
=BDH("KO1 Comdty",       "PX_LAST", "2016-10-15", "2026-10-15", "Per=M", "Fill=P")
=BDH("WIL SP Equity",    "PX_LAST", "2016-10-15", "2026-10-15", "Per=M", "Currency=SGD")
=BDH("NESN SW Equity",   "PX_LAST", "2016-10-15", "2026-10-15", "Per=M", "Currency=CHF")
=BDH("ULVR LN Equity",   "PX_LAST", "2016-10-15", "2026-10-15", "Per=M", "Currency=GBP")
=BDH("WIL SP Equity",    "VOLATILITY_90D", "2016-10-15", "2026-10-15", "Per=M")

' --- annual fundamentals, FY2016-FY2025 (reporting currency) ---
=BDH("WIL SP Equity",  "SALES_REV_TURN,GROSS_PROFIT,IS_OPER_INC,IS_INT_EXPENSE,BS_INVENTORIES,CF_CASH_FROM_OPER,CF_CAP_EXPEND_PRPTY_ADD",
                       "2016-12-31", "2025-12-31", "Per=FY", "Fill=P")
' repeat for NESN SW Equity and ULVR LN Equity

' --- ESG: confirm each mnemonic in FLDS <GO> (search "BESG", "scope 3") ---
=BDH("WIL SP Equity",  "BESG_ESG_SCORE,BESG_ENVIRONMENTAL_PILLAR_SCORE,BESG_SOCIAL_PILLAR_SCORE,BESG_GOVERNANCE_PILLAR_SCORE",
                       "2016-12-31", "2025-12-31", "Per=FY")
=BDH("WIL SP Equity",  "<FIELD_SCOPE_1>,<FIELD_SCOPE_2>,<FIELD_SCOPE_3>", "2016-12-31", "2025-12-31", "Per=FY")
""", 7)
    code(doc, """# --- BQL template (Bloomberg Query Language; run in BQuant or the Excel BQL function) ---
get(px_last(dates=range(-10Y, 0D), frq=M))  for(['KO1 Comdty'])
get(sales_rev_turn(fpt=A, fpr=range(-9Y, 0Y)))  for(['WIL SP Equity', 'NESN SW Equity', 'ULVR LN Equity'])

# --- SPLC: use the screen (SPLC <GO> > Suppliers > Export to Excel); keep one export per firm and per date.
# --- CN: CN <GO>, filter by company and keywords; export headline, date, source; code severity 1-5 with a written rubric.
""", 7)
    h2(doc, "A.3  Panel file for the classifier (spoei_panel.csv)")
    table_cap(doc, "A", "Panel columns read by notebook Part 5")
    table(doc, ["Column", "Definition", "Source"], [
        ["firm_id, month", "Issuer identifier; month-end (YYYY-MM), 2016-01 to 2026-09", "—"],
        ["X1_hhi", "HHI of the issuer’s supplier cost shares (SPLC snapshot, history where available)", "SPLC"],
        ["X2_env_gap, X2_env_gap_chg12", "10 − BESG environmental pillar; 12-month change", "ESG"],
        ["X3_news_z, X3_news_vol", "Trailing 90-day z-score and volatility of Bloomberg news sentiment for the issuer", "CN / sentiment"],
        ["X4_cpo_var_x_exposure", "Variance of KO1 returns (trailing 90 days) × the issuer’s palm-linked spend share", "GP + company data"],
        ["X5_int_cover, X6_flag_share, X7_eq_vol", "Operating income / interest; share of suppliers with Bloomberg flags; 90-day equity volatility", "FA, SPLC, DES"],
        ["Y_event_12m", "1 if, in months t+1 to t+12, an RSPO complaint or sanction, a new ESG controversy flag, or a CN headline on deforestation / RSPO / EUDR / NDPE with severity ≥ 3. At least one source outside the feature set", "RSPO complaints record; CN; ESG"],
    ], [4.5, 9.0, 2.9], 8, ["l", "l", "l"], bold_first_col=True)

    h1(doc, "Appendix B  Python Simulation Code")
    para(doc, "The listing reproduces the core engine of the companion file palm_oil_traceability_model.py: global parameters, scenario multipliers, firm profiles, the present-value engine, the deterministic scenario function and the Monte Carlo. The market-data tables, the tornado, the coverage-exclusion grid and the notebook (including the classifier in Part 5) are in the companion files. Seed 42; 20,000 simulations.", 10.5, 6)
    a = MODEL.index("# 2. COST-BENEFIT MODEL INPUTS"); a = MODEL.rfind("# ----", 0, a); b = MODEL.index("# 5. SENSITIVITY"); b = MODEL.rfind("# ----", 0, b)
    core = MODEL[a:b]
    h2(doc, "B.1  Cost-benefit and Monte Carlo engine")
    for chunk in split_code(core, 60): code(doc, chunk, 6.6)
    h2(doc, "B.2  Classifier protocol (notebook Part 5, core functions)")
    nb = (ROOT / "notebooks" / "CP45_Palm_Oil_Traceability_Notebook.ipynb").read_text()
    import json
    cells = json.loads(nb)["cells"]; src = "".join(cells[14]["source"]) if False else None
    ml = [ "".join(c["source"]) for c in cells if c["cell_type"] == "code" and "def delong_p" in "".join(c["source"]) ][0]
    s0 = ml.index("def blocks():"); s1 = ml.index("results, store = [], {}")
    for chunk in split_code(ml[s0:s1], 60): code(doc, chunk, 6.6)

def references(doc):
    h1(doc, "References")
    refs = [
        "Akerlof, G. A. (1970). The market for ‘lemons’: Quality uncertainty and the market mechanism. *The Quarterly Journal of Economics*, 84(3), 488–500.",
        "Austin, K. G., Schwantes, A., Gu, Y., & Kasibhatla, P. S. (2017). Shifting patterns of oil palm driven deforestation in Indonesia and implications for zero-deforestation commitments. *Land Use Policy*, 69, 41–48.",
        "Babich, V., & Hilary, G. (2020). Distributed ledgers and operations: What operations management researchers should know about blockchain technology. *Manufacturing & Service Operations Management*, 22(2), 223–240.",
        "Bloomberg L.P. (2026). *Supply Chain (SPLC), Financial Analysis (FA), ESG, Company News (CN), Historical Price (HP/GP) and Description (DES) functions, Bloomberg Terminal*, Woxsen Bloomberg Lab, captured 15 October 2026. Product overview: https://professional.bloomberg.com/institutions/corporations/supply-chain/",
        "Breiman, L. (2001). Random forests. *Machine Learning*, 45(1), 5–32.",
        "Caldarelli, G. (2020). Understanding the blockchain oracle problem: A call for action. *Information*, 11(11), 509.",
        "Carlson, K. M., Heilmayr, R., Gibbs, H. K., et al. (2018). Effect of oil palm sustainability certification on deforestation and fire in Indonesia. *Proceedings of the National Academy of Sciences*, 115(1), 121–126.",
        "Cerqueira, V., Torgo, L., & Mozetič, I. (2020). Evaluating time series forecasting models: An empirical study on performance estimation methods. *Machine Learning*, 109, 1997–2028.",
        "Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining*, 785–794.",
        "Chod, J., Trichakis, N., Tsoukalas, G., Aspegren, H., & Weber, M. (2020). On the financing benefits of supply chain transparency and blockchain adoption. *Management Science*, 66(10), 4378–4396.",
        "Christopher, M., & Peck, H. (2004). Building the resilient supply chain. *The International Journal of Logistics Management*, 15(2), 1–14.",
        "Cole, R., Stevenson, M., & Aitken, J. (2019). Blockchain technology: Implications for operations and supply chain management. *Supply Chain Management: An International Journal*, 24(4), 469–483.",
        "DeLong, E. R., DeLong, D. M., & Clarke-Pearson, D. L. (1988). Comparing the areas under two or more correlated receiver operating characteristic curves: A nonparametric approach. *Biometrics*, 44(3), 837–845.",
        "European Commission (2026, 13 July). *Commission updates product scope and tools to support EUDR*. Directorate-General for Environment. https://environment.ec.europa.eu/news/commission-updates-product-scope-and-tools-support-eudr-2026-07-13_en",
        "Gaveau, D. L. A., Locatelli, B., Salim, M. A., et al. (2022). Slowing deforestation in Indonesia follows declining oil palm expansion and lower oil prices. *PLOS ONE*, 17(3), e0266178.",
        "Greenhouse Gas Protocol (2011). *Corporate Value Chain (Scope 3) Accounting and Reporting Standard*. World Resources Institute and World Business Council for Sustainable Development.",
        "Hanley, J. A., & McNeil, B. J. (1982). The meaning and use of the area under a receiver operating characteristic (ROC) curve. *Radiology*, 143(1), 29–36.",
        "Hogan Lovells (2026, 15 May). *EU Deforestation Regulation: Commission publishes simplification package ahead of December 2026 application date*. https://www.hlc.com/en/publications/eu-deforestation-regulation-commission-publishes-simplification-package-ahead-of-december-2026",
        "Kamilaris, A., Fonts, A., & Prenafeta-Boldú, F. X. (2019). The rise of blockchain technology in agriculture and food supply chains. *Trends in Food Science & Technology*, 91, 640–652.",
        "Kaufman, S., Rosset, S., & Perlich, C. (2012). Leakage in data mining: Formulation, detection, and avoidance. *ACM Transactions on Knowledge Discovery from Data*, 6(4), Article 15.",
        "Kshetri, N. (2018). 1 Blockchain’s roles in meeting key supply chain management objectives. *International Journal of Information Management*, 39, 80–89.",
        "Lambin, E. F., Gibbs, H. K., Heilmayr, R., et al. (2018). The role of supply-chain initiatives in reducing deforestation. *Nature Climate Change*, 8, 109–116.",
        "Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30.",
        "Nakamoto, S. (2008). *Bitcoin: A peer-to-peer electronic cash system*. https://bitcoin.org/bitcoin.pdf",
        "Regulation (EU) 2023/1115 of the European Parliament and of the Council of 31 May 2023 on the making available on the Union market and the export from the Union of certain commodities and products associated with deforestation and forest degradation and repealing Regulation (EU) No 995/2010. *Official Journal of the European Union*, L 150, 9.6.2023. https://eur-lex.europa.eu/eli/reg/2023/1115/oj/eng",
        "Roundtable on Sustainable Palm Oil (2017). *RSPO Supply Chain Certification Standard* (v1.1, June 2017). https://rspo.org/wp-content/uploads/rspo-std-t05-001-v1.1-eng_scc-standard-june-2017_.pdf",
        "Saberi, S., Kouhizadeh, M., Sarkis, J., & Shen, L. (2019). Blockchain technology and its relationships to sustainable supply chain management. *International Journal of Production Research*, 57(7), 2117–2135.",
        "Sheffi, Y., & Rice, J. B. (2005). A supply chain view of the resilient enterprise. *MIT Sloan Management Review*, 47(1), 41–48.",
        "Unilever PLC, Nestlé S.A. and Wilmar International Ltd: annual and sustainability reports and investor-relations disclosures, FY2025. Data used in this report were taken from Bloomberg FA/ESG; original filings were not re-examined. https://www.unilever.com/investors/",
        "Williamson, O. E. (1979). Transaction-cost economics: The governance of contractual relations. *The Journal of Law and Economics*, 22(2), 233–261.",
        "Williamson, O. E. (1985). *The Economic Institutions of Capitalism*. Free Press.",
        "World Bank (2026). *Commodity Markets*. https://www.worldbank.org/en/research/commodity-markets (benchmark source named in the project brief; not used for figures).",
    ]
    for r in refs:
        p = doc.add_paragraph(); runs(p, r, 9.2); pfmt(p, 0, 4, 1.08, False, WD_ALIGN_PARAGRAPH.LEFT, 0.7, -0.7)
