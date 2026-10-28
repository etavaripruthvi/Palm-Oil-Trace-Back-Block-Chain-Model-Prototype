import json
from _bootstrap import ROOT, DERIVED
from cp45_style import *
import numpy as np, pandas as pd
import palm_oil_traceability_model as M
N = json.load(open(DERIVED / "nums.json")); det = N["det"]; comps = N["comps"]
ks = ["ULVR", "NESN", "WIL"]; sc = ["Base", "Adverse", "Severe"]

# F9 scenario NPV benefit
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.9), sharey=False)
for a, k in zip(ax, ks):
    x = np.arange(3); w = 0.36
    db = [det[f"{k}_{s}"]["DB"]["benefit"] for s in sc]; bc = [det[f"{k}_{s}"]["BC"]["benefit"] for s in sc]
    a.bar(x - w / 2, db, w, color=OPT["DB"], label="Central database"); a.bar(x + w / 2, bc, w, color=OPT["BC"], label="Permissioned blockchain")
    for xi, v in zip(x - w / 2, db): a.text(xi, v + max(bc) * 0.02, f"{v:.0f}", ha="center", fontsize=7)
    for xi, v in zip(x + w / 2, bc): a.text(xi, v + max(bc) * 0.02, f"{v:.0f}", ha="center", fontsize=7)
    a.set_xticks(x); a.set_xticklabels(sc); a.set_title(NAME[k], loc="left", color=C[k]); a.grid(axis="x", visible=False); a.axhline(0, color=INK, lw=0.8)
ax[0].set_ylabel("NPV benefit vs status quo (USD m)")
h, l = ax[0].get_legend_handles_labels(); fig.legend(h, l, ncol=2, loc="lower center", bbox_to_anchor=(0.5, -0.07), fontsize=8)
fig.tight_layout(); save(fig, "f09_scenario_npv")

# F10 cost decomposition (Base)
fig, ax = plt.subplots(1, 3, figsize=(7.2, 3.1))
parts = [("pv_reg", "EUDR fines / market-access loss", "#C0392B"), ("pv_sub", "Emergency supplier substitution", "#E69F00"), ("pv_rep", "Brand / controversy revenue loss", "#8E6BB5"), ("pv_opex", "Programme OpEx (PV)", "#56B4E9"), ("capex", "Programme CapEx", "#1F4E9C")]
for a, k in zip(ax, ks):
    bottom = np.zeros(3)
    for key, lab, col in parts:
        v = np.array([comps[f"{k}_Base"][o][key] for o in ("SQ", "DB", "BC")]); a.bar(["Status\nquo", "Central\nDB", "Block-\nchain"], v, bottom=bottom, color=col, label=lab, width=0.62); bottom += v
    for i, t in enumerate(bottom): a.text(i, t + bottom.max() * 0.015, f"{t:.0f}", ha="center", fontsize=7.5, fontweight="bold")
    a.set_title(NAME[k], loc="left", color=C[k]); a.grid(axis="x", visible=False); a.set_ylim(0, bottom.max() * 1.12)
ax[0].set_ylabel("PV of total cost, Base scenario (USD m)")
h, l = ax[0].get_legend_handles_labels(); fig.legend(h, l, ncol=3, loc="lower center", bbox_to_anchor=(0.5, -0.12), fontsize=7.5)
fig.tight_layout(); save(fig, "f10_cost_decomp")

# F11 Monte Carlo distributions (Mixed regime)
fig, ax = plt.subplots(1, 3, figsize=(7.2, 2.8))
for a, k in zip(ax, ks):
    b = M.monte_carlo(k, "Mixed"); lo = min(np.percentile(b["DB"], 1), np.percentile(b["BC"], 1)); hi = max(np.percentile(b["DB"], 98), np.percentile(b["BC"], 98))
    bins = np.linspace(lo, hi, 60)
    for o in ("DB", "BC"): a.hist(b[o], bins=bins, color=OPT[o], alpha=0.55, label={"DB": "Central DB", "BC": "Blockchain"}[o], density=True)
    a.axvline(0, color=INK, lw=1); a.set_title(NAME[k], loc="left", color=C[k]); a.set_yticks([]); a.set_xlabel("NPV benefit (USD m)"); a.grid(axis="y", visible=False)
ax[0].legend(loc="upper right", fontsize=7); fig.tight_layout(); save(fig, "f11_mc")

# F12 tornado (ULVR, BC) -- merge identical multiplicative rows
tor = pd.DataFrame(N["tornado"]); base = N["tornado_base"]
tor = tor[~tor.driver.str.startswith("Realised fine")].copy(); tor.loc[tor.driver.str.startswith("Regulatory"), "driver"] = "Expected regulatory loss rate\n(event probability × fine; ×0.5 / ×2)"
tor["driver"] = tor.driver.str.replace("(x", "(×", regex=False).str.replace(" / x", " / ×", regex=False)
tor = tor.sort_values("swing")
fig, ax = plt.subplots(figsize=(7.2, 3.6))
y = np.arange(len(tor)); ax.barh(y, tor.high_case, color="#009E73", height=0.6, label="Favourable case"); ax.barh(y, tor.low_case, color="#C0392B", height=0.6, label="Unfavourable case")
ax.set_yticks(y); ax.set_yticklabels(tor.driver, fontsize=7.6); ax.axvline(0, color=INK, lw=0.9); ax.set_xlabel(f"Change in NPV benefit vs base case of USD {base:.1f} m (Unilever, blockchain)"); ax.legend(loc="lower right"); ax.grid(axis="y", visible=False)
fig.tight_layout(); save(fig, "f12_tornado")

# F13 coverage x exclusion heat maps
fig, ax = plt.subplots(1, 2, figsize=(7.2, 3.1))
for a, k in zip(ax, ("ULVR", "WIL")):
    g = M.coverage_exclusion_grid(k); im = a.imshow(g.values, cmap="YlOrRd", aspect="auto", origin="lower")
    a.set_xticks(range(g.shape[1])); a.set_xticklabels(g.columns); a.set_yticks(range(g.shape[0])); a.set_yticklabels(g.index); a.grid(False)
    for i in range(g.shape[0]):
        for j in range(g.shape[1]): a.text(j, i, f"{abs(round(g.values[i, j])):.0f}", ha="center", va="center", fontsize=6.8, color="white" if g.values[i, j] > g.values.max() * 0.6 else INK)
    a.set_title(NAME[k], loc="left", color=C[k]); a.set_xlabel("Share of non-traceable volume excluded / re-sourced"); [s.set_visible(False) for s in a.spines.values()]
ax[0].set_ylabel("Steady-state traceable share of palm supply")
fig.suptitle("PV of supplier-substitution cost, 7 years (USD m)", x=0.02, ha="left", fontsize=9.5, fontweight="bold"); fig.tight_layout(); save(fig, "f13_cov_excl")

# F15 risk-return of interventions (Mixed MC)
mc = pd.DataFrame(N["mc"]); mx = mc[mc.regime == "Mixed"]
fig, ax = plt.subplots(figsize=(7.2, 3.4))
for _, r in mx.iterrows():
    ax.scatter(r.p5, r["mean"], s=120, color=C[r.profile], marker="o" if r.option == "DB" else "D", edgecolor="white", lw=1, zorder=3)
    ax.annotate(f"{NAME[r.profile]} · {'DB' if r.option == 'DB' else 'BC'}", (r.p5, r["mean"]), xytext=(6, 4), textcoords="offset points", fontsize=7.5, color=INK)
ax.axvline(0, color=INK, lw=0.8); ax.set_xlabel("Downside: 5th-percentile NPV benefit (USD m), mixed enforcement regimes"); ax.set_ylabel("Expected NPV benefit (USD m)")
ax.scatter([], [], marker="o", color=MUTE, label="Central database"); ax.scatter([], [], marker="D", color=MUTE, label="Permissioned blockchain"); ax.legend(loc="lower left")
ax.set_title("Risk–return of the two interventions (each firm; 20,000 draws)", loc="left"); fig.tight_layout(); save(fig, "f15_risk_return")

# fine-rate robustness table
rows = []
for fine in (0.02, 0.04):
    for k in ks:
        for s in sc:
            d = M.deterministic(k, s, {"all": {"fine": fine}}); rows.append(dict(fine=fine, firm=k, scn=s, DB=d["DB"]["benefit"], BC=d["BC"]["benefit"], diff=d["BC_minus_DB"], bcr_bc=d["BC"]["bcr"], bcr_db=d["DB"]["bcr"]))
json.dump(rows, open(DERIVED / "fine_rob.json", "w"), default=float)
print("done b")
