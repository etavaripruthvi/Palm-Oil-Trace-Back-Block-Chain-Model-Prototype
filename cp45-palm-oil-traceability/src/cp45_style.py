import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams.update({
    "font.family": ["Liberation Sans", "DejaVu Sans"], "font.size": 8.5,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titlesize": 9.5, "axes.titleweight": "bold",
    "axes.labelsize": 8.5, "legend.frameon": False, "legend.fontsize": 8, "figure.dpi": 100, "savefig.dpi": 220,
    "axes.grid": True, "grid.color": "#E5E7EB", "grid.linewidth": 0.6, "axes.axisbelow": True,
})
C = {"ULVR": "#0072B2", "NESN": "#E69F00", "WIL": "#009E73"}
NAME = {"ULVR": "Unilever", "NESN": "Nestlé", "WIL": "Wilmar"}
OPT = {"SQ": "#9CA3AF", "DB": "#56B4E9", "BC": "#D55E00"}
INK = "#1F2937"; MUTE = "#6B7280"
import pathlib
FIG = str(pathlib.Path(__file__).resolve().parents[1] / "figures") + "/"
def save(fig, name):
    pathlib.Path(FIG).mkdir(parents=True, exist_ok=True)
    fig.savefig(FIG + name + ".png", bbox_inches="tight", facecolor="white"); plt.close(fig)
