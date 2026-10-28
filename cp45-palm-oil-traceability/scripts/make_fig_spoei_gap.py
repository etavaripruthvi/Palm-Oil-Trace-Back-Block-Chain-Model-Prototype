import json
from _bootstrap import ROOT, DERIVED
from cp45_style import *
import numpy as np
N = json.load(open(DERIVED / "nums.json")); ind = N["ind"]
names = ["BESG gap", "Social-pillar gap", "Scope 3 intensity", "Supplier conduct flags", "High-GHG suppliers", "ESG-laggard suppliers", "Sanctioned / distressed", "Adverse news severity", "Equity volatility", "Interest cover (inverse)"]
S = np.array([i["sc"] for i in ind]); w = np.array([i["w"][0] for i in ind]); c = S * w[:, None]
dWN = c[:, 2] - c[:, 1]; dWU = c[:, 2] - c[:, 0]
order = np.argsort(np.abs(dWN) + np.abs(dWU))
fig, ax = plt.subplots(figsize=(7.2, 3.8)); y = np.arange(10); h = 0.36
ax.barh(y + h / 2, dWN[order], h, color=C["NESN"], label="Wilmar minus Nestlé"); ax.barh(y - h / 2, dWU[order], h, color=C["ULVR"], label="Wilmar minus Unilever")
ax.set_yticks(y); ax.set_yticklabels([names[i] for i in order], fontsize=8); ax.axvline(0, color=INK, lw=0.9); ax.grid(axis="y", visible=False)
ax.set_xlabel("Contribution to the SPOEI gap (index points, base weights)"); ax.legend(loc="lower right")
ax.text(0.99, 0.02, f"Total gap: {c[:,2].sum()-c[:,1].sum():+.1f} (vs Nestlé), {c[:,2].sum()-c[:,0].sum():+.1f} (vs Unilever)", transform=ax.transAxes, ha="right", va="bottom", fontsize=7.5, color=MUTE) if False else None
fig.tight_layout(); save(fig, "f17_spoei_gap")
print("ok", c[:,2].sum()-c[:,1].sum(), c[:,2].sum()-c[:,0].sum())
