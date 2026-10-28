"""Recompute every number the report quotes from the model + the evidence workbook -> data/derived/nums.json."""
import json
from _bootstrap import ROOT, DERIVED, WORKBOOK
import numpy as np, openpyxl
import palm_oil_traceability_model as M
import wb_a
N = {}
# margins
YRS = list(range(2019, 2026))
for co, d in wb_a.FUND.items():
    rev, cogs, oi = np.array(d["rev"]), np.array(d["cogs"]), np.array(d["oi"])
    N[f"gm_{co}"] = ((rev - cogs) / rev * 100).round(2).tolist()
    N[f"om_{co}"] = (oi / rev * 100).round(2).tolist()
    N[f"cov_{co}"] = (oi / np.array(d["intexp"])).round(2).tolist()
    N[f"dio_{co}"] = (np.array(d["inv"]) / cogs * 365).round(1).tolist()
    N[f"fcf_{co}"] = (np.array(d["cfo"]) + np.array(d["capex"])).round(1).tolist()
    N[f"rev_{co}"] = d["rev"]
# ESG vs margin (Wilmar 2019-2024)
b = wb_a.ESG["WIL"]["besg"][3:9]; g = N["gm_WIL"][:6]
r = float(np.corrcoef(b, g)[0, 1]); n = 6
t = r * np.sqrt((n - 2) / (1 - r ** 2))
from scipy import stats
N["esg_gm_r"] = r; N["esg_gm_p"] = float(2 * stats.t.sf(abs(t), n - 2)); N["esg_gm_n"] = n
N["besg_WIL"] = b; N["gm_WIL_19_24"] = g
# workbook values
wb = openpyxl.load_workbook(WORKBOOK, data_only=True)
ws = wb["Risk_Index"]
ind = []
for r_ in range(5, 15):
    ind.append(dict(name=ws.cell(r_, 1).value, floor=ws.cell(r_, 3).value, cap=ws.cell(r_, 4).value,
                    raw=[ws.cell(r_, c).value for c in (5, 6, 7)], sc=[ws.cell(r_, c).value for c in (8, 9, 10)],
                    w=[ws.cell(r_, c).value for c in (11, 12, 13)]))
N["ind"] = ind
N["score"] = {k: [ws.cell(rr, c).value for c in (8, 9, 10)] for k, rr in (("base", 18), ("equal", 19), ("env", 20))}
# SPOEI excluding news (base weights renormalised)
w = np.array([i["w"][0] for i in ind]); sc = np.array([i["sc"] for i in ind])
mask = np.array([("news" not in i["name"].lower()) for i in ind])
ex = (sc[mask] * (w[mask] / w[mask].sum())[:, None]).sum(0)
N["score_exnews"] = ex.tolist()
# supply chain stats
sc_ws = wb["Supply_Chain"]
for r_ in range(1, sc_ws.max_row + 1):
    v = sc_ws.cell(r_, 1).value
    if isinstance(v, str):
        for key, lab in (("w_cov", "Visible supplier cost, % of Wilmar"), ("w_lev", "Cost-weighted dependence"), ("w_hhi", "HHI of visible cost shares, ex"),
                         ("w_palmn", "Palm/plantation nodes visible (count)")):
            if v.startswith(lab) and key not in N: N[key] = sc_ws.cell(r_, 2).value
        if v.startswith("  of which palm"): N["w_palm"] = sc_ws.cell(r_, 2).value
N["n_cov"], N["u_cov"], N["n_hhi"], N["u_hhi"] = None, None, None, None
cnt = 0
for r_ in range(1, sc_ws.max_row + 1):
    v = sc_ws.cell(r_, 1).value
    if v == "Visible supplier cost, % of COGS (lower bound)":
        N["n_cov" if cnt == 0 else "u_cov"] = sc_ws.cell(r_, 2).value; cnt += 1
cnt = 0
for r_ in range(1, sc_ws.max_row + 1):
    if sc_ws.cell(r_, 1).value == "HHI of visible cost shares (0–10,000)":
        N["n_hhi" if cnt == 0 else "u_hhi"] = sc_ws.cell(r_, 2).value; cnt += 1
# deterministic + components
def comps(pk, scn="Base", ov=None):
    pf = M.PROFILES[pk]; s = M.SCEN[scn]; price = np.full(M.G["horizon"], s["cpo"]); out = {}
    for opt in M.OPTIONS:
        prm = dict(r=M.G["r"], fine=M.G["fine"], q=M.G["q"], pi=M.G["pi"] * s["pi"], c0=M.G["c0"], p_reg=pf["p_reg"] * s["p_reg"],
                   p_ctrv=pf["p_ctrv"] * s["p_ctrv"], eff=M.OPTIONS[opt]["eff"], cmax=M.OPTIONS[opt]["cmax"], ramp=M.OPTIONS[opt]["ramp"])
        x = M.pv_total(pf, opt, prm, price); out[opt] = {k: float(v) for k, v in x.items()}
    return out
N["comps"] = {f"{pk}_{scn}": comps(pk, scn) for pk in M.PROFILES for scn in M.SCEN}
N["det"] = {f"{pk}_{scn}": M.deterministic(pk, scn) for pk in M.PROFILES for scn in M.SCEN}
mc = M.mc_summary(); N["mc"] = mc.to_dict("records")
N["cpo_sigma"] = M.CPO_SIGMA; N["mkt"] = M.market_analytics(M.price_frame()).reset_index().to_dict("records")
base, tor = M.tornado("ULVR", "BC"); N["tornado_base"] = base; N["tornado"] = tor.to_dict("records")
# parity effectiveness
from scipy.optimize import brentq
N["parity"] = {}
for pk in M.PROFILES:
    for scn in ("Base", "Adverse"):
        f = lambda e: M.deterministic(pk, scn, {"BC": {"eff": e}})["BC_minus_DB"]
        N["parity"][f"{pk}_{scn}"] = float(brentq(f, 0.5, 1.5))
# blueprint case
import copy
sv = (copy.deepcopy(M.PROFILES), dict(M.G)); M.G["horizon"] = 5; M.PROFILES["ULVR"]["cost"]["BC"] = (25.0, 5.0)
bp = []
for fine in (0.02, 0.04):
    for scn in ("Base", "Adverse", "Severe"):
        d = M.deterministic("ULVR", scn, {"all": {"fine": fine}})
        bp.append(dict(fine=fine, scn=scn, bc=d["BC"]["benefit"], roi=d["BC"]["bcr"], db=d["DB"]["benefit"], diff=d["BC_minus_DB"]))
N["blueprint"] = bp; M.PROFILES, M.G = sv
json.dump(N, open(DERIVED / "nums.json", "w"), default=float, indent=1)
print("saved"); print({k: N[k] for k in ("esg_gm_r","esg_gm_p","score","score_exnews","w_cov","w_palm","w_lev","w_hhi","n_cov","u_cov","parity")})
