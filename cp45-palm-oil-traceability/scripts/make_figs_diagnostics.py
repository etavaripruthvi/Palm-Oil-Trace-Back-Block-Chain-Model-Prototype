import json
from _bootstrap import ROOT, DERIVED
from cp45_style import *
import numpy as np, pandas as pd, matplotlib.dates as mdates
import palm_oil_traceability_model as M, wb_a, wb_b1, wb_b2
N = json.load(open(DERIVED / "nums.json"))
YRS = list(range(2019, 2026))

# F1 margins ---------------------------------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0))
for k in ("ULVR", "NESN", "WIL"):
    for a, key in zip(ax, ("gm", "om")):
        y = N[f"{key}_{k}"]; a.plot(YRS, y, color=C[k], lw=2, marker="o", ms=3.5, label=NAME[k])
        dy = {"ULVR": 6, "NESN": -6}.get(k, 0) if key == "gm" else 0
        a.annotate(f"{y[-1]:.1f}%", (YRS[-1], y[-1]), xytext=(5, dy), textcoords="offset points", color=C[k], fontsize=8, va="center", fontweight="bold")
for a, t in zip(ax, ("Gross margin (%)", "Operating margin (%)")):
    a.set_title(t, loc="left"); a.set_xticks(YRS); a.set_xticklabels([f"FY{y%100}" for y in YRS]); a.set_xlim(2018.8, 2026.1); a.set_ylim(0, 55 if "Gross" in t else 24)
ax[0].legend(loc="center left", bbox_to_anchor=(0.0, 0.62))
ax[0].annotate("Wilmar GM falls\n11.1% → 7.7%", (2021, 11.08), xytext=(2019.9, 24), arrowprops=dict(arrowstyle="->", color=MUTE), fontsize=7.5, color=MUTE)
fig.tight_layout(); save(fig, "f01_margins")

# F2 CPO + equities --------------------------------------------------------
df = M.price_frame()
fig, ax = plt.subplots(2, 1, figsize=(7.2, 4.4), sharex=True, gridspec_kw=dict(height_ratios=[1, 1.15]))
s = df["CPO"].dropna(); ax[0].plot(s.index, s.values, color="#6B3FA0", lw=2)
ax[0].set_title("Bursa Malaysia crude palm oil, Dec-26 contract (KOZ6 Comdty, MYR/t)", loc="left")
hi = s.idxmax(); ax[0].annotate(f"High {s.max():,.0f}\n{hi:%d-%b}", (hi, s.max()), xytext=(40, -12), textcoords="offset points", fontsize=7.5, color=MUTE, arrowprops=dict(arrowstyle="->", color=MUTE))
ax[0].set_ylim(4480, 5250)
ax[0].annotate(f"{s.iloc[0]:,.0f}", (s.index[0], s.iloc[0]), xytext=(-2, -14), textcoords="offset points", fontsize=7.5, color=MUTE)
ax[0].annotate(f"{s.iloc[-1]:,.0f}", (s.index[-1], s.iloc[-1]), xytext=(4, -3), textcoords="offset points", fontsize=7.5, color="#6B3FA0", fontweight="bold")
for k in ("ULVR", "NESN", "WIL"):
    x = df[k].dropna(); ax[1].plot(x.index, x / x.iloc[0] * 100, color=C[k], lw=1.8, label=NAME[k])
ax[1].axhline(100, color=MUTE, lw=0.8, ls=":")
ax[1].set_title("Equities rebased to 100 at 17-Aug-2026 (local-currency price)", loc="left"); ax[1].legend(ncol=3, loc="lower left")
ax[1].xaxis.set_major_formatter(mdates.DateFormatter("%d-%b")); ax[1].xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=0, interval=1))
plt.setp(ax[1].get_xticklabels(), rotation=0, fontsize=7.5)
fig.tight_layout(); save(fig, "f02_cpo_equities")

# F3 BESG + scope 1 index --------------------------------------------------
E = wb_a.ESG; ys = [int(y) for y in E["years"]]
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0))
for k in ("ULVR", "NESN", "WIL"):
    b = E[k]["besg"]; xs = [y for y, v in zip(ys, b) if v is not None]; vs = [v for v in b if v is not None]
    ax[0].plot(xs, vs, color=C[k], lw=2, marker="o", ms=3, label=NAME[k]); ax[0].annotate(f"{vs[-1]:.2f}", (xs[-1], vs[-1]), xytext=(4, 0), textcoords="offset points", fontsize=7.5, color=C[k], fontweight="bold", va="center")
    s1 = E[k]["s1"]; xs1 = [y for y, v in zip(ys, s1) if v is not None]; v1 = [v for v in s1 if v is not None]
    idx = np.array(v1) / v1[0] * 100; ax[1].plot(xs1, idx, color=C[k], lw=2, marker="o", ms=3)
    ax[1].annotate(f"{idx[-1]:.0f}", (xs1[-1], idx[-1]), xytext=(4, 0), textcoords="offset points", fontsize=7.5, color=C[k], fontweight="bold", va="center")
ax[0].set_title("Bloomberg ESG disclosure score (BESG, 0–10)", loc="left"); ax[0].legend(loc="lower right"); ax[0].set_xlim(2015.7, 2025.2); ax[0].set_ylim(2, 7)
ax[1].set_title("Reported Scope 1 emissions (2016 = 100)", loc="left"); ax[1].axhline(100, color=MUTE, lw=0.8, ls=":"); ax[1].set_xlim(2015.7, 2026.4)
fig.tight_layout(); save(fig, "f03_besg_scope1")

# F4 scope 3 --------------------------------------------------------------
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1.6, 1]))
for k in ("ULVR", "NESN", "WIL"):
    s3 = E[k]["s3"]; xs = [y for y, v in zip(ys, s3) if v is not None]; vs = [v / 1000 for v in s3 if v is not None]
    ax[0].plot(xs, vs, color=C[k], lw=2, marker="o", ms=3, label=NAME[k])
ax[0].set_title("Reported Scope 3 emissions (Mt CO₂e)", loc="left"); ax[0].legend(loc="upper left", ncol=3)
ax[0].annotate("Unilever series breaks\n(2020, 2022; restated boundary)", (2022, 52.8), xytext=(2017.1, 24), fontsize=7.2, color=MUTE, arrowprops=dict(arrowstyle="->", color=MUTE)); ax[0].set_ylim(0, 195)
iv = {k: v for k, v in zip(("ULVR", "NESN", "WIL"), (N["ind"][2]["raw"]))} if False else dict(zip(("WIL", "NESN", "ULVR"), (N["ind"][2]["raw"][0], N["ind"][2]["raw"][1], N["ind"][2]["raw"][2])))
# ind raw order in workbook = Unilever, Nestle, Wilmar
raw = dict(zip(("ULVR", "NESN", "WIL"), N["ind"][2]["raw"]))
ks = sorted(raw, key=raw.get, reverse=True)
ax[1].barh([NAME[k] for k in ks][::-1], [raw[k] for k in ks][::-1], color=[C[k] for k in ks][::-1], height=0.55)
for i, k in enumerate(ks[::-1]): ax[1].text(raw[k] + 40, i, f"{raw[k]:,.0f}", va="center", fontsize=8, color=INK)
ax[1].set_xlim(0, 2900); ax[1].set_title("Intensity, 2024\n(kt CO₂e per USD bn revenue)", loc="left"); ax[1].grid(axis="y", visible=False)
fig.tight_layout(); save(fig, "f04_scope3")

# F5 SPLC visibility -------------------------------------------------------
ws = {"ULVR": N["u_cov"], "NESN": N["n_cov"], "WIL": N["w_cov"]}
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.0), gridspec_kw=dict(width_ratios=[1, 1.7]))
ks = ["ULVR", "NESN", "WIL"]
ax[0].bar([NAME[k] for k in ks], [ws[k] * 100 for k in ks], color=[C[k] for k in ks], width=0.55)
for i, k in enumerate(ks): ax[0].text(i, ws[k] * 100 + 0.3, f"{ws[k]*100:.1f}%", ha="center", fontsize=8.5, fontweight="bold")
ax[0].set_title("Visible supplier cost, % of COGS\n(24 captured rows; lower bound)", loc="left"); ax[0].set_ylim(0, 20); ax[0].grid(axis="x", visible=False)
labs = ["Business-conduct\nrisk", "High GHG\nvs peers", "ESG-score\nlaggard", "Sanctioned or\ndistressed"]
rows = {k: [N["ind"][3]["raw"][i] * 100 for i in (0, 1, 2)] for i, k in enumerate(("ULVR", "NESN", "WIL"))}
vals = {"ULVR": [N["ind"][j]["raw"][0] * 100 for j in (3, 4, 5, 6)], "NESN": [N["ind"][j]["raw"][1] * 100 for j in (3, 4, 5, 6)], "WIL": [N["ind"][j]["raw"][2] * 100 for j in (3, 4, 5, 6)]}
w = 0.26
for i, k in enumerate(ks):
    ax[1].bar(np.arange(4) + (i - 1) * w, vals[k], w, color=C[k], label=NAME[k])
    for j, v in enumerate(vals[k]): ax[1].text(j + (i - 1) * w, v + 0.8, f"{v:.0f}", ha="center", fontsize=7)
ax[1].set_xticks(range(4)); ax[1].set_xticklabels(labs, fontsize=7.8); ax[1].set_title("Share of listed suppliers carrying a Bloomberg flag (%)", loc="left"); ax[1].legend(ncol=3, loc="upper right"); ax[1].set_ylim(0, 48); ax[1].grid(axis="x", visible=False)
fig.tight_layout(); save(fig, "f05_splc_visibility")

# F6 news timeline ---------------------------------------------------------
news = [r for r in wb_b2.NEWS if r[0] >= pd.Timestamp("2025-10-15") and "Antitrust" not in r[3]]
fig, ax = plt.subplots(figsize=(7.2, 2.7))
ypos = {"WIL": 2, "ULVR": 1, "NESN": 0}
for d, f, h, cat, sent, sev, n, filt in news:
    col = {-1: "#C0392B", 0: "#9CA3AF", 1: "#2E8B57"}[sent]
    ax.scatter(d, ypos[f], s=40 + sev * 55, color=col, alpha=0.8, edgecolor="white", lw=0.8, zorder=3)
ax.set_yticks([0, 1, 2]); ax.set_yticklabels(["Nestlé", "Unilever", "Wilmar"]); ax.set_ylim(-0.6, 2.8); ax.grid(axis="y", visible=False)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b-%y")); ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1)); plt.setp(ax.get_xticklabels(), fontsize=7.5)
lab = {"2026-05-28": ("Indonesia export\nunder-invoicing probe", 2.42), "2026-03-03": ("Unit executive\njailed (bribery)", 2.42), "2026-05-08": ("Russia seizure\nreport", 1.55)}
for d, (t, y) in lab.items(): ax.annotate(t, (pd.Timestamp(d), 2), xytext=(pd.Timestamp(d), y), fontsize=7, ha="center", color=MUTE, arrowprops=dict(arrowstyle="-", color="#D1D5DB", lw=0.7))
ax.scatter([], [], s=70, color="#C0392B", label="Adverse"); ax.scatter([], [], s=70, color="#9CA3AF", label="Neutral"); ax.scatter([], [], s=70, color="#2E8B57", label="Positive")
ax.legend(ncol=3, loc="lower left", bbox_to_anchor=(0.0, -0.02)); ax.set_title("Hand-coded Bloomberg CN headlines, last 12 months (bubble size = severity 1–5)", loc="left")
fig.tight_layout(); save(fig, "f06_news")

# F7 SPOEI heat map -------------------------------------------------------
ind = N["ind"]; names = ["BESG gap", "Social-pillar gap", "Scope 3 intensity", "Supplier conduct flags", "High-GHG suppliers", "ESG-laggard suppliers", "Sanctioned/distressed", "Adverse news severity", "Equity volatility (90d)", "Interest cover (inverse)"]
A = np.array([i["sc"] for i in ind]); wts = np.array([i["w"][0] for i in ind])
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.9), gridspec_kw=dict(width_ratios=[1.9, 1.15]))
im = ax[0].imshow(A, cmap="YlOrRd", vmin=0, vmax=100, aspect="auto")
ax[0].set_xticks(range(3)); ax[0].set_xticklabels(["Unilever", "Nestlé", "Wilmar"]); ax[0].set_yticks(range(10)); ax[0].set_yticklabels([f"{n}  (w={w_:.2f})" for n, w_ in zip(names, wts)], fontsize=7.6)
for i in range(10):
    for j in range(3): ax[0].text(j, i, f"{A[i, j]:.0f}", ha="center", va="center", fontsize=8, color="white" if A[i, j] > 62 else INK)
ax[0].grid(False); ax[0].tick_params(length=0); ax[0].xaxis.tick_top(); [s.set_visible(False) for s in ax[0].spines.values()]
ax[0].set_title("Scaled indicator scores (0–100), base weights", loc="left", pad=22)
sc = N["score"]; ex = N["score_exnews"]
labs2 = ["Base", "Equal", "E/S-\nheavy", "Base,\nex-news"]; data = np.array([sc["base"], sc["equal"], sc["env"], ex])
x = np.arange(4); w_ = 0.26
for j, k in enumerate(("ULVR", "NESN", "WIL")): ax[1].bar(x + (j - 1) * w_, data[:, j], w_, color=C[k], label=NAME[k])
ax[1].set_xticks(x); ax[1].set_xticklabels(labs2, fontsize=7.2); ax[1].set_ylim(0, 80); ax[1].set_title("SPOEI under four weightings", loc="left"); ax[1].legend(fontsize=7, ncol=1, loc="upper left"); ax[1].grid(axis="x", visible=False)
fig.tight_layout(); save(fig, "f07_spoei")

# F14 leverage vs criticality (Wilmar suppliers) --------------------------
sup = wb_b1.WSUP[:17]
fig, ax = plt.subplots(figsize=(7.2, 3.9))
for name, rev, cost, typ, chg, palm, rel in sup:
    if rev is None or cost is None: continue
    col = "#009E73" if palm == "Y" else "#9CA3AF"; mk = "s" if rel == "Y" else "o"
    ax.scatter(cost * 100, rev * 100, s=70, color=col, marker=mk, edgecolor="white", lw=0.8, zorder=3, alpha=0.9)
    if rev > 0.2 or cost > 0.004:
        ax.annotate(name.replace(" Tbk PT", "").replace(" Holdings", "").replace(" Plantations", " Plant."), (cost * 100, rev * 100), xytext=(5, 3), textcoords="offset points", fontsize=7, color=INK)
from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
ax.set_xscale("log"); ax.xaxis.set_major_locator(FixedLocator([0.01, 0.1, 1])); ax.xaxis.set_major_formatter(FixedFormatter(["0.01%", "0.1%", "1%"])); ax.xaxis.set_minor_locator(NullLocator())
ax.set_xlabel("Supplier's share of Wilmar's cost base (log scale): criticality to Wilmar →"); ax.set_ylabel("Wilmar's share of supplier revenue (%):\nWilmar's leverage over the supplier →")
ax.axhline(20, color=MUTE, lw=0.8, ls="--"); ax.text(0.0085, 23, "high-leverage zone (>20% of supplier revenue)", fontsize=7.5, color=MUTE, ha="left"); ax.set_xlim(0.0085, 2.0)
ax.scatter([], [], color="#009E73", s=60, label="Palm / plantation node"); ax.scatter([], [], color="#9CA3AF", s=60, label="Other supplier"); ax.scatter([], [], color=MUTE, marker="s", s=60, label="Related party / JV (verify)")
ax.legend(loc="upper right"); ax.set_ylim(-3, 105); fig.tight_layout(); save(fig, "f14_leverage")

from matplotlib.ticker import FixedLocator, FixedFormatter, NullLocator
# F16 power curve ---------------------------------------------------------
from scipy.stats import norm
def hm_se(A, n1, n0):
    q1 = A / (2 - A); q2 = 2 * A * A / (1 + A)
    return np.sqrt((A * (1 - A) + (n1 - 1) * (q1 - A * A) + (n0 - 1) * (q2 - A * A)) / (n1 * n0))
def n_events(A, prev=0.2, alpha=0.05, power=0.8):
    for n1 in range(4, 2000):
        n0 = int(round(n1 * (1 - prev) / prev))
        se0 = hm_se(0.5, n1, n0); se1 = hm_se(A, n1, n0)
        if norm.cdf(((A - 0.5) - norm.ppf(1 - alpha) * se0) / se1) >= power: return n1, n0
    return None
grid = np.arange(0.62, 0.91, 0.02); req = {p: [n_events(a, p) for a in grid] for p in (0.2, 0.35)}
fig, ax = plt.subplots(figsize=(7.2, 2.9))
for p, c in ((0.2, "#D55E00"), (0.35, "#0072B2")):
    ax.plot(grid, [r[0] for r in req[p]], color=c, lw=2, label=f"Event prevalence {int(p*100)}%")
ax.axhline(21 * 0.2, color=MUTE, ls=":", lw=1); ax.text(0.622, 21 * 0.2 + 0.25, "≈4 events if 20% of the 21 available firm-years are 'events'", fontsize=7.2, color=MUTE, ha="left")
ax.set_xlabel("True AUC to be detected (versus 0.5)"); ax.set_ylabel("Events (positives) required"); ax.set_yscale("log"); ax.yaxis.set_major_locator(FixedLocator([4, 6, 10, 20, 40, 60])); ax.yaxis.set_major_formatter(FixedFormatter(["4", "6", "10", "20", "40", "60"])); ax.yaxis.set_minor_locator(NullLocator()); ax.legend(loc="upper right", bbox_to_anchor=(1.0, 0.8))
ax.set_title("Positive events needed for 80% power, one-sided α = 5% (Hanley–McNeil)", loc="left"); fig.tight_layout(); save(fig, "f16_power")
json.dump({"power": {str(p): [(round(a, 2), r) for a, r in zip(grid, req[p])] for p in req}}, open(DERIVED / "power.json", "w"))
print("done a")
