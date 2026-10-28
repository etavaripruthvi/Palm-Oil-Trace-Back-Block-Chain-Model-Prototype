"""Generate notebooks/CP45_Palm_Oil_Traceability_Notebook.ipynb (the notebook source lives in this file).

    python scripts/build_notebook.py [output.ipynb]
"""
import json, sys
cells = []
def md(t): cells.append({"cell_type": "markdown", "metadata": {}, "source": t.strip("\n").splitlines(True)})
def code(t): cells.append({"cell_type": "code", "metadata": {}, "execution_count": None, "outputs": [], "source": t.strip("\n").splitlines(True)})

md("""
# CP-45 — Blockchain Sustainable Palm Oil Traceability (Unilever · Nestlé · Wilmar)
**Run All** from top to bottom. The notebook finds `src/palm_oil_traceability_model.py` automatically (it holds the data and the NPV / Monte Carlo engine); if you copy the notebook elsewhere, keep that file next to it.

| Part | What it does | Evidence status |
|---|---|---|
| 1 | Market analytics on the Bloomberg price tables you captured | Real data, only ~8 weeks — method demo |
| 2 | Cost-benefit: status quo vs central database vs permissioned blockchain (Base / Adverse / Severe) | Bloomberg revenue/COGS + **assumptions** |
| 3 | The "blueprint case": CapEx $25M, OpEx $5M/yr, 5-year horizon | Assumptions from the brief |
| 4 | Monte Carlo, tornado, coverage × substitution heat map | Same engine |
| 5 | Distress classifier per report Ch. 4.2: power table, walk-forward split, benchmarks B0–B3, RF / elastic-net / XGBoost, DeLong test, SHAP or grouped permutation importance | **Runs on `data/panel/spoei_panel.csv` if you supply it; otherwise a SYNTHETIC code-test panel — not evidence** |
""")
code("""
import os, sys, pathlib, warnings
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
for _p in (pathlib.Path.cwd(), *pathlib.Path.cwd().parents):          # find src/ whether run from notebooks/ or the repo root
    if (_p / "src" / "palm_oil_traceability_model.py").exists():
        sys.path.insert(0, str(_p / "src")); REPO = _p; break
else:
    REPO = pathlib.Path.cwd()                                           # module sitting next to the notebook
import palm_oil_traceability_model as M
warnings.filterwarnings("ignore")
pd.set_option("display.width", 160, "display.float_format", lambda x: f"{x:,.2f}")
plt.rcParams.update({"figure.figsize": (9, 4.2), "axes.grid": True, "grid.alpha": .3})
print("Model module loaded. Seed:", M.SEED, "| simulations:", M.N_SIMS)
""")
md("## 1. Market analytics — KOZ6 palm oil futures vs the three equities\nLog returns only where both days printed. ~8 weeks of data: correlations inside ±2/√n are indistinguishable from zero.")
code("""
px = M.price_frame()
stats = M.market_analytics(px)
stats["band_±2/√n"] = 2 / np.sqrt(stats["n_pairs_vs_CPO"])
display(stats)
reb = px.ffill() / px.ffill().iloc[0] * 100
ax = reb.plot(); ax.set_title("Rebased prices (17-Aug-26 = 100)"); ax.set_ylabel("index"); plt.show()
""")
md("## 2. Cost-benefit: three options × three scenarios (USD m, PV vs status quo)\nBenefit = PV(total cost, status quo) − PV(total cost, option). Inputs marked ASSUMPTION in the module are placeholders to calibrate.")
code("""
rows = []
for pk in M.PROFILES:
    for scn in M.SCEN:
        d = M.deterministic(pk, scn)
        rows.append(dict(firm=M.PROFILES[pk]["name"], scenario=scn, DB_NPV=d["DB"]["benefit"], BC_NPV=d["BC"]["benefit"],
                         BC_minus_DB=d["BC_minus_DB"], DB_ROI=d["DB"]["bcr"], BC_ROI=d["BC"]["bcr"], BC_breakeven_pReg_x=d["BC"]["breakeven_k"]))
det = pd.DataFrame(rows); display(det)
piv = det.pivot(index="firm", columns="scenario", values="BC_minus_DB")[list(M.SCEN)]
ax = piv.plot.bar(); ax.set_title("Blockchain NPV minus central-database NPV (USD m)"); ax.axhline(0, color="k", lw=.8); plt.show()
""")
md("""
## 3. The blueprint case — CapEx $25M, OpEx $5M/yr, 5-year horizon, fines 2–4% of EU turnover
Applied to Unilever. Two honesty points: (i) a ledger records data but cannot verify it (the *oracle problem*), so 'fines → ~0' needs satellite + audit verification feeding it — here that is the effectiveness parameter; (ii) the right comparison is against a central database, not only against doing nothing.
""")
code("""
import copy
saved = (copy.deepcopy(M.PROFILES), dict(M.G), copy.deepcopy(M.OPTIONS))
M.G["horizon"] = 5
M.PROFILES["ULVR"]["cost"]["BC"] = (25.0, 5.0)
out = []
for fine in (0.02, 0.04):
    for eff in (0.90, 0.99):
        for scn in ("Base", "Severe"):
            d = M.deterministic("ULVR", scn, {"all": {"fine": fine}, "BC": {"eff": eff}})
            out.append(dict(fine_rate=fine, blockchain_effectiveness=eff, scenario=scn, NPV_BC=d["BC"]["benefit"],
                            ROI_x=d["BC"]["bcr"], NPV_central_DB=d["DB"]["benefit"], BC_minus_DB=d["BC_minus_DB"]))
blue = pd.DataFrame(out); display(blue)
print("Reading: with the brief's $25M/$5M and 5 years, does the blockchain beat doing nothing?",
      "YES" if (blue.NPV_BC > 0).all() else "ONLY IN SOME CASES", "| does it beat a central database?",
      "YES in all cases" if (blue.BC_minus_DB > 0).all() else f"in {(blue.BC_minus_DB > 0).sum()} of {len(blue)} cases")
M.PROFILES, M.G, M.OPTIONS = saved   # restore the 7-year workbook settings
""")
md("## 4. Monte Carlo, tornado and heat map (7-year workbook settings)")
code("""
res = {r: M.monte_carlo("ULVR", r) for r in ("Base", "Mixed", "Severe")}
fig, axs = plt.subplots(1, 3, figsize=(13, 3.8), sharey=True)
for ax, (r, b) in zip(axs, res.items()):
    lo, hi = np.percentile(np.r_[b["DB"], b["BC"]], [1, 99]); bins = np.linspace(lo, hi, 40)
    ax.hist(np.clip(b["DB"], lo, hi), bins, alpha=.55, label="Central database"); ax.hist(np.clip(b["BC"], lo, hi), bins, alpha=.55, label="Blockchain")
    ax.axvline(0, color="k", lw=.8); ax.set_title(f"Unilever — {r}"); ax.set_xlabel("NPV benefit, USD m")
axs[0].legend(); plt.tight_layout(); plt.show()
mc = M.mc_summary(); display(mc[mc.regime == "Mixed"].round(2))
""")
code("""
base, tor = M.tornado("ULVR", "BC")
ax = tor.set_index("driver")[["low_case", "high_case"]].iloc[::-1].plot.barh(stacked=False, figsize=(9, 4.5))
ax.set_title(f"Tornado — Unilever blockchain NPV (base {base:,.1f} USD m)"); ax.axvline(0, color="k", lw=.8); plt.show()
g = M.coverage_exclusion_grid("ULVR").abs()
fig, ax = plt.subplots(figsize=(6.5, 4.5)); im = ax.imshow(g.values, cmap="RdYlGn_r", aspect="auto")
ax.set_xticks(range(g.shape[1]), g.columns); ax.set_yticks(range(g.shape[0]), g.index)
ax.set_xlabel("share of non-traceable volume excluded"); ax.set_ylabel("steady traceable share"); ax.set_title("PV substitution cost, USD m")
for i in range(g.shape[0]):
    for j in range(g.shape[1]): ax.text(j, i, f"{g.values[i, j]:.0f}", ha="center", va="center", fontsize=8)
plt.colorbar(im); plt.show()
""")
md("""
## 5. Distress classifier — the protocol in report Chapter 4.2 (firm-month panel)
**What this section can and cannot prove.** A supervised model needs a *labelled panel*. The Bloomberg screens captured on 15-Oct-2026 give 3 firms × 7 years, which is too small (see the power table below). Save your panel as `data/panel/spoei_panel.csv` (one row per firm-month, ≥ 40 palm-exposed issuers, 2016-01 → 2026-09) with columns

`firm_id, month (YYYY-MM), X1_hhi, X2_env_gap, X2_env_gap_chg12, X3_news_z, X3_news_vol, X4_cpo_var_x_exposure, X5_int_cover, X6_flag_share, X7_eq_vol, Y_event_12m`

`Y_event_12m` = 1 if in months t+1…t+12 there is an RSPO complaint/sanction, a new Bloomberg ESG controversy flag, or a CN headline on deforestation / RSPO / EUDR / NDPE with severity ≥ 3. Define it **before** modelling and keep at least one of its sources outside the feature set (otherwise the AUC measures how well you predict your own inputs).

Without the file, a **SYNTHETIC panel** is generated only to prove the code runs. Every number printed from it is tagged and is **not evidence**.
""")
code("""
# 5a. How many labelled events are needed? (Hanley–McNeil standard errors, one-sided alpha, power)
from scipy.stats import norm
def _hm_se(A, n1, n0):
    q1, q2 = A / (2 - A), 2 * A * A / (1 + A)
    return np.sqrt((A * (1 - A) + (n1 - 1) * (q1 - A * A) + (n0 - 1) * (q2 - A * A)) / (n1 * n0))
def n_events_required(auc, prevalence=0.2, alpha=0.05, power=0.8):
    for n1 in range(4, 5000):
        n0 = int(round(n1 * (1 - prevalence) / prevalence))
        if norm.cdf(((auc - .5) - norm.ppf(1 - alpha) * _hm_se(.5, n1, n0)) / _hm_se(auc, n1, n0)) >= power: return n1, n0
pw = pd.DataFrame([dict(true_AUC=a, prevalence=p, events=n_events_required(a, p)[0], non_events=n_events_required(a, p)[1]) for a in (.65, .70, .75, .80) for p in (.2, .35)])
pw["total_rows"] = pw.events + pw.non_events; display(pw)
print("Rows held from the screens: 21 firm-years (3 firms x 7 years) -> not enough for RQ3.")
""")
code("""
# 5b. Panel loading, time-based walk-forward split, benchmarks and models
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.metrics import roc_auc_score, average_precision_score, brier_score_loss
try:
    from xgboost import XGBClassifier; HAVE_XGB = True
except Exception:
    HAVE_XGB = False
try:
    import shap; HAVE_SHAP = True
except Exception:
    HAVE_SHAP = False

ALL_FEATS = ["X1_hhi", "X2_env_gap", "X2_env_gap_chg12", "X3_news_z", "X3_news_vol", "X4_cpo_var_x_exposure", "X5_int_cover", "X6_flag_share", "X7_eq_vol"]
PILLAR = {"X1_hhi": "Supplier network", "X6_flag_share": "Supplier network", "X2_env_gap": "ESG gap", "X2_env_gap_chg12": "ESG gap",
          "X3_news_z": "News", "X3_news_vol": "News", "X4_cpo_var_x_exposure": "Market & financial", "X5_int_cover": "Market & financial", "X7_eq_vol": "Market & financial"}
SIGN = {"X5_int_cover": -1}      # lower interest cover = riskier; every other feature: higher = riskier

def load_panel(path=None):
    cands = [path] if path else ["spoei_panel.csv", str(REPO / "data" / "panel" / "spoei_panel.csv")]
    path = next((c for c in cands if c and os.path.exists(c)), None)
    if path:
        df = pd.read_csv(path); df["SYNTHETIC"] = False
    else:                                       # SYNTHETIC code-test panel -- NOT EVIDENCE
        rng = np.random.default_rng(M.SEED); n, T = 45, 120
        df = pd.DataFrame([(i, t) for i in range(n) for t in range(T)], columns=["firm_id", "t"])
        df["month"] = pd.period_range("2016-01", periods=T, freq="M").astype(str)[df.t]
        f = lambda s: rng.normal(0, s, len(df))
        df["X1_hhi"] = rng.beta(2, 8, n)[df.firm_id] + f(.02); df["X2_env_gap"] = rng.uniform(0, 1, n)[df.firm_id] + f(.05)
        df["X2_env_gap_chg12"] = f(.1); df["X3_news_z"] = f(1); df["X3_news_vol"] = np.abs(f(1))
        df["X4_cpo_var_x_exposure"] = rng.gamma(2, .5, T)[df.t] * rng.uniform(.2, 1, n)[df.firm_id]
        df["X5_int_cover"] = rng.uniform(2, 12, n)[df.firm_id] + f(.5); df["X6_flag_share"] = rng.beta(2, 10, n)[df.firm_id] + f(.01); df["X7_eq_vol"] = rng.uniform(15, 40, n)[df.firm_id] + f(2)
        z = -4.3 + 3 * df.X1_hhi + 1.5 * df.X2_env_gap + .5 * df.X3_news_z - .12 * df.X5_int_cover + .5 * df.X4_cpo_var_x_exposure
        df["Y_event_12m"] = (rng.uniform(size=len(df)) < 1 / (1 + np.exp(-z))).astype(int); df["SYNTHETIC"] = True
    df["m"] = pd.PeriodIndex(df["month"], freq="M").astype(int)       # integer month index
    return df.sort_values(["firm_id", "m"]).reset_index(drop=True)

panel = load_panel(); SYN = bool(panel.SYNTHETIC.iloc[0]); TAG = "SYNTHETIC - code test, NOT EVIDENCE" if SYN else "real panel"
FEATS = [c for c in ALL_FEATS if c in panel.columns]; assert len(FEATS) >= 4, "need at least X1-X4"
panel["B1_persist"] = panel.groupby("firm_id")["Y_event_12m"].shift(12)           # event during the previous 12 months
print(f"[{TAG}] rows={len(panel)} firms={panel.firm_id.nunique()} events={panel.Y_event_12m.sum()} features={FEATS}")

def blocks():
    # three walk-forward test blocks; training rows must have their 12-month label window END before the block starts
    P = lambda s: pd.Period(s, "M").ordinal
    return [("2022", P("2022-01"), P("2022-12")), ("2023", P("2023-01"), P("2023-12")), ("2024-01..2025-09", P("2024-01"), P("2025-09"))]

def spoei_score(df, ref):                      # B3: equal-weight composite of standardised features (train-fitted mean/sd)
    mu, sd = ref[FEATS].mean(), ref[FEATS].std().replace(0, 1)
    return sum(SIGN.get(c, 1) * (df[c] - mu[c]) / sd[c] for c in FEATS) / len(FEATS)

def make_models():
    m = {"B2 Logit, env gap only": ("one", make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))),
         "Elastic-net logit": ("all", make_pipeline(StandardScaler(), LogisticRegression(penalty="elasticnet", solver="saga", l1_ratio=.5, C=.5, max_iter=5000))),
         "Random Forest": ("all", RandomForestClassifier(n_estimators=500, max_depth=5, min_samples_leaf=5, class_weight="balanced", random_state=M.SEED, n_jobs=-1))}
    if HAVE_XGB: m["XGBoost"] = ("all", XGBClassifier(n_estimators=300, max_depth=3, learning_rate=.05, subsample=.8, eval_metric="logloss", random_state=M.SEED))
    return m

def metrics(y, p, top=.10):
    k = max(1, int(round(top * len(y)))); idx = np.argsort(-p)[:k]
    return dict(ROC_AUC=roc_auc_score(y, p), PR_AUC=average_precision_score(y, p), Precision_top10=y.iloc[idx].mean(), Recall_top10=y.iloc[idx].sum() / max(1, y.sum()), Brier=brier_score_loss(y, np.clip(p, 0, 1)))

def delong_p(y, p1, p2):                       # paired DeLong test of AUC1 == AUC2 (DeLong et al., 1988)
    y = np.asarray(y); pos, neg = y == 1, y == 0; m, n = pos.sum(), neg.sum()
    def comps(p):
        px, py = p[pos], p[neg]
        v10 = np.array([((x > py).sum() + .5 * (x == py).sum()) / n for x in px]); v01 = np.array([((px > z).sum() + .5 * (px == z).sum()) / m for z in py]); return v10, v01
    c1, c2 = comps(np.asarray(p1, float)), comps(np.asarray(p2, float))
    V10, V01 = np.vstack([c1[0], c2[0]]), np.vstack([c1[1], c2[1]])
    auc = V10.mean(axis=1); S = np.cov(V10) / m + np.cov(V01) / n
    var = S[0, 0] + S[1, 1] - 2 * S[0, 1]; z = (auc[0] - auc[1]) / np.sqrt(var) if var > 0 else np.nan
    return 2 * (1 - norm.cdf(abs(z)))

results, store = [], {}
for bname, lo, hi in blocks():
    tr = panel[panel.m <= lo - 13]; te = panel[(panel.m >= lo) & (panel.m <= hi)].dropna(subset=["B1_persist"])
    if te.Y_event_12m.sum() < 5 or te.Y_event_12m.nunique() < 2 or tr.Y_event_12m.sum() < 5: print(f"block {bname}: too few events - skipped"); continue
    y = te.Y_event_12m; sc = {"B0 Prevalence": np.full(len(te), tr.Y_event_12m.mean()), "B1 Persistence": te.B1_persist.values.astype(float), "B3 SPOEI score": spoei_score(te, tr).values}
    fitted = {}
    for nm, (cols, mdl) in make_models().items():
        c = ["X2_env_gap"] if cols == "one" else FEATS; mdl.fit(tr[c], tr.Y_event_12m); sc[nm] = mdl.predict_proba(te[c])[:, 1]; fitted[nm] = (mdl, c)
    best_bench = max(["B1 Persistence", "B2 Logit, env gap only", "B3 SPOEI score"], key=lambda k: roc_auc_score(y, sc[k]))
    for nm, p in sc.items():
        r = dict(block=bname, model=nm, **metrics(y, np.asarray(p, float)))
        r["DeLong_p_vs_best_benchmark"] = delong_p(y, p, sc[best_bench]) if nm not in ("B0 Prevalence", best_bench) else np.nan
        results.append(r)
    store[bname] = (te, fitted, best_bench)
res = pd.DataFrame(results); res["data"] = TAG
display(res.round(3))
if len(res):
    last = res[res.block == res.block.iloc[-1]].set_index("model"); adv = [m for m in ("Elastic-net logit", "Random Forest", "XGBoost") if m in last.index]; bench = ["B1 Persistence", "B2 Logit, env gap only", "B3 SPOEI score"]
    a_best = last.loc[adv, "ROC_AUC"].idxmax(); b_best = last.loc[bench, "ROC_AUC"].idxmax()
    ok = (last.ROC_AUC[a_best] - last.ROC_AUC[b_best] >= .05) and (last.DeLong_p_vs_best_benchmark[a_best] < .05) and (last.PR_AUC[a_best] > last.PR_AUC[b_best])
    print(f"[{TAG}] Headline block {last.block.iloc[0]}: best advanced model = {a_best}; best simple benchmark = {b_best}. Pre-registered rule (AUC gain >= 0.05, DeLong p < 0.05, higher PR-AUC): {'MET' if ok else 'NOT MET'}.")
""")
code("""
# 5c. Which variable predicts best?  Grouped permutation importance (by pillar) + SHAP if installed
if store:
    bname = list(store)[-1]; te, fitted, _ = store[bname]; mdl, cols = fitted["Random Forest"]; y = te.Y_event_12m; rng = np.random.default_rng(M.SEED)
    base_auc = roc_auc_score(y, mdl.predict_proba(te[cols])[:, 1]); imp = {}
    for pillar in sorted(set(PILLAR[c] for c in cols)):
        drops = []
        for _ in range(20):
            X = te[cols].copy(); idx = rng.permutation(len(X))
            for c in cols:
                if PILLAR[c] == pillar: X[c] = X[c].values[idx]
            drops.append(base_auc - roc_auc_score(y, mdl.predict_proba(X)[:, 1]))
        imp[pillar] = np.mean(drops)
    ax = pd.Series(imp).sort_values().plot.barh(); ax.set_title(f"Fall in test AUC when a pillar is shuffled - Random Forest [{TAG}]"); ax.set_xlabel("AUC drop"); plt.show()
    if HAVE_SHAP:
        sv = shap.TreeExplainer(mdl).shap_values(te[cols]); sv = sv[1] if isinstance(sv, list) else (sv[..., 1] if getattr(sv, "ndim", 2) == 3 else sv)
        shap.summary_plot(sv, te[cols], show=False); plt.title(f"SHAP - Random Forest [{TAG}]"); plt.show()
    else: print("shap not installed (pip install shap) - grouped permutation importance shown instead.")
""")
md("""
## Reading the results
* **Economics (parts 2–4):** traceability itself carries most of the value; the blockchain's *incremental* value over a central database depends on how much extra assurance it earns (`eff`) and on enforcement severity. Quote the break-even `eff`, not just a positive NPV.
* **Classifier (part 5):** only report AUC / SHAP once `spoei_panel.csv` holds a real labelled panel. Until then this section proves the pipeline, not the hypothesis. The pre-registered success rule is in the report (Ch. 4.2).
* **Before submitting:** replace the illustrative FX and every ASSUMPTION with sourced values (see the workbook's *Assumptions* and *Next_Steps* sheets).
""")

nb = {"cells": cells, "metadata": {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
      "language_info": {"name": "python"}}, "nbformat": 4, "nbformat_minor": 5}
from _bootstrap import ROOT
out = ROOT / "notebooks" / "CP45_Palm_Oil_Traceability_Notebook.ipynb" if len(sys.argv) < 2 else __import__("pathlib").Path(sys.argv[1])
out.parent.mkdir(parents=True, exist_ok=True)
with open(out, "w", encoding="utf-8") as fh:
    json.dump(nb, fh, indent=1, ensure_ascii=False)
print("wrote", out, "-", len(cells), "cells")
