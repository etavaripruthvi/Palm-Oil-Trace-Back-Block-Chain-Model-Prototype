from _bootstrap import ROOT, DERIVED
from cp45_style import *
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
fig, ax = plt.subplots(figsize=(7.4, 7.4)); ax.set_xlim(-6, 100); ax.set_ylim(0, 100); ax.axis("off")
def box(x, y, w, h, text, fc, ec, fs=6.9, bold=False):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.2,rounding_size=1.0", fc=fc, ec=ec, lw=1.1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=INK, fontweight="bold" if bold else "normal", linespacing=1.3)
def arrow(x1, y1, x2, y2, col=INK, ls="-", lw=1.3, style="-|>"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle=style, mutation_scale=9, color=col, lw=lw, ls=ls, shrinkA=0, shrinkB=0))
def lane(y0, y1, label, col):
    ax.add_patch(FancyBboxPatch((-5.8, y0), 3.4, y1 - y0, boxstyle="round,pad=0.1,rounding_size=0.8", fc=col, ec="none"))
    ax.text(-4.1, (y0 + y1) / 2, label, rotation=90, ha="center", va="center", fontsize=7.2, fontweight="bold", color="white")
xs = [2, 21.5, 41, 60.5, 80]; w = 16.6
# lane A physical
PH, PE = "#FFF4DC", "#E69F00"
lane(80.5, 95, "A  PHYSICAL", "#B7791F")
for x, l in zip(xs, ["Plantation /\nsmallholder\n(fresh fruit bunches)", "Mill\n(FFB → crude\npalm oil)", "Refinery / trader\n(RBD oil, fractions;\nWilmar-type)", "FMCG manufacturer\n(Unilever, Nestlé)", "EU market\n(EUDR enforcement)"]): box(x, 81.5, w, 12.5, l, PH, PE)
for i in range(4): arrow(xs[i] + w + 0.3, 87.7, xs[i + 1] - 0.3, 87.7, col="#B7791F", lw=1.6)
ax.text(50, 97.4, "Mass balance: certified and non-certified oil may be mixed physically; only the ledger can show which volumes are verified", ha="center", fontsize=6.8, color="#7A4B00", style="italic")
# lane B capture / oracles
OR, OE = "#EAF6EA", "#2E8B57"
lane(60, 74, "B  ORACLES", "#2E8B57")
for x, l in zip(xs, ["Plot survey, land\ntitle, farmer ID", "Satellite check\n(optical + radar)", "Scale weights, IoT,\nQR / RFID lot tags", "Third-party audits,\nRSPO / NDPE records", "Customs and EU\nregulatory systems"]): box(x, 61, w, 12, l, OR, OE)
for x in xs: arrow(x + w / 2, 80.9, x + w / 2, 73.4, col="#9CA3AF", ls=(0, (3, 2)), lw=1.1)
# lane C ledger events
DG, DE = "#E6F1FB", "#0072B2"
lane(38, 54, "C  LEDGER", "#0072B2")
for x, l in zip(xs, ["1  Register plot\nhash GPS polygon", "2  Deforestation\ncheck (31-Dec-20)", "3  Mill batch event\nFFB lots → CPO lots", "4  Refinery split /\nmerge: balance cap", "5  Due-diligence\nstatement + ref. no."]): box(x, 39, w, 14, l, DG, DE)
for i in range(4): arrow(xs[i] + w + 0.3, 46, xs[i + 1] - 0.3, 46, col=DE, lw=1.4)
for x in xs: arrow(x + w / 2, 60.7, x + w / 2, 53.6, col=OE, lw=1.3)
# lane D contracts and governance
CO, CE = "#F3E8FA", "#7B3FA0"
lane(9, 30, "D  CONTRACTS", "#7B3FA0")
dx = [2, 35.5, 69]; dw = 29
box(dx[0], 10, dw, 19, "Permissioned consortium nodes\nManufacturers · refiners / traders\nmills · certifiers / auditors\nRead-only: regulator, NGOs\nBFT-type consensus", CO, CE)
box(dx[1], 10, dw, 19, "Smart contracts\nEscrow released on 'verified'\nAuto-hold on satellite alert\nMass-balance cap per refinery\nPremium / penalty payout", CO, CE)
box(dx[2], 10, dw, 19, "Governance and data rules\nMembership, voting, upgrades\nCommercial terms off-chain\nOracle challenge and disputes\nExit and data-portability terms", CO, CE)
for x in dx: arrow(x + dw / 2, 38.6, x + dw / 2, 29.4, col=CE, lw=1.4)
# bloomberg strip
box(2, 0.8, 96, 5.8, "Off-chain risk layer: Bloomberg SPLC / ESG / CN feeds → SPOEI supplier risk score → Tier-2 audit trigger (Ch. 6.3)", "#F3F4F6", "#6B7280", fs=6.9)
arrow(50, 9.6, 50, 6.9, col=MUTE, lw=1.0, style="<|-|>")
save(fig, "f08_architecture")
