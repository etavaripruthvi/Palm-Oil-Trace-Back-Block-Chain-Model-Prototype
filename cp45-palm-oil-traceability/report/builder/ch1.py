from lib import *
import json
N = J("nums.json")

def build(doc):
    h1(doc, "Chapter 1  Introduction and Problem Context")
    h2(doc, "1.1  The palm oil supply chain challenge")
    para(doc, "Palm oil is the most widely traded vegetable oil and an input to food, home-care and personal-care products. Its production is concentrated in Indonesia and Malaysia, where oil-palm expansion has been a major driver of forest loss (Austin et al., 2017; Gaveau et al., 2022). Between the plantation and the consumer, the oil passes through several hands: smallholders and estates deliver fresh fruit bunches to mills; mills sell crude palm oil to refiners and traders; refiners sell fractions and derivatives to manufacturers such as Unilever and Nestlé. Many mills buy from hundreds of smallholders, and refineries blend oil from many mills, so the origin of any given tonne is rarely recorded beyond the first or second tier.")
    para(doc, "The industry response has been voluntary certification under the Roundtable on Sustainable Palm Oil (RSPO) and company “no deforestation, no peat, no exploitation” (NDPE) policies. Certification has had measurable local effects (Carlson et al., 2018), but supply-chain initiatives alone leave gaps because uncommitted buyers absorb the displaced volume (Lambin et al., 2018). Most of the certified volume that reaches manufacturers moves under the **mass-balance** model, which is central to this report.")
    table_cap(doc, 1, "RSPO supply-chain models and what each can prove under the EUDR")
    table(doc, ["Model", "Physical link to certified origin", "Plot-level evidence?", "EUDR fit"], [
        ["Identity preserved", "Single certified source, kept apart end to end", "Yes, if source is geolocated", "Strong, costly, small volumes"],
        ["Segregated", "Certified oil from several sources, kept apart from non-certified", "Yes, at mill-group level", "Good, if inputs are geolocated"],
        ["Mass balance", "Certified and non-certified oil may be mixed; certified volume tracked on paper", "No: the claim is an accounting entry", "Weak: cannot show that *this* batch is deforestation-free"],
        ["Book and claim (credits)", "No physical link; credits traded separately", "No", "Not a due-diligence tool"],
    ], [3.1, 5.2, 3.7, 4.4], 8.5, ["l", "l", "l", "l"], bold_first_col=True, highlight={2: "FFF1DC"})
    note(doc, "Source: RSPO Supply Chain Certification Standard (RSPO, 2017); authors’ assessment of fit with Regulation (EU) 2023/1115, Article 9 (geolocation of plots of production).")
    para(doc, "As Table 1.1 shows, the mass-balance model is efficient for certification but opaque for regulation. A refinery can hold a ledger entry saying 1,000 tonnes of certified oil came in and 1,000 tonnes were sold as certified, while the physical oil was a blend. That is acceptable under the RSPO rules, but it cannot by itself give a buyer the plot-level geolocation that EU law now requires. The gap between what the paperwork asserts and what can be proved is the **information asymmetry** that this project quantifies and tests a blockchain against.")

    h2(doc, "1.2  Regulatory and Scope 3 risks")
    para(doc, "**EUDR.** The Regulation covers seven commodities (cattle, cocoa, coffee, palm oil, rubber, soy and wood) and their derived products. Operators must file a due-diligence statement that includes geolocation of the plots of production and shows that the product is deforestation-free (no conversion after the 31 December 2020 cut-off) and legally produced; traders and downstream operators must keep and pass on the reference numbers. Application dates, as confirmed on the Commission’s site in July 2026, are **30 December 2026 for large and medium-sized operators** and 30 June 2027 for other micro and small operators (European Commission, 2026). A May 2026 simplification package lightened duties for low-risk-country sourcing and for downstream traders, but kept the dates and the core obligations (Hogan Lovells, 2026). A July 2026 update to the product scope adds certain palm-oil derivatives from 30 December 2027.")
    para(doc, "**Penalties.** Article 25 requires Member States to set effective, proportionate and dissuasive penalties. For legal persons, the maximum fine must be *at least* **4% of the operator’s total annual Union-wide turnover** in the preceding financial year. Penalties also include confiscation of the products and of the revenue from them, exclusion from public procurement and public funding for up to 12 months, and a temporary ban on placing or making products available on the market (Regulation (EU) 2023/1115, Art. 25). Because 4% is a floor for the *maximum*, and national authorities decide the realised amount, the cost-benefit model in Chapter 5 treats the realised fine as an uncertain parameter between 0.5% and 4% of EU turnover rather than as a fixed 4%.")
    para(doc, "**Scope 3.** For consumer-goods companies the bulk of the carbon footprint is in purchased goods, the category where palm-driven land-use change sits (GHG Protocol, 2011). Bloomberg ESG shows reported Scope 3 emissions of about 104 Mt CO₂e for Unilever (2025), 72 Mt for Nestlé (2025) and 147 Mt for Wilmar (2024). Disclosure regimes such as ESRS E1 and IFRS S2 expect Scope 3 reporting where it is material, although the scope and timing of the EU rules are still being simplified. Poor traceability makes Scope 3 figures estimates built from industry averages rather than measured supplier data. Table 1.2 groups these exposures into the channels that Chapter 5 prices.")
    table_cap(doc, 1, "Exposure channels and how the model prices them")
    table(doc, ["Channel", "Mechanism", "How Chapter 5 models it"], [
        ["Regulatory", "Fine, confiscation, market-access suspension for non-compliant EU-bound volume", "Annual event probability × realised fine rate × EU-regulated revenue × (1 − mitigation)"],
        ["Supply", "Volume that cannot be shown to be compliant must be excluded and re-sourced at a premium", "Palm spend × EU share × untraced share × exclusion share × price premium"],
        ["Reputational", "Controversy leads to boycotts, delisting and lost sales on palm-linked products", "Annual controversy probability × revenue loss × palm-linked revenue share × (1 − mitigation)"],
        ["Financing and rating", "ESG-score downgrades, covenant and index exclusion (not priced)", "Qualitative; discussed in Chapter 6"],
    ], [2.6, 6.8, 7.0], 8.5, ["l", "l", "l"], bold_first_col=True)

    h2(doc, "1.3  Research objectives and questions")
    para(doc, "The project brief (CP-45) states the following objectives and research questions, reproduced verbatim; Table 1.3 then maps each question to the evidence that answers it.", after=3)
    bullets(doc, ["Build a Bloomberg-derived dataset for Unilever, Nestlé and Wilmar.", "Identify the main drivers of blockchain sustainable palm oil traceability.", "Develop and validate a predictive/analytical model.", "Run base, adverse and severe simulations.", "Recommend sourcing, blockchain, hedging, inventory or resilience actions."], 10, True, 1)
    for q in ("**RQ1:** Which Bloomberg-derived indicators best explain/predict blockchain sustainable palm oil traceability?", "**RQ2:** How do ESG, supply links, palm oil prices, controversy/news interact under normal and stressed conditions?", "**RQ3:** Does the predictive model outperform a simple historical/statistical benchmark?", "**RQ4:** Which supply-chain/blockchain intervention gives the best risk–cost trade-off?"):
        p = para(doc, q, 10.5, 2, WD_ALIGN_PARAGRAPH.LEFT, left=0.6)
    sp = doc.add_paragraph(); pfmt(sp, 0, 2, 1.0)
    table_cap(doc, 1, "Where each research question is answered, and how far the evidence goes")
    table(doc, ["RQ", "Chapter", "Evidence used", "Status"], [
        ["RQ1", "3, 4", "SPOEI indicator ranking and weight-robustness; feature specification for the classifier", "**Partly answered.** Index drivers identified; predictive ranking needs a labelled panel"],
        ["RQ2", "3, 5", "Descriptive links among BESG, Scope 1/3, SPLC flags, news coding, 8-week CPO window; stress scenarios", "**Answered descriptively.** Price links are not statistically testable on 8 weeks of data"],
        ["RQ3", "4", "Protocol, benchmarks and power analysis", "**Not answered.** Requires the labelled panel (about 85 firm-periods, ≥17 events)"],
        ["RQ4", "5, 6", "Three-option cost-benefit model, 20,000-draw Monte Carlo, tornado, parity points", "**Answered**, conditional on ASSUMPTION inputs"],
    ], [1.2, 1.7, 7.4, 6.1], 8.5, ["c", "c", "l", "l"], bold_first_col=True, highlight={2: "FFF9C4"})

    h2(doc, "1.4  Scope and case-study focus")
    para(doc, "The brief names three units of analysis, which sit at different points of the chain (Table 1.4). **Unilever** and **Nestlé** are downstream manufacturers and, depending on the product and the import route, operators or downstream operators/traders under the Regulation. **Wilmar International** is one of the world’s largest palm-oil processors and traders and also owns plantations, so it is both an upstream supplier to the manufacturers and a regulated operator in its own right. The benchmark programme named in the brief is RSPO certification. The analysis is global, with emphasis on Indonesia, Malaysia and the EU market. Data are annual (FY2019–FY2025) for fundamentals, annual (2016–2024/25) for ESG, and daily for an eight-week price window (17 August to 15 October 2026).")
    table_cap(doc, 1, "The three case firms (Bloomberg DES, FA and ESG, 15 October 2026)")
    table(doc, ["", "Unilever", "Nestlé", "Wilmar"], [
        ["Ticker", "ULVR LN", "NESN SW", "WIL SP"],
        ["Role in the palm chain", "Brand owner / EU operator", "Brand owner / EU operator", "Refiner, trader, plantation owner"],
        ["FY2025 revenue (reporting currency, m)", "EUR 50,503", "CHF 89,885", "USD 70,416"],
        ["FY2025 gross margin / operating margin", "47.0% / 20.0%", "45.8% / 15.5%", "8.2% / 3.2%"],
        ["Market capitalisation (local currency, m)", "GBP 104,033", "CHF 203,262", "SGD 21,668"],
        ["Employees", "118,000", "271,000", "100,000"],
        ["BESG score, 2024 (0–10)", "4.82", "5.28", "6.15"],
        ["Reported Scope 3 (Mt CO₂e)", "103.8 (2025)", "72.0 (2025)", "147.0 (2024)"],
        ["Interest cover, FY2025 (operating income / interest)", "9.1×", "8.3×", "2.1×"],
        ["Largest revenue market (SPLC)", "USA 20.6%", "USA 33.9%", "China 47.3%; EU exposure indirect"],
    ], [6.4, 3.3, 3.3, 3.4], 8.5, ["l", "c", "c", "c"], bold_first_col=False)
    note(doc, "Source: Bloomberg (DES, FA, ESG, SPLC), transcribed 15-Oct-2026. Unilever FY2024–25 reflect the ice-cream demerger restatement; Scope 3 series for Unilever contain boundary breaks (Chapter 3).")
    callout(doc, "Scope boundary", "Bloomberg SPLC lists visible Tier-1 relationships only. Private Tier-2 mills and Tier-3 smallholders are outside the data. The report therefore measures how much of the chain is *invisible* and what closing that gap is worth, rather than mapping the chain itself.", "warn")
