from lib import *
import json, numpy as np
N = J("nums.json"); P = J("power.json")
ind = N["ind"]; S = np.array([i["sc"] for i in ind]); Wt = np.array([i["w"] for i in ind]); base = Wt[:, 0]
NAMES = ["BESG score gap", "BESG social-pillar gap", "Scope 3 intensity", "Supplier conduct-risk flags", "High-GHG suppliers", "ESG-laggard suppliers", "Sanctioned / distressed suppliers", "Adverse news severity (12M)", "Equity volatility (90-day)", "Interest cover (inverse)"]
PILLAR = ["ESG gap", "ESG gap", "ESG gap", "Supplier network", "Supplier network", "Supplier network", "Supplier network", "News", "Market and financial", "Market and financial"]
DEF = ["10 − BESG overall score, 2024", "10 − BESG social pillar, 2024", "Scope 3 (kt CO₂e) per USD bn revenue, 2024", "Share of listed suppliers with Bloomberg business-conduct risk", "Share of listed suppliers with high GHG intensity vs peers", "Share of listed suppliers that are ESG-score laggards", "Share of listed suppliers sanctioned or distressed", "Sum of severity (1–5) of adverse CN headlines, 12 months, excl. antitrust", "90-day annualised equity volatility, %", "Operating income / interest expense, FY2025 (lower = riskier)"]
FC = ["0 → 10", "0 → 10", "0 → 3,000", "0 → 40%", "0 → 25%", "0 → 10%", "0 → 5%", "0 → 20", "10 → 40", "12× → 2×"]

def eq(doc, parts, size=11):
    p = doc.add_paragraph(); p.alignment = WD_ALIGN_PARAGRAPH.CENTER; pfmt(p, 3, 5, 1.15, False, WD_ALIGN_PARAGRAPH.CENTER)
    for text, mode in parts:
        r = p.add_run(text); set_font(r, size, False, mode != "up" and True, INKC, name="Cambria Math" if False else "Cambria")
        if mode == "sub": r.font.subscript = True
        if mode == "sup": r.font.superscript = True
        if mode == "up": r.font.italic = False
    return p

def build(doc):
    h1(doc, "Chapter 4  Predictive Modelling and Empirical Findings")
    para(doc, "This chapter builds the Sustainable Palm Oil Exposure Index (SPOEI) from the Bloomberg indicators (4.1), specifies the supervised model that would test whether the index and its components *predict* supply-chain distress (4.2), and reports what can and cannot be concluded now (4.3). We separate the three clearly: an *index* is a transparent weighted summary; a *classifier* is validated against outcomes it did not see; only the first can be built from the screens captured.", 10.5, 6)
    h2(doc, "4.1  The Sustainable Palm Oil Exposure Index (SPOEI)")
    para(doc, "**Definition.** For firm i, SPOEI is the weighted average of K scaled indicators:", after=2)
    eq(doc, [("SPOEI", "up"), ("i", "sub"), (" = Σ", "up"), ("k=1..K", "sub"), (" w", None), ("k", "sub"), (" · S", None), ("ik", "sub"), ("        Σ w", "up"), ("k", "sub"), (" = 1,   w", "up"), ("k", "sub"), (" ≥ 0", "up")])
    eq(doc, [("S", None), ("ik", "sub"), (" = 100 × min{ 1, max{ 0, (x", "up"), ("ik", "sub"), (" − f", None), ("k", "sub"), (") / (c", "up"), ("k", "sub"), (" − f", None), ("k", "sub"), (") } }", "up")])
    para(doc, "where x is the raw indicator, f the floor (score 0) and c the cap (score 100), set so that the scale is meaningful rather than sample-relative (Table 4.1). Higher means more exposure. For indicators where *lower* is riskier (interest cover) the floor is above the cap, which reverses the scale. The ten indicators fall into four pillars that map to the four ingredients named in the brief:", after=3)
    bullets(doc, ["**Supplier network** (concentration and flags): four SPLC flag shares. HHI of visible cost shares is computed (Chapter 3) but is not scored here, because on captured rows it is a within-sample number; it enters the panel version below.", "**ESG gap**: BESG score gap, social-pillar gap, Scope 3 intensity.", "**News**: severity of adverse CN headlines over 12 months. News *volatility* needs a sentiment time series (panel version).", "**Market and financial**: equity volatility and interest cover. Commodity price variance is common to all three firms at one date, so it cannot rank them; it enters the panel version as σ²(CPO) × firm palm exposure."], 10, False, 1)
    para(doc, "**Panel version (for Section 4.2).** With firm-month data the index generalises to", after=2)
    eq(doc, [("SPOEI", "up"), ("it", "sub"), (" = ω", None), ("1", "sub"), (" · HHI*", "up"), ("it", "sub"), (" + ω", None), ("2", "sub"), (" · GAP", "up"), ("it", "sub"), (" + ω", None), ("3", "sub"), (" · σ(NEWS)", "up"), ("it", "sub"), (" + ω", None), ("4", "sub"), (" · σ²(CPO)", "up"), ("t", "sub"), (" · EXP", "up"), ("i", "sub")])
    para(doc, "where HHI* is the scaled supplier concentration, GAP the scaled ESG gap, σ(NEWS) the scaled volatility of news sentiment, and EXP the firm’s palm-linked spend share. The ten-indicator index estimated here is the cross-sectional special case.", after=6)
    table_cap(doc, 4, "SPOEI indicators, scaling and weights")
    rows = []
    for k in range(10): rows.append([str(k + 1), NAMES[k], PILLAR[k], DEF[k], FC[k], f"{Wt[k,0]:.2f}", f"{Wt[k,1]:.2f}", f"{Wt[k,2]:.2f}"])
    rows.append(["", "Sum of weights", "", "", "", "1.00", "1.00", "1.00"])
    table(doc, ["#", "Indicator", "Pillar", "Definition (source: Bloomberg SPLC, ESG, CN, FA, DES)", "Floor → cap", "Base", "Equal", "E/S-heavy"], rows, [0.6, 3.0, 2.0, 5.5, 1.7, 1.2, 1.2, 1.2], 7.5, ["c", "l", "l", "l", "c", "c", "c", "c"], total_row=True)
    note(doc, "Floors and caps are the authors’ judgement and are listed in the workbook sheet Risk_Index. “E/S-heavy” raises the weights on environmental and social indicators and drops equity volatility.")
    figure(doc, 4, "f07_spoei.png", "SPOEI indicator scores and index under four weightings", "Source: Bloomberg SPLC, ESG, CN, FA, DES (15-Oct-2026); authors’ calculations. Right panel: base, equal, environmental/social-heavy weights, and base without the news indicator (re-normalised).")
    h3(doc, "Descriptive statistics")
    sc = {"Base": N["score"]["base"], "Equal": N["score"]["equal"], "E/S-heavy": N["score"]["env"], "Base, no news": N["score_exnews"]}
    rows = []
    for nm, v in sc.items():
        v = np.array(v); order = "Wilmar > Unilever > Nestlé" if v[2] > v[0] > v[1] else "other"
        rows.append([nm, f"{v[0]:.1f}", f"{v[1]:.1f}", f"{v[2]:.1f}", f"{v.mean():.1f}", f"{v.std(ddof=1):.1f}", f"{v.max()-v.min():.1f}", order])
    table_cap(doc, 4, "SPOEI by weighting scheme (0–100; higher = more exposed)")
    table(doc, ["Weighting", "Unilever", "Nestlé", "Wilmar", "Mean", "Std. dev. (n = 3)", "Range", "Ranking (high → low)"], rows, [2.6, 1.7, 1.7, 1.7, 1.5, 2.2, 1.5, 3.5], 8.5, ["l", "c", "c", "c", "c", "c", "c", "l"])
    note(doc, "Source: workbook sheet Risk_Index; authors’ calculations. Only three cross-sectional observations exist, so the standard deviation describes the spread of these firms, not a sampling distribution.")
    para(doc, "Under base weights (Table 4.2, Figure 4.1) Wilmar scores 63.5, Unilever 53.0 and Nestlé 39.9 (mean 52.2, range 23.6). The order Wilmar > Unilever > Nestlé is the same under all four weightings. It also survives **dropping any single indicator** (10 of 10 leave-one-out runs) and holds in **78% of 20,000 random weight vectors** (Dirichlet(1,…,1)); Wilmar is the top-ranked firm in 83% of them and Nestlé the lowest in 92%. The weakest link is Unilever versus Wilmar (a 10.5-point base-case gap that shrinks to 8 points when the news indicator is dropped and to 4 points when interest cover is dropped). The result is therefore robust for Nestlé’s lower position and moderately robust for Wilmar’s higher one.")
    para(doc, "**What drives the ranking.** Figure 4.2 decomposes Wilmar’s premium. Against Nestlé (+23.6 points) the largest contributors are adverse news (+9.0), Scope 3 intensity (+7.9), supplier conduct flags (+6.5) and interest cover (+6.2); against Unilever (+10.5) they are interest cover (+7.1), conduct flags (+5.7) and news (+3.5), partly offset by Unilever’s much weaker social-pillar score (−6.6). Notably, **the BESG-based indicators work against Wilmar**: its disclosure score is the *best* of the three, so a score-based screen would rank it safest. This is the central RQ1 observation: the indicators that best separate the firms are financial resilience, supplier conduct flags and news, not the ESG score.")
    figure(doc, 4, "f17_spoei_gap.png", "What makes Wilmar’s SPOEI higher than Nestlé’s and Unilever’s", "Source: workbook sheet Risk_Index; authors’ calculations. Bars are weight × indicator-score differences, so they sum to the total gap.")
    callout(doc, "How far the index can be trusted", ["**It is a screening tool, not a validated predictor.** Scores are relative to judgement-based floors and caps, there are only three firms, and indicators were chosen by us. Validating the index against an outcome it does not contain is the job of the model in 4.2.", "**Circularity warning.** If the model’s target were built from the same news and ESG signals that feed the index, a high AUC would show only that we predicted our own inputs. The specification below prevents that."], "warn")

    h2(doc, "4.2  Model specification and methodology")
    para(doc, "The question behind RQ1 and RQ3 is whether Bloomberg-observable indicators observed at date *t* predict a supply-chain distress or controversy event in the following twelve months better than a naive benchmark. Table 4.3 gives the design, which is implemented in the companion notebook (Part 5, function `load_panel()`) and runs unchanged when the panel file is supplied.")
    table_cap(doc, 4, "Model specification")
    table(doc, ["Element", "Specification"], [
        ["Unit and panel", "Firm-month, 2016-01 to 2026-09. Universe of at least 40 palm-exposed issuers: the three case firms plus SPLC peers (plantations, refiners/traders, FMCG buyers). A three-firm panel has only three independent clusters and cannot generalise."],
        ["Target Y(i,t)", "1 if, in months t+1…t+12, any of: (a) an RSPO complaint or membership sanction against the firm or a named subsidiary; (b) a new Bloomberg ESG controversy flag; (c) a CN headline matching deforestation / RSPO / EUDR / NDPE with coded severity ≥ 3. Source for (a) is external to Bloomberg to keep the target independent of the features."],
        ["Features X(i,t)", "X1 HHI of supplier cost shares; X2 BESG environmental gap and its 12-month change; X3 news z-score (trailing 90 days) and sentiment volatility; X4 σ²(CPO) × palm exposure; X5 interest cover; X6 SPLC flag shares; X7 equity volatility and beta. All measured at t or earlier and lagged one period."],
        ["Benchmarks (RQ3)", "B0 prevalence (constant base rate); B1 persistence (event in the previous 12 months); B2 logistic regression on the BESG gap alone; B3 SPOEI as a single score."],
        ["Advanced models", "Elastic-net logistic regression (L1 ratio 0.5, C = 0.5); Random Forest (500 trees, depth ≤ 5, min. leaf 5, balanced class weights); XGBoost (300 trees, depth 3, learning rate 0.05) if installed."],
        ["Split and validation", "Expanding-window walk-forward with three test blocks: 2022, 2023 and 2024-01 to 2025-09 (the headline block). Each block is trained only on rows whose 12-month label window ends before the block starts (training month ≤ block start − 13 months), which also removes the overlap between adjacent labels (Cerqueira et al., 2020). Hyperparameters are fixed in advance (below), so no tuning window can leak. Standardisation is fitted on training data only."],
        ["Metrics", "ROC-AUC (with firm-clustered bootstrap CI), PR-AUC, precision and recall at the top 10% alert rate, Brier score and calibration slope. AUC differences against benchmarks tested with DeLong et al. (1988)."],
        ["Explainability", "Permutation importance grouped by pillar and SHAP values from the tree models (Lundberg and Lee, 2017); stability checked across walk-forward folds; partial-dependence plots for the top three features."],
        ["Leakage controls", "(i) No feature uses information after t. (ii) Target source (a) is external to the feature set. (iii) Variant runs drop X3 so that news does not appear on both sides. (iv) No random k-fold across time (Kaufman et al., 2012). (v) Firm identity is not a feature."],
        ["Success criterion (pre-registered)", "The model *outperforms* if test ROC-AUC exceeds the best of B0–B3 by at least 0.05 with a DeLong p-value < 0.05, and PR-AUC is also higher."],
    ], [3.4, 13.0], 8.3, ["l", "l"], bold_first_col=True)
    note(doc, "Random Forest: Breiman (2001). Gradient boosting: Chen and Guestrin (2016).")
    h2(doc, "4.3  Results and feature importance")
    callout(doc, "Status: classifier results are not reported", ["The screens captured on 15 October give annual fundamentals and ESG for three firms (21 firm-years) and eight weeks of prices. They contain no labelled event history, so **no ROC-AUC, precision, recall or SHAP values can be computed from them, and none are reported.** We did not substitute simulated or synthetic labels, because a model trained on invented outcomes would measure our own assumptions.", "RQ3 therefore remains open. Table 4.4 states what is needed, Figure 4.3 shows the sample size at which the question becomes answerable, and Table 4.5 is the results shell that the notebook fills once the panel exists."], "warn")
    table_cap(doc, 4, "What the available data can and cannot support")
    table(doc, ["Requirement for RQ3", "Held now", "Needed", "Gap"], [
        ["Labelled firm-periods", "21 firm-years (3 firms × 7)", "≈ 85 (17 events + 68 non-events) for AUC 0.70 vs 0.5 at 80% power", "About 4× more observations"],
        ["Events (Y = 1)", "Not labelled; ≈ 4 if 20% prevalence", "≥ 17 at prevalence 20% (≥ 20 at 35%)", "13+ events"],
        ["Independent clusters (firms)", "3", "≥ 40 for out-of-firm generalisation", "37+ firms"],
        ["Time depth", "7 years annual; 8 weeks daily", "10 years monthly (≈ 120 per firm)", "Monthly pull via BQL"],
        ["Benchmark comparison (RQ3)", "None possible", "B0–B3 on the same test window", "Panel file"],
    ], [4.0, 3.9, 5.5, 3.0], 8.3, ["l", "l", "l", "l"], bold_first_col=True)
    note(doc, "Source: Hanley and McNeil (1982) variance approximation; authors’ calculations. See notebook function `n_events_required()`.")
    figure(doc, 4, "f16_power.png", "Positive events required to detect a given AUC against chance", "Source: Hanley–McNeil standard errors; one-sided α = 5%, power 80%; authors’ calculations. Dotted line: events if 20% of the 21 available firm-years were positives.")
    para(doc, "**What can be said now about RQ1.** The structural analysis in 4.1 shows which Bloomberg indicators separate the three firms (interest cover, supplier conduct flags, adverse news and Scope 3 intensity) and which do not (BESG-based gaps, equity volatility). This is an answer about the *index*, not about *prediction*; it tells us where to look but not whether those indicators foresee events. The one pairwise test we can run, Wilmar’s BESG score against its gross margin over six years, gives r = −0.76 (p = 0.08), too weak and too short to support a conclusion.")
    table_cap(doc, 4, "Results table to be completed when the panel is available (test window 2024-01 to 2025-09)")
    ph = "[ — ]"
    table(doc, ["Model", "ROC-AUC (95% CI)", "PR-AUC", "Precision @ top 10%", "Recall @ top 10%", "Brier", "DeLong p vs best benchmark"], [
        ["B0 Prevalence", ph, ph, ph, ph, ph, "—"], ["B1 Persistence", ph, ph, ph, ph, ph, "—"], ["B2 Logit, BESG gap only", ph, ph, ph, ph, ph, ph], ["B3 SPOEI score", ph, ph, ph, ph, ph, ph], ["Elastic-net logit", ph, ph, ph, ph, ph, ph], ["Random Forest", ph, ph, ph, ph, ph, ph],
    ], [3.7, 2.6, 1.7, 2.2, 2.0, 1.5, 2.7], 8, ["l"] + ["c"] * 6, highlight={(i, j): "FFF9C4" for i in range(6) for j in range(1, 7)})
    note(doc, "Yellow cells are intentionally empty. Run notebook Part 5 after saving the panel as spoei_panel.csv (columns listed in Appendix A.3); the notebook prints this table and the SHAP/permutation-importance chart.")
