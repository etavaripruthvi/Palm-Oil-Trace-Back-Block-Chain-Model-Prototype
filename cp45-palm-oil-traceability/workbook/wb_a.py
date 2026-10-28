from wb_common import *
from openpyxl.chart import LineChart, Reference
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "src"))
import palm_oil_traceability_model as M

YRS = ["2019", "2020", "2021", "2022", "2023", "2024", "2025"]
# company -> metric -> 7 values (2019..2025); None = n/a.  Source: Bloomberg FA screens (15-Oct-2026).
FUND = {
 "ULVR": dict(name="Unilever PLC (ULVR LN)", cur="EUR m", 
   rev=[51980,50724,52444,60073,59604,52479,50503], cogs=[29102,28684,30259,35906,34429,27976,26794],
   oi=[9947,9367,9636,9592,9931,10198,10084], intexp=[763,647,563,782,1075,1063,1104],
   pretax=[9493,9040,9564,9331,9654,9941,9808],
   inv=[4164,4462,4683,5931,5119,5177,4043], cash=[5072,6297,4495,5523,5853,7317,5012],
   rec=[4916,3433,3582,4544,4023,4227,4852], ppe=[12062,10558,10347,10770,10707,11669,8992],
   gw=[18067,18942,20330,21609,21109,22311,17709],
   ni=[5625,5581,6049,7642,6487,5744,9469], da=[1982,2018,1763,1946,1579,1382,1364],
   cfo=[7725,8791,7817,7010,9033,9269,8436], capex=[-1526,-1021,-1340,-1709,-1745,-1614,-1591],
   div=[-4209,-4279,-4483,-4329,-4363,-4319,-4453],
   ltm=dict(rev=50629.0, oi=None), est=dict(rev=(51834.8,53358.6), gp=(24245.7,25100.4), oi=(10455.8,10788.5), pretax=(9989.4,10316.7))),
 "NESN": dict(name="Nestlé SA (NESN SW)", cur="CHF m",
   rev=[92865,84681,87470,94780,93351,91720,89885], cogs=[46647,42971,45468,51745,50328,48670,48694],
   oi=[16047,14248,14902,15839,15865,15948,13947], intexp=[1124,831,815,1124,1500,1700,1683],
   pretax=[15031,13374,14029,14799,14505,14463,12421],
   inv=[9343,10101,11982,15019,11896,13260,12813], cash=[10263,8609,13995,6687,5851,7871,6230],
   rec=[9408,8087,8564,8795,8992,9414,8744], ppe=[28762,25840,28345,30141,30467,33706,32549],
   gw=[28896,27620,31012,31262,28693,30595,27636],
   ni=[12609,12232,16905,9270,11209,10884,9033], da=[3713,3465,3440,3541,3458,3582,3633],
   cfo=[15850,14377,13864,11907,15941,16675,15904], capex=[-4211,-4364,-5341,-5361,-6203,-5963,-4911],
   div=[-7230,-7700,-7681,-7618,-7829,-7816,-7849],
   ltm=dict(rev=88775.0), est=dict(rev=(90103.0,92208.1), gp=(41731.2,43139.6), oi=(14728.2,15083.4), pretax=(13274.7,14079.4))),
 "WIL": dict(name="Wilmar International (WIL SP)", cur="USD m",
   rev=[42640.5,50526.8,65793.6,73399.0,67155.3,67379.1,70415.7], cogs=[38154.4,44929.2,58602.4,66852.7,61882.1,62168.3,64619.9],
   oi=[1866.6,2215.6,2701.6,3190.2,2179.4,2526.3,2243.8], intexp=[922.7,651.1,588.4,872.1,1251.5,1266.7,1077.4],
   pretax=[1595.3,2363.2,2740.8,2920.9,1757.0,1900.1,1818.9],
   inv=[7970.2,9436.2,11738.7,13230.1,11801.7,12989.3,14652.6], cash=[4361.4,6214.9,6668.4,6084.6,8436.2,7374.9,7657.7],
   rec=[4251.6,5277.9,6833.4,6549.0,6384.5,7553.2,7351.2], ppe=[11945.5,13439.8,14830.6,15415.8,16310.1,16161.6,16897.6],
   gw=[3791.5,3868.0,3819.1,3832.2,3725.2,3619.4,5507.0],
   ni=[1293.4,1534.1,1890.4,2402.5,1524.8,1169.8,1410.9], da=[878.4,1058.0,1146.7,1153.4,1219.5,1298.8,1387.9],
   cfo=[3479.1,726.2,51.1,2149.5,4000.2,1441.1,2386.2], capex=[-1813.2,-1977.1,-2527.3,-2483.0,-2210.5,-1571.9,-1081.0],
   div=[-461.8,-618.6,-968.3,-755.4,-795.0,-796.3,-663.3],
   ltm=dict(rev=76083.6), est=dict(rev=(78654.0,83077.6), gp=(6386.7,6845.6), oi=(2662.3,2854.9), pretax=(2319.7,2488.4))),
}
ROW = {}   # ROW[co][metric] -> excel row number on Fundamentals

def build_fundamentals(wb):
    ws = wb.create_sheet("Fundamentals")
    title(ws, "Fundamentals — Bloomberg FA screens (transcribed)",
          "Blue = value typed from your Bloomberg screenshots (BBG Adjusted / Standardized, as of 15-Oct-2026). Black = formula. Reporting currencies differ (EUR / CHF / USD) — compare ratios, not levels.")
    r = 4
    for co, d in FUND.items():
        sec(ws, r, f"{d['name']}  —  {d['cur']}", 12)
        r += 1
        hdr(ws, r, ["Metric", "Unit"] + YRS + ["LTM 06/30/26", "2026E", "2027E"])
        r += 1
        R = {}
        def line(key, label, vals, ext=None, fmt=NUM):
            nonlocal r
            put(ws, (r, 1), label); put(ws, (r, 2), d["cur"] if fmt == NUM else "")
            for i, v in enumerate(vals):
                if v is not None: put(ws, (r, 3 + i), v, f_in, fmt)
                else: put(ws, (r, 3 + i), None)
            for j in range(3):
                put(ws, (r, 10 + j), None, f_in, fmt)
            if ext:
                for j, v in ext.items():
                    if v is not None: put(ws, (r, 10 + j), v, f_in, fmt)
            R[key] = r; r += 1
        e = d["est"]
        line("rev", "Revenue", d["rev"], {0: d["ltm"]["rev"], 1: e["rev"][0], 2: e["rev"][1]})
        line("cogs", "Cost of revenue", d["cogs"])
        # gross profit formula for history
        put(ws, (r, 1), "Gross profit"); put(ws, (r, 2), d["cur"])
        for i in range(7):
            put(ws, (r, 3 + i), f"={L(3+i)}{R['rev']}-{L(3+i)}{R['cogs']}", f_calc, NUM)
        put(ws, (r, 10), None); put(ws, (r, 11), e["gp"][0], f_in, NUM); put(ws, (r, 12), e["gp"][1], f_in, NUM)
        R["gp"] = r; r += 1
        line("oi", "Operating income (BBG adj.)", d["oi"], {1: e["oi"][0], 2: e["oi"][1]})
        line("intexp", "Interest expense", d["intexp"])
        line("pretax", "Pretax income, adjusted", d["pretax"], {1: e["pretax"][0], 2: e["pretax"][1]})
        line("inv", "Inventories (year-end)", d["inv"])
        line("cash", "Cash & ST investments", d["cash"])
        line("rec", "Accounts receivable", d["rec"])
        line("ppe", "PP&E, net", d["ppe"])
        line("gw", "Goodwill", d["gw"])
        line("ni", "Net income (cash-flow statement)", d["ni"])
        line("da", "Depreciation & amortisation", d["da"])
        line("cfo", "Cash from operations", d["cfo"])
        line("capex", "Capex (acq. fixed & intangibles)", d["capex"])
        line("div", "Dividends paid", d["div"])
        # derived
        put(ws, (r, 1), "— derived —", f_bold, fill=fill_note)
        for c in range(2, 13): put(ws, (r, c), None, fill=fill_note)
        r += 1
        def calc(key, label, fn, fmt, cols=range(7), ext=False):
            nonlocal r
            put(ws, (r, 1), label); put(ws, (r, 2), "")
            for i in range(12):
                put(ws, (r, 3 + i), None)
            for i in cols:
                put(ws, (r, 3 + i), fn(i), f_calc, fmt)
            R[key] = r; r += 1
        calc("g", "Revenue growth y/y", lambda i: f"={L(3+i)}{R['rev']}/{L(2+i)}{R['rev']}-1", PCT, range(1, 7))
        calc("gm", "Gross margin", lambda i: f"={L(3+i)}{R['gp']}/{L(3+i)}{R['rev']}", PCT)
        put(ws, (R["gm"], 11), f"=K{R['gp']}/K{R['rev']}", f_calc, PCT); put(ws, (R["gm"], 12), f"=L{R['gp']}/L{R['rev']}", f_calc, PCT)
        calc("om", "Operating margin", lambda i: f"={L(3+i)}{R['oi']}/{L(3+i)}{R['rev']}", PCT)
        put(ws, (R["om"], 11), f"=K{R['oi']}/K{R['rev']}", f_calc, PCT); put(ws, (R["om"], 12), f"=L{R['oi']}/L{R['rev']}", f_calc, PCT)
        calc("cov", "Interest cover (OI / interest)", lambda i: f"={L(3+i)}{R['oi']}/{L(3+i)}{R['intexp']}", MULT)
        calc("dio", "Inventory days (inv / COGS x 365)", lambda i: f"={L(3+i)}{R['inv']}/{L(3+i)}{R['cogs']}*365", NUM)
        calc("fcf", "Free cash flow (CFO + capex)", lambda i: f"={L(3+i)}{R['cfo']}+{L(3+i)}{R['capex']}", NUM)
        calc("fcfdiv", "FCF / dividends paid", lambda i: f"=IFERROR(-{L(3+i)}{R['fcf']}/{L(3+i)}{R['div']},0)", MULT)
        calc("capint", "Capex / revenue", lambda i: f"=-{L(3+i)}{R['capex']}/{L(3+i)}{R['rev']}", PCT)
        ROW[co] = R
        r += 2
    widths(ws, {"A": 36, "B": 9, **{L(i): 12 for i in range(3, 13)}})
    ws.freeze_panes = "C4"
    note(ws, f"A{r}", "Caveats: (1) Unilever FY2024-25 revenue is restated for the ice-cream demerger, so 2023→2024 'growth' is a perimeter change, not trading. "
         "(2) Nestlé 2019-21 include large disposal gains in net income. (3) Wilmar 2019 CFO is a working-capital swing. Spot-check any figure you cite against the Terminal.")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=12); ws.row_dimensions[r].height = 42
    return ws


SNAP = [  # label, fmt, WIL, NESN, ULVR   (Bloomberg DES / profile screens, 15-Oct-2026)
 ("Price, last (local ccy; ULVR in GBp)", NUM2, 3.47, 78.89, 4829.0),
 ("1-day change %", PCT, -0.0114, 0.0206, 0.0252),
 ("52-week high", NUM2, 4.02, 87.09, 5525.0),
 ("52-week low", NUM2, 2.88, 70.29, 4068.0),
 ("YTD change %", PCT, 0.1266, 0.0019, -0.0063),
 ("Market cap (local ccy m; SGD / CHF / GBP)", NUM0, 21667.6, 203261.7, 104032.5),
 ("P/E (trailing)", NUM2, 11.82, 27.28, 22.58),
 ("Est. P/E (FY Dec-26)", NUM2, 10.74, 17.70, 17.50),
 ("T12M EPS (USD / CHF / EUR)", NUM2, 0.23, 2.89, 2.52),
 ("Est. EPS", NUM2, 0.25, 4.46, 3.26),
 ("Est. PEG", NUM2, 2.71, 3.47, 3.90),
 ("Indicated gross dividend yield", PCT, 0.0432, 0.0393, 0.0330),
 ("5Y net dividend growth", PCT, -0.0606, 0.0242, -0.0033),
 ("12M total return", PCT, 0.2447, 0.0781, 0.0338),
 ("Beta vs local index (STI / SMI / UKX)", NUM2, 0.60, 0.86, 0.62),
 ("Employees (12/31/25)", NUM0, 100000, 271000, 118000),
 ("5Y price high (Bloomberg HP table)", NUM2, 4.87, 129.50, 5472.0),
 ("5Y price low", NUM2, 2.85, 71.00, 4078.0),
 ("5Y average price", NUM2, 3.62, 96.07, 4690.64),
 ("5Y net change %", PCT, -0.1895, -0.3238, -0.0008),
 ("30-day volatility (Bloomberg chart, % ann.)", NUM2, 20.5669, 20.8245, 19.7499),
 ("90-day volatility (Bloomberg chart, % ann.)", NUM2, 21.6096, 23.9151, 23.1949),
]
SNAPROW = {}

def build_market(wb):
    ws = wb.create_sheet("Market_Data")
    title(ws, "Market snapshot — Bloomberg profile / HP / GP screens",
          "Blue = typed from screenshots. Wilmar price table range ends 10/09; header quote 3.47 is later. Check the 'as of' date before quoting.")
    hdr(ws, 4, ["Metric", "Wilmar (WIL SP)", "Nestlé (NESN SW)", "Unilever (ULVR LN)"])
    for i, (lab, fmt, a, b, c) in enumerate(SNAP):
        rr = 5 + i
        put(ws, (rr, 1), lab)
        for j, v in enumerate((a, b, c)):
            put(ws, (rr, 2 + j), v, f_in, fmt)
        SNAPROW[lab] = rr
    r = 5 + len(SNAP) + 1
    sec(ws, r, "Palm oil futures — KOZ6 Comdty (Bursa Malaysia CPO, Dec-26), MYR / tonne", 4); r += 1
    cpo = [("Last (15-Oct-26)", 4666.0, NUM), ("Previous close", 4700.0, NUM), ("Day high / low", "4,737 / 4,621", None),
           ("Open interest (contracts)", 89521, NUM0),
           ("Range high 12/15/25–10/15/26 (09/08/26)", 5115.0, NUM), ("Range low (12/19/25)", 3911.0, NUM),
           ("Range average", 4511.68, NUM2), ("Net change over range", 706.0, NUM), ("Net change %", 0.1783, PCT)]
    for lab, v, fmt in cpo:
        put(ws, (r, 1), lab); put(ws, (r, 2), v, f_in, fmt); r += 1
    put(ws, (r, 1), "Drawdown from range high (formula)"); put(ws, (r, 2), f"=B{r-9}/B{r-5}-1", f_calc, PCT); r += 2
    note(ws, f"A{r}", "Bloomberg ticker note: your screens use KOZ6 Comdty (a single contract month). For a continuous history use the generic first-month series (KO1 Comdty — confirm with the Terminal search) "
         "and state the roll rule. The draft plan's 'KOA Comdty' does not match what you actually pulled.")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=4); ws.row_dimensions[r].height = 44
    widths(ws, {"A": 52, "B": 20, "C": 20, "D": 20})
    ws.freeze_panes = "B5"
    return ws

PRICE_FIRST = 7
def build_prices(wb):
    ws = wb.create_sheet("Price_Analytics")
    title(ws, "Price analytics — CPO futures vs the three equities",
          "Daily closes 17-Aug to 15-Oct-2026 typed from the HP tables. Returns are log returns, computed only where both days printed. Only ~8 weeks of data: treat statistics as a demo of method, not evidence.")
    df = M.price_frame()
    hdr(ws, 6, ["Date", "CPO KOZ6 (MYR/t)", "WIL SP (SGD)", "NESN SW (CHF)", "ULVR LN (GBp)",
                "ret CPO", "ret WIL", "ret NESN", "ret ULVR", "CPO (rebased)", "WIL (rebased)", "NESN (rebased)", "ULVR (rebased)"], height=30)
    n = len(df)
    last = PRICE_FIRST + n - 1
    for i, (dt, row) in enumerate(df.iterrows()):
        r = PRICE_FIRST + i
        put(ws, (r, 1), dt.to_pydatetime(), f_in, "dd-mmm-yy")
        for j, c in enumerate(["CPO", "WIL", "NESN", "ULVR"]):
            v = row[c]
            put(ws, (r, 2 + j), None if v != v else float(v), f_in, NUM2)
            col = L(2 + j)
            if i == 0:
                put(ws, (r, 6 + j), None); 
                put(ws, (r, 10 + j), f"={col}{r}/{col}${PRICE_FIRST}*100", f_calc, NUM)
            else:
                put(ws, (r, 6 + j), f'=IF(AND(ISNUMBER({col}{r}),ISNUMBER({col}{r-1})),LN({col}{r}/{col}{r-1}),"")', f_calc, '0.00%')
                put(ws, (r, 10 + j), f"=IF(ISNUMBER({col}{r}),{col}{r}/{col}${PRICE_FIRST}*100,{L(10+j)}{r-1})", f_calc, NUM)
    # stats block
    put(ws, "O6", "Statistic", f_hdr, fill=fill_hdr); 
    for j, h in enumerate(["CPO", "WIL", "NESN", "ULVR"]):
        put(ws, (6, 16 + j), h, f_hdr, fill=fill_hdr, align=center)
    stats = [("Return observations (n)", "=COUNT({c}{a}:{c}{b})", '0'),
             ("Annualised volatility (x sqrt 252)", "=STDEV({c}{a}:{c}{b})*SQRT(252)", PCT),
             ("Correlation vs CPO returns", "=CORREL({c}{a}:{c}{b},$F${a}:$F${b})", NUM2),
             ("Beta vs CPO returns", "=SLOPE({c}{a}:{c}{b},$F${a}:$F${b})", NUM2),
             ("Pairs used with CPO", "=SUMPRODUCT(ISNUMBER({c}{a}:{c}{b})*ISNUMBER($F${a}:$F${b}))", '0'),
             ("Approx. 95% band on correlation (±2/√n)", "=2/SQRT(P12)", NUM2)]
    a, b = PRICE_FIRST + 1, last
    for k, (lab, f, fmt) in enumerate(stats):
        r = 7 + k
        put(ws, (r, 15), lab)
        for j in range(4):
            c = L(6 + j)
            if lab.startswith("Correlation") or lab.startswith("Beta") or lab.startswith("Pairs") :
                if j == 0:
                    put(ws, (r, 16), "n/a", f_sub); continue
            if lab.startswith("Approx"):
                if j == 0: put(ws, (r, 16), "n/a", f_sub); continue
                put(ws, (r, 16 + j), f"=2/SQRT({L(16+j)}11)", f_calc, fmt); continue
            put(ws, (r, 16 + j), f.format(c=c, a=a, b=b), f_calc, fmt)
    put(ws, "O14", "Reading: |corr| below the ±2/√n band is statistically indistinguishable from zero.", f_sub, border=False)
    put(ws, "O15", "Next step: pull ≥5Y daily history with BDH() / BQL and rerun (see Next_Steps sheet).", f_sub, border=False)
    widths(ws, {"A": 11, **{L(i): 13 for i in range(2, 14)}, "N": 3, "O": 40, "P": 11, "Q": 11, "R": 11, "S": 11})
    ws.freeze_panes = "B7"
    ch = LineChart(); ch.title = "Rebased prices (17-Aug-26 = 100)"; ch.height = 8.5; ch.width = 20
    ch.y_axis.title = "Index"; ch.y_axis.scaling.min = 90; ch.y_axis.scaling.max = 115
    ch.add_data(Reference(ws, min_col=10, max_col=13, min_row=6, max_row=last), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=PRICE_FIRST, max_row=last))
    ch.x_axis.number_format = "dd-mmm"; ch.x_axis.delete = False; ch.y_axis.delete = False
    ws.add_chart(ch, "O18")
    return ws

ESG = {  # BESG / GHG series 2016..2025 (None = '--').  Bloomberg ESG screens.
 "years": ["2016","2017","2018","2019","2020","2021","2022","2023","2024","2025"],
 "WIL": dict(besg=[2.71,2.76,3.06,3.74,4.90,5.12,6.29,5.97,6.15,None], env=[1.87,2.08,2.60,4.14,6.20,6.61,7.17,6.71,6.59,None],
             soc=[2.45,2.32,2.31,2.28,3.26,3.29,6.31,5.59,6.46,None], gov=[4.68,4.58,4.81,4.72,4.60,4.78,4.90,5.16,5.16,None],
             s1=[3550.5,3937.4,4888.0,4955.5,6711.1,8300.0,9000.0,8700.0,8300.0,9100.0],
             s2=[573.6,593.9,623.5,681.2,4523.1,4273.4,3800.0,5300.0,4000.0,None],
             s3=[None,None,None,None,None,None,160556.0,151000.0,147000.0,None]),
 "NESN": dict(besg=[4.54,4.92,5.03,5.94,6.17,5.01,5.14,5.23,5.28,None], env=[5.41,4.72,4.79,5.83,5.82,4.62,4.72,5.06,5.18,None],
             soc=[2.44,3.82,3.95,5.27,6.30,3.72,3.95,3.89,4.11,None], gov=[5.84,6.42,6.56,6.79,6.51,7.07,7.09,6.97,6.71,None],
             s1=[3607.9,3532.1,3210.0,3246.4,3310.0,3420.0,3230.0,3060.0,3020.0,2820.0],
             s2=[3736.6,3639.0,2380.0,3089.0,3052.2,2600.0,2612.7,2583.4,2420.0,2480.0],
             s3=[105793.0,106926.0,81940.0,107411.0,99430.0,88910.0,79850.0,69980.0,68000.0,72010.0]),
 "ULVR": dict(besg=[3.92,4.03,4.24,4.28,4.56,4.41,4.68,4.91,4.82,None], env=[3.15,3.68,4.14,4.61,5.13,4.65,4.95,5.29,5.51,None],
             soc=[1.31,1.32,1.32,1.35,1.46,1.49,2.08,2.12,2.08,None], gov=[8.57,8.25,8.48,7.96,8.17,8.15,7.74,8.09,7.59,None],
             s1=[860.2,820.4,758.2,659.0,606.8,730.0,640.0,570.0,480.0,430.0],
             s2=[1501.4,938.9,1430.7,1098.6,1264.3,None,1260.0,1160.0,1260.0,820.0],
             s3=[61543.2,60398.6,62017.6,61020.4,114634.0,120213.0,52820.0,102880.0,107960.0,103770.0]),
}
ESGROW = {}
def build_esg(wb):
    ws = wb.create_sheet("ESG")
    title(ws, "ESG — Bloomberg BESG scores (0–10, higher = better) and GHG emissions",
          "Blue = typed from ESG screens. GHG units as shown by Bloomberg (verify; likely '000 tCO2e). Series breaks flagged below.")
    r = 4
    names = {"WIL": "Wilmar (WIL SP)", "NESN": "Nestlé (NESN SW)", "ULVR": "Unilever (ULVR LN)"}
    labs = [("besg", "BESG ESG score", NUM2), ("env", "BESG Environmental pillar", NUM2), ("soc", "BESG Social pillar", NUM2),
            ("gov", "BESG Governance pillar", NUM2), ("s1", "GHG Scope 1", NUM0), ("s2", "GHG Scope 2 (location-based)", NUM0),
            ("s3", "GHG Scope 3", NUM0)]
    for co in ("WIL", "NESN", "ULVR"):
        sec(ws, r, names[co], 12); r += 1
        hdr(ws, r, ["Metric"] + ESG["years"] + ["% change first→last"]); r += 1
        ESGROW[co] = {}
        for key, lab, fmt in labs:
            put(ws, (r, 1), lab)
            vals = ESG[co][key]
            for i, v in enumerate(vals):
                put(ws, (r, 2 + i), v, f_in, fmt)
            # change between first and last available value
            put(ws, (r, 12), f'=IFERROR(LOOKUP(2,1/ISNUMBER(B{r}:K{r}),B{r}:K{r})/INDEX(B{r}:K{r},MATCH(TRUE,INDEX(ISNUMBER(B{r}:K{r}),0),0))-1,"")', f_calc, '0%')
            ESGROW[co][key] = r; r += 1
        r += 1
    note(ws, f"A{r}", "Why this matters for the capstone: Wilmar's BESG score rose from 2.71 (2016) to 6.15 (2024) while its reported Scope 1 more than doubled (3,551 → 9,100). "
         "That pattern points to disclosure improving, not footprint falling — so a BESG score alone is a weak predictor of traceability risk (RQ1). "
         "Series breaks: Unilever Scope 3 jumps 61,020 (2019) → 114,634 (2020) → 52,820 (2022) → 102,880 (2023) — a methodology/perimeter change, not real movement. Do not trend across it. "
         "Wilmar Scope 3 is missing before 2022 and for 2025; Scope 2 market-based figures exist but are omitted here.")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=12); ws.row_dimensions[r].height = 78
    r += 2
    ch = LineChart(); ch.title = "BESG ESG score"; ch.height = 7.5; ch.width = 18
    for co in ("WIL", "NESN", "ULVR"):
        rr = ESGROW[co]["besg"]
        from openpyxl.chart import Series
        s = Series(Reference(ws, min_col=2, max_col=10, min_row=rr), title=names[co]); ch.series.append(s)
    ch.set_categories(Reference(ws, min_col=2, max_col=10, min_row=5))
    ch.x_axis.delete = False; ch.y_axis.delete = False; ch.y_axis.scaling.min = 0; ch.y_axis.scaling.max = 8
    ws.add_chart(ch, f"A{r}")
    widths(ws, {"A": 34, **{L(i): 10 for i in range(2, 12)}, "L": 12})
    ws.freeze_panes = "B4"
    return ws
