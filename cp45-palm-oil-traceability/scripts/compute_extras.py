"""Two analyses the report quotes that are not part of the core model run:

  1. Parity points  - the BC programme-cost multiple and the regulatory-event-probability multiple at which a permissioned
                      blockchain has the same base-case NPV as a central database.   -> data/derived/parity2.json
  2. Staged strategy - "database first, ledger-ready": run the central database; switch to the ledger only in worlds drawn as
                      severe enforcement (25% of mixed-regime draws).  -> data/derived/staged.json
        upper bound        : the switch is free (database records migrate at no extra cost)
        conservative bound : the switch repeats the full ledger programme on top of the sunk database cost
                             (deterministic PV of the database programme is subtracted in switch worlds)

Uses the same seed and common random numbers as palm_oil_traceability_model.monte_carlo, so the draws are identical.
"""
import json
import numpy as np
from scipy.optimize import brentq
from _bootstrap import DERIVED
import palm_oil_traceability_model as M


def parity_points():
    out = {}
    for pk, pf in M.PROFILES.items():
        capex, opex = pf["cost"]["BC"]

        def d_cost(k):                       # BC minus DB when the BC programme (capex and opex) is scaled by k
            return M.deterministic(pk, "Base", {"BC": dict(capex_BC=capex * k, opex_BC=opex * k)})["BC_minus_DB"]

        def d_preg(k):                       # BC minus DB when the regulatory-event probability is scaled by k
            return M.deterministic(pk, "Base", {"all": dict(p_reg=pf["p_reg"] * k)})["BC_minus_DB"]

        out[pk] = dict(cost_mult=float(brentq(d_cost, 0.2, 3.0)), preg_mult=float(brentq(d_preg, 0.05, 6.0)),
                       bc_cost_base=capex, bc_opex=opex, db=list(pf["cost"]["DB"]))
    return out


def staged_strategy(n=M.N_SIMS, seed=M.SEED):
    pick = np.random.default_rng(seed).choice(3, size=n, p=[0.25, 0.50, 0.25])   # first draw inside monte_carlo("Mixed")
    switch = pick == 2                                                             # severe-enforcement worlds
    res = {}
    for pk in M.PROFILES:
        ben = M.monte_carlo(pk, "Mixed", n=n, seed=seed)
        pv_db_prog = M.deterministic(pk, "Base")["DB"]["prog"]
        series = {"DB": ben["DB"], "BC": ben["BC"],
                  "Staged (upper)": np.where(switch, ben["BC"], ben["DB"]),
                  "Staged (conservative)": np.where(switch, ben["BC"] - pv_db_prog, ben["DB"])}
        for name, x in series.items():
            res[f"{pk}|{name}"] = dict(mean=float(x.mean()), p5=float(np.percentile(x, 5)), ppos=float((x > 0).mean()))
    return res


if __name__ == "__main__":
    p = parity_points(); s = staged_strategy()
    json.dump(p, open(DERIVED / "parity2.json", "w"))
    json.dump(s, open(DERIVED / "staged.json", "w"))
    print("parity:", {k: (round(v["cost_mult"], 3), round(v["preg_mult"], 3)) for k, v in p.items()})
    print("staged mean NPV benefit (USD m):", {k: round(v["mean"], 1) for k, v in s.items() if k.startswith("ULVR")})
