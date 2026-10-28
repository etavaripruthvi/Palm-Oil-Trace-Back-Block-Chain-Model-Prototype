from lib import *
import sys, json
import wb_a, wb_b1, wb_b2, pandas as pd, numpy as np
N = J("nums.json")
SRC = "Source: Bloomberg SPLC, 15-Oct-2026 (captured rows only); authors’ calculations."

def pct(x, d=1): return f"{x*100:.{d}f}%"

def build(doc):
    h1(doc, "Chapter 3  Bloomberg Supply Chain Mapping and Baseline Diagnostics")
    para(doc, "This chapter sets the empirical baseline. It asks how much of each firm’s supply chain Bloomberg can see (3.1), how exposed profitability has been to commodity-driven margin pressure (3.2), and how ESG scores, emissions and news flow describe reputational risk (3.3). Every figure is traceable to a sheet in the companion workbook.", 10.5, 6)
    h2(doc, "3.1  Network topology using SPLC")
    h3(doc, "What SPLC shows")
    para(doc, "SPLC lists 508 suppliers and 172 customers for Nestlé, 287 and 126 for Unilever, but only 30 suppliers and 17 customers for Wilmar. We captured the top 24 suppliers by cost share for each firm from the screens, so all coverage figures below are **lower bounds** on what SPLC holds. Table 3.1 summarises the network panels.")
    table_cap(doc, 3, "SPLC network panels (suppliers and customers listed by Bloomberg)")
    table(doc, ["Metric", "Unilever", "Nestlé", "Wilmar"], [
        ["Suppliers listed (count)", "287", "508", "30"], ["Customers listed (count)", "126", "172", "17"],
        ["Suppliers with business-conduct risk flag", "40 (13.9%)", "54 (10.6%)", "11 (36.7%)"],
        ["Suppliers with high GHG intensity vs peers", "59 (20.6%)", "99 (19.5%)", "4 (13.3%)"],
        ["Suppliers that are ESG-score laggards", "13 (4.5%)", "21 (4.1%)", "1 (3.3%)"],
        ["Suppliers sanctioned or distressed", "5 (1.7%)", "15 (3.0%)", "1 (3.3%)"],
        ["Suppliers with high water stress", "72 (25.1%)", "71 (14.0%)", "5 (16.7%)"],
    ], [7.2, 3.1, 3.1, 3.0], 8.5, ["l", "c", "c", "c"])
    note(doc, SRC + " Percentages are of listed suppliers. Sanctioned-or-distressed combines the two SPLC counters (Unilever 1 + 4; Nestlé 2 + 13; Wilmar 1 + 0).")
    figure(doc, 3, "f05_splc_visibility.png", "How much of the supply base is visible, and what the visible part looks like", SRC)
    h3(doc, "Finding 1 — the palm chain is invisible to SPLC")
    para(doc, "The 24 captured Unilever suppliers account for 16.6% of Unilever’s cost base and the 24 captured Nestlé suppliers for 12.9% (Figure 3.1); they are dominated by packaging (49% of Nestlé’s visible cost, 19% of Unilever’s), flavours and ingredients, technology and logistics. **None is a palm trader, refiner or plantation. Wilmar appears in neither list, and neither Unilever nor Nestlé appears among Wilmar’s visible customers.** The chain “mill → Wilmar → Unilever/Nestlé” that motivates the project is therefore an industry fact, not an SPLC finding. Nestlé’s own news flow points to other palm partners: in July 2025 Bloomberg reported that Musim Mas, Nestlé and AAK renewed a palm partnership on environmental and social issues.")
    para(doc, "For Wilmar, the 24 captured suppliers account for only 2.7% of Wilmar’s cost base (COGS plus SG&A). Ten are palm or plantation nodes, together just **0.4% of the cost base**, although palm products dominate Wilmar’s business. Most palm is bought from third-party mills and smallholders that SPLC does not cover. **This gap, not any single supplier, is the traceability problem.**")
    h3(doc, "Finding 2 — what Wilmar’s visible suppliers say about leverage")
    para(doc, "Figure 3.2 plots Wilmar’s visible suppliers (listed in Table 3.2) by their weight in Wilmar’s costs (criticality to Wilmar) and by Wilmar’s weight in *their* revenue (Wilmar’s leverage over them). Plantation suppliers such as Andira Agro (99% of revenue from Wilmar), Gozco (47%) and AEP Pinago (39%) are tiny in Wilmar’s cost base but depend heavily on Wilmar. Weighted by cost, Wilmar supplies **27% of the revenue of its visible palm nodes**. In TCE terms (Chapter 2), the buyer holds the bargaining power: Wilmar can require geolocation and audit access from these suppliers at low cost to itself. The squares are group companies or joint ventures (Yihai Kerry Arawana, Wilmar Cahaya Indonesia, AWL Agri); these relationships are flagged from company names and should be verified.")
    figure(doc, 3, "f14_leverage.png", "Wilmar’s visible suppliers: criticality to Wilmar versus Wilmar’s leverage over the supplier", SRC + " Palm and related-party flags are the authors’ judgement from company names.")
    table_cap(doc, 3, "Wilmar’s largest visible suppliers (SPLC, top 12 of 24 captured)")
    rows = []
    for name, rev, cost, typ, chg, palm, rel in wb_b1.WSUP[:12]:
        rows.append([name, pct(cost, 2), pct(rev, 1), typ, "Yes" if palm == "Y" else "No", "Yes" if rel == "Y" else "No"])
    table(doc, ["Supplier", "Share of Wilmar cost", "Wilmar share of supplier revenue", "Cost type", "Palm / plantation node", "Related party (verify)"], rows, [5.6, 2.1, 2.9, 1.7, 2.2, 1.9], 8, ["l", "c", "c", "c", "c", "c"])
    note(doc, SRC)
    h3(doc, "Concentration and the Wilmar-to-brand-owner link")
    para(doc, "Concentration among the visible suppliers is moderate. The Herfindahl–Hirschman Index (HHI, sum of squared cost shares ×10,000, computed on the visible rows only) is 781 for Nestlé, 1,456 for Unilever and 1,331 for Wilmar (excluding related parties; the top three unrelated suppliers hold 54% of Wilmar’s visible cost). These are *within-sample* measures and say little about the true concentration of the palm base.")
    para(doc, "The brief asks for “Supplier Revenue Exposure %” and “COGS Reliance %” for Wilmar as a supplier to Unilever and Nestlé. SPLC does not show this link, so we bound it. Using the palm-spend shares assumed in Chapter 5 (3.0% of Unilever’s COGS and 1.5% of Nestlé’s; ASSUMPTION), annual palm purchases would be about USD 0.9 bn for Unilever and USD 0.9 bn for Nestlé. Even if every tonne came from Wilmar, that is at most **about 1.3% of Wilmar’s revenue per brand owner**, while for each brand owner palm oil is a small share of COGS. The relationship is therefore important for compliance and reputation but not for the brand owner’s cost structure or for Wilmar’s revenue. That is why Chapter 5 values traceability by avoided regulatory, reputational and substitution loss rather than by input-cost savings.")
    callout(doc, "To complete from the Terminal (not available from the captured screens)", "Search the full SPLC supplier lists of Unilever and Nestlé for Wilmar, IOI, Musim Mas, AAK and Cargill (SPLC <GO>, enter the company, Suppliers tab, search box). If found, insert the Supplier Revenue Exposure % and Cost % into the placeholder rows of the workbook sheet Supply_Chain and replace the bounds above. Add each brand owner’s published mill list as a second source.", "todo")

    h2(doc, "3.2  Financial health and margin analysis")
    para(doc, "Annual statements (Bloomberg FA) for FY2019–FY2025 show very different margin structures (Figure 3.3). Unilever and Nestlé earn gross margins of 46–47% and operating margins of 16–20%; Wilmar, a processor and merchant, earns 8% and 3%. For the brand owners, palm oil is a small part of COGS, so margins respond mainly to the broader mix of inputs, pricing and portfolio changes. Unilever’s FY2024–25 figures are restated after the ice-cream demerger and are not strictly comparable with earlier years.")
    figure(doc, 3, "f01_margins.png", "Gross and operating margins, FY2019–FY2025", "Source: Bloomberg FA, 15-Oct-2026; authors’ calculations (gross margin = (revenue − COGS)/revenue).")
    g = lambda k, i: N[f"gm_{k}"][i]; o = lambda k, i: N[f"om_{k}"][i]
    rows = []
    for k, nm in (("ULVR", "Unilever"), ("NESN", "Nestlé"), ("WIL", "Wilmar")):
        gm, om = np.array(N[f"gm_{k}"]), np.array(N[f"om_{k}"])
        rows.append([nm, f"{gm[0]:.1f} → {gm[-1]:.1f}", f"{gm[-1]-gm[0]:+.1f}", f"{gm.min():.1f}–{gm.max():.1f}", f"{om[0]:.1f} → {om[-1]:.1f}", f"{om[-1]-om[0]:+.1f}", f"{N['cov_'+k][-1]:.1f}×", f"{N['dio_'+k][-1]:.0f}"])
    table_cap(doc, 3, "Margin and resilience diagnostics, FY2019 → FY2025")
    table(doc, ["Firm", "Gross margin %\nFY19 → FY25", "Change (pp)", "Gross margin range", "Operating margin %\nFY19 → FY25", "Change (pp)", "Interest cover FY25", "Inventory days FY25"], rows, [2.0, 2.5, 1.5, 2.2, 2.6, 1.5, 2.1, 2.0], 8, ["l"] + ["c"] * 7)
    note(doc, "Source: Bloomberg FA; authors’ calculations. Inventory days = inventory / COGS × 365.")
    para(doc, "Three patterns stand out (Table 3.3). **(i) Wilmar’s gross margin compressed** from 10.9% in FY2021 to 7.7% in FY2024 while revenue grew by about 65% from FY2019 to FY2025 (USD 42.6 bn to 70.4 bn), consistent with commodity price inflation lifting sales faster than spread. **(ii) Nestlé’s operating margin fell** to 15.5% in FY2025, its lowest in the window, and Nestlé holds the most inventory (96 days). **(iii) Interest cover has fallen at both brand owners**, from 13.0× to 9.1× (Unilever) and from 14.3× to 8.3× (Nestlé), while Wilmar is back where it started (2.0× in FY2019, 2.1× in FY2025) after peaking at 4.6× in FY2021. Thin cover is what makes Wilmar fragile: a fine or a forced supplier substitution is a larger share of its earnings than of Unilever’s or Nestlé’s.")
    h3(doc, "Palm oil price overlay")
    para(doc, "Figure 3.4 shows the Dec-2026 Bursa Malaysia crude palm oil contract (KOZ6 Comdty) and the three equities over the eight weeks captured on 15 October. KOZ6 rose to MYR 5,115 per tonne on 8 September and then fell 9% to MYR 4,666. Over the 33–36 return pairs that align with each equity, correlations with palm oil returns are 0.18 (Unilever), 0.23 (Nestlé) and −0.08 (Wilmar). With this sample a correlation must exceed about ±0.34 to be distinguishable from zero at the 5% level, so **none of the three is statistically significant** and we make no claim about price pass-through from these data (RQ2). Annualised volatility is 17% for palm oil, 18% for Unilever, 18% for Nestlé and 19% for Wilmar.")
    figure(doc, 3, "f02_cpo_equities.png", "Crude palm oil (KOZ6) and equity prices, 17 August – 15 October 2026", "Source: Bloomberg HP / GP tables, 15-Oct-2026. KOZ6 is the Dec-2026 contract; a continuous series (KO1) is needed for multi-year work.")
    callout(doc, "Multi-year overlay still to be added from the Terminal", "The brief asks for 5–10 years of palm oil prices overlaid on margins. The screens we captured cover eight weeks of daily prices. Pull KO1 Comdty (monthly, 2016–2026) with the BDH query in Appendix A.2, then re-run Section 4 of the notebook; the margin table above is already annual and needs no change. The correlation test above should be repeated on monthly returns (≈120 observations).", "todo")

    h2(doc, "3.3  ESG and controversy profiling")
    para(doc, "Bloomberg’s ESG disclosure score (BESG, 0–10) rises for all three firms over 2016–2024, most steeply for Wilmar (2.71 to 6.15; Figure 3.5 and Table 3.4). Reported Scope 1 emissions tell a different story: Wilmar’s rose 2.6× (3,551 to 9,100 kt CO₂e) while Unilever’s halved and Nestlé’s fell 22%. **The score tracks disclosure, not footprint.** A firm that discloses more earns a higher score even when its emissions grow. The correlation between Wilmar’s BESG score and its gross margin over 2019–2024 is −0.76, but with six observations it is not significant (p = 0.08) and reflects two trends moving in opposite directions, not a causal link.")
    figure(doc, 3, "f03_besg_scope1.png", "ESG disclosure score and Scope 1 emissions, 2016–2025", "Source: Bloomberg ESG, 15-Oct-2026; authors’ calculations. Scope 1 indexed to 2016 = 100 (Wilmar 3,551 kt → 9,100 kt).")
    E = wb_a.ESG
    rows = []
    for k, nm in (("ULVR", "Unilever"), ("NESN", "Nestlé"), ("WIL", "Wilmar")):
        i24 = 8
        rows.append([nm, f"{E[k]['besg'][i24]:.2f}", f"{E[k]['env'][i24]:.2f}", f"{E[k]['soc'][i24]:.2f}", f"{E[k]['gov'][i24]:.2f}", f"{E[k]['besg'][i24]-E[k]['besg'][3]:+.2f}", f"{E[k]['s1'][9]/1000:.1f}", f"{[v for v in E[k]['s3'] if v][-1]/1000:.0f}"])
    table_cap(doc, 3, "Bloomberg ESG snapshot, 2024 (BESG pillars 0–10)")
    table(doc, ["Firm", "BESG overall", "Environmental", "Social", "Governance", "Change in BESG 2019→24", "Scope 1, 2025 (Mt)", "Scope 3, latest (Mt)"], rows, [2.0, 1.9, 2.3, 1.7, 2.1, 2.5, 1.9, 2.0], 8, ["l"] + ["c"] * 7)
    note(doc, "Source: Bloomberg ESG. Wilmar’s latest Scope 3 is 2024 (147 Mt); Unilever and Nestlé 2025. Unilever’s Scope 3 series has boundary breaks in 2020 and 2022.")
    figure(doc, 3, "f04_scope3.png", "Reported Scope 3 emissions and 2024 intensity", "Source: Bloomberg ESG; intensity = Scope 3 (kt CO₂e) / revenue (USD bn), 2024; authors’ calculations.")
    para(doc, "In Figure 3.6, Scope 3 intensity per dollar of revenue is highest at Wilmar (2,182 kt per USD bn), then Unilever (1,789) and Nestlé (593). The Unilever and Wilmar figures are not directly comparable with Nestlé’s because they depend on different Scope 3 boundaries and methods; we use intensity only as an indicator in the SPOEI (Chapter 4), capped so that one boundary change cannot dominate the score.")
    h3(doc, "News and controversy")
    news = [r for r in wb_b2.NEWS if r[0] >= pd.Timestamp("2025-10-15")]
    rows = []
    for k, nm, filt in (("ULVR", "Unilever", "Unilever + ESG"), ("NESN", "Nestlé", "Nestlé + Palm Oil"), ("WIL", "Wilmar", "Wilmar + Palm Oil; Wilmar + ESG")):
        its = [r for r in news if r[1] == k]; adv = [r for r in its if r[4] == -1 and "Antitrust" not in r[3]]; pos = [r for r in its if r[4] == 1]; ant = [r for r in its if "Antitrust" in r[3]]
        rows.append([nm, filt, str(len(its)), str(len(adv)), str(sum(r[5] for r in adv)), str(len(pos)), str(len(ant))])
    table_cap(doc, 3, "Hand-coded Bloomberg News headlines, 15-Oct-2025 to 15-Oct-2026")
    table(doc, ["Firm", "CN search filter", "Items coded", "Adverse items", "Severity (sum, 1–5 each)", "Positive items", "Antitrust items (excluded)"], rows, [2.0, 4.2, 1.8, 1.9, 2.4, 1.9, 2.2], 8, ["l", "l", "c", "c", "c", "c", "c"])
    note(doc, "Source: Bloomberg CN, captured 15-Oct-2026; severity coding by the authors (1 = minor, 5 = major). Search filters differ by firm (see caution below).")
    figure(doc, 3, "f06_news.png", "Timeline of coded headlines for the three firms", "Source: Bloomberg CN; authors’ coding. Antitrust items (McCormick–Unilever Foods review, Turkey probe) are excluded because they are not supply-chain risk.")
    para(doc, "Table 3.5 and Figure 3.7 summarise the coded headlines. Wilmar carries the heaviest adverse record (six items, severity 19), led by the Indonesian export under-invoicing and transfer-pricing probe (May 2026; Wilmar shares fell most in six years), the report that Russia would seize a Wilmar stake (May 2026), the jailing of a Wilmar unit executive for bribery (March 2026), a Glass Lewis controversy alert (April 2026) and Indonesian land-seizure news (January 2026). Unilever’s items are governance, claims and product-quality stories (Sunlight greenwashing order, plant production halt, Ben & Jerry’s governance, packaging targets). Nestlé has one adverse item (a sell-side cost-inflation warning) and one neutral item on palm prices; its July 2025 palm-partnership story falls just outside the window.")
    callout(doc, "Two cautions on the news evidence", ["**Governance, not deforestation.** Wilmar’s 2026 headlines are about corruption, tax and sanctions-type risk. They raise reputational and counterparty risk, but they are different from the deforestation risk the EUDR targets. The report therefore keeps the two narratives separate when reading the SPOEI.", "**Filters are not identical.** The CN search terms differ by firm (Wilmar was searched with “Palm Oil” and “ESG”; Unilever with “ESG”; Nestlé with “Palm Oil”), so counts are not like-for-like. Chapter 4 reports the index with and without the news indicator for this reason. A time series of Bloomberg’s own sentiment score for the keywords “deforestation” and “RSPO controversy” would let us compute sentiment volatility; we did not have it, so no sentiment chart is shown."], "warn")
