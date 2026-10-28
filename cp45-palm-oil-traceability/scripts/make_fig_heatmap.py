import json
from _bootstrap import ROOT, DERIVED
from cp45_style import *
import numpy as np
import palm_oil_traceability_model as M
N = json.load(open(DERIVED / "nums.json")); comps = N["comps"]
G = M.G; fx = {"ULVR": G["EURUSD"], "NESN": G["CHFUSD"], "WIL": 1.0}
om = {k: N[f"om_{k}"][-1] / 100 for k in fx}; rev = {"ULVR": 50503.0, "NESN": 89885.0, "WIL": 70415.7}
oi = {k: om[k] * rev[k] * fx[k] for k in fx}
spoei = dict(zip(("ULVR", "NESN", "WIL"), N["score"]["base"]))
imp = {k: comps[f"{k}_Base"]["SQ"]["pv_loss"] / oi[k] * 100 for k in fx}
imp_sev = {k: comps[f"{k}_Severe"]["SQ"]["pv_loss"] / oi[k] * 100 for k in fx}
ben = {k: N["det"][f"{k}_Base"]["BC"]["benefit"] for k in fx}
print({k: round(v, 2) for k, v in imp.items()}, {k: round(v, 2) for k, v in imp_sev.items()}, {k: round(v) for k, v in oi.items()})
json.dump(dict(oi=oi, imp=imp, imp_sev=imp_sev), open(DERIVED / "impact.json", "w"))
fig, ax = plt.subplots(figsize=(7.2, 4.3))
xs = np.linspace(26, 75, 200); ys = np.logspace(-0.5, 2.0, 200); X, Y = np.meshgrid(xs, ys)
Z = (X - 26) / 49 * 0.5 + (np.log10(Y) + 0.5) / 2.5 * 0.5
ax.imshow(Z, origin="lower", extent=[26, 75, 10 ** -0.5, 10 ** 2.0], aspect="auto", cmap="YlOrRd", alpha=0.55, vmin=0, vmax=1.0)
ax.set_yscale("log"); ax.set_xlim(26, 75); ax.set_ylim(10 ** -0.5, 10 ** 2.0)
for k in fx:
    ax.scatter(spoei[k], imp[k], s=120 + ben[k] * 4, color=C[k], edgecolor="white", lw=1.5, zorder=4)
    ax.scatter(spoei[k], imp_sev[k], s=60, color=C[k], edgecolor="white", lw=1.2, marker="v", zorder=4)
    ax.plot([spoei[k]] * 2, [imp[k], imp_sev[k]], color=C[k], lw=1.2, ls=":", zorder=3)
    ax.annotate(f"{NAME[k]}\nSPOEI {spoei[k]:.0f}; {imp[k]:.1f}% (base)", (spoei[k], imp[k]), xytext={"NESN": (-14, -6), "ULVR": (0, -30), "WIL": (14, -6)}[k], textcoords="offset points", ha={"NESN": "right", "ULVR": "center", "WIL": "left"}[k], fontsize=8, color=INK, fontweight="bold")
ax.axvline(60, color=INK, lw=0.8, ls="--"); ax.text(60.4, 0.36, "SPOEI ≥ 60: Tier-2 audit", fontsize=7.5, color=INK, rotation=90, va="bottom")
ax.axhline(5, color=INK, lw=0.8, ls="--"); ax.text(26.8, 5.6, "impact ≥ 5% of one year's operating income", fontsize=7.5, color=INK)
ax.set_xlabel("Probability proxy: SPOEI (0–100)"); ax.set_ylabel("Impact: PV of 7-year expected loss, untraced,\n% of FY2025 operating income (log scale)")
ax.scatter([], [], s=70, color=MUTE, label="Base scenario"); ax.scatter([], [], s=45, color=MUTE, marker="v", label="Severe scenario"); ax.legend(loc="lower right")
ax.set_title("Risk–cost heat map: probability proxy versus economic impact (bubble size = blockchain NPV)", loc="left", fontsize=9)
ax.grid(False); fig.tight_layout(); save(fig, "f18_heatmap")
