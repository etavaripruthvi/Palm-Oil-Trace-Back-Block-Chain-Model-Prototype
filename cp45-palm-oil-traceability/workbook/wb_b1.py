from wb_common import *

SPLC = [  # label, fmt, WIL, NESN, ULVR   (Bloomberg SPLC summary panels, as of 15-Oct-2026)
 ("Suppliers listed (count)", NUM0, 30, 508, 287),
 ("Customers listed (count)", NUM0, 17, 172, 126),
 ("Suppliers with sanctions", NUM0, 1, 2, 1),
 ("Customers with sanctions", NUM0, 0, 3, 1),
 ("Suppliers distressed", NUM0, 0, 13, 4),
 ("Customers distressed", NUM0, 1, 4, 3),
 ("Suppliers = ESG-score laggards (count)", NUM0, 1, 21, 13),
 ("Suppliers = business-conduct risk (count)", NUM0, 11, 54, 40),
 ("Suppliers = high GHG vs peers (count)", NUM0, 4, 99, 59),
 ("Suppliers = high physical risk (count)", NUM0, 2, 11, 6),
 ("Suppliers = high water stress (count)", NUM0, 5, 71, 72),
]
SPLCROW = {}
GEO = {"WIL": [("China", .4733, .2825, .1761), ("Indonesia", .0444, .2177, .0344), ("Malaysia", .0353, .1089, .0800), ("Australia", .0327, .0968, .0172), ("India", .0389, .0685, .0273)],
       "NESN": [("USA", .3392, .2549, .3249), ("Brazil", .0226, .0562, .0271), ("France", None, .0475, .0396), ("Chile", None, .0367, .0096), ("United Kingdom", None, .0367, .0452)],
       "ULVR": [("India", .0433, .2283, .0491), ("USA", .2055, .0868, .3157), ("United Kingdom", .1474, .0502, .0451), ("Brazil", .0747, .0457, .0246), ("China", .1967, .0365, .0907)]}
COMM = {"WIL": [("Sugar", .3190), ("Polyethylene", .2120), ("Rice", .2064), ("Biofuel", -.1654), ("Eggs", -.1559)],
        "NESN": [("Barley", .5257), ("Sugar", .3190), ("Maize", .2651), ("Fish", .2638), ("Polyethylene", .2133)],
        "ULVR": [("Diesel", .5184), ("Sugar", .3190), ("Crude", .2250), ("Polyethylene", .2137), ("Biofuel", -.1654)]}

# Wilmar suppliers: name, supplier's revenue % from Wilmar, WIL cost % (None = '--'), cost type, 3M price chg, palm node, related party
WSUP = [
 ("Yihai Kerry Arawana Holdings", .0253, .0128, "COGS", -.0087, "N", "Y"),
 ("Wilmar Cahaya Indonesia Tbk PT", .4800, .0042, "COGS", .0046, "N", "Y"),
 ("Shree Renuka Sugars", .1702, .0025, "COGS", -.0009, "N", "N"),
 ("Dharma Satya Nusantara Tbk PT", .1272, .0014, "COGS", .1818, "Y", "N"),
 ("GPT Group/The", .0059, .0012, "SGA", -.0438, "N", "N"),
 ("Ecolab Inc", .0032, .0008, "COGS", .0646, "N", "N"),
 ("AEP Pinago Plantations Tbk PT", .3861, .0007, "COGS", -.0805, "Y", "N"),
 ("Bakrie Sumatera Plantations Tbk PT", .2206, .0005, "COGS", .5340, "Y", "N"),
 ("Kencana Agri Ltd", .1387, .0004, "COGS", .1875, "Y", "N"),
 ("Gozco Plantations Tbk PT", .4733, .0004, "COGS", -.0068, "Y", "N"),
 ("PPB Group Bhd", .0150, .0003, "COGS", -.0617, "N", "N"),
 ("SIS Ltd", .0007, .0003, "SGA", -.0810, "N", "N"),
 ("Eagle High Plantations Tbk PT", .0459, .0003, "COGS", .2800, "Y", "N"),
 ("Andira Agro Tbk PT", .9939, .0003, "COGS", .2222, "Y", "N"),
 ("Cisadane Sawit Raya Tbk PT", .1124, .0002, "COGS", -.0658, "Y", "N"),
 ("AWL Agri Business Ltd", .0013, .0002, "COGS", .0082, "N", "Y"),
 ("Clariant AG", .0018, .0001, "COGS", .3406, "N", "N"),
 ("Cosan SA", None, None, "", .2875, "N", "N"),
 ("Icents Group Holdings Bhd", None, None, "", .2109, "N", "N"),
 ("Mitra Pack Tbk PT", None, None, "", -.2459, "N", "N"),
 ("Sawit Sumbermas Sarana Tbk PT", None, None, "", .1648, "Y", "N"),
 ("Humpuss Intermoda Transportasi Tbk PT", None, None, "", None, "N", "N"),
 ("Astra Agro Lestari Tbk PT", None, None, "", .3571, "Y", "N"),
 ("Wijaya Karya Beton Tbk PT", None, None, "", -.0811, "N", "N"),
]
NSUP = [  # name, supplier rev %, cost %, type, 3M, category
 ("Amcor PLC", .0547, .0217, "COGS", -.0258, "Packaging"), ("Silgan Holdings", .1400, .0154, "COGS", -.2143, "Packaging"),
 ("International Flavors & Fragrances", .0595, .0117, "COGS", .1897, "Flavours/ingredients"), ("Telefonaktiebolaget LM Ericsson", .0021, .0106, "CAPEX", -.0021, "Technology"),
 ("Ball Corp", .0378, .0093, "COGS", -.0061, "Packaging"), ("Crown Holdings", .0319, .0069, "COGS", -.0040, "Packaging"),
 ("Alibaba Group Holding", .0013, .0067, "SGA", -.0554, "Technology"), ("Givaudan SA", .0437, .0063, "COGS", .1283, "Flavours/ingredients"),
 ("Barry Callebaut AG", .0144, .0043, "COGS", -.0676, "Flavours/ingredients"), ("Symrise AG", .0376, .0038, "COGS", .1061, "Flavours/ingredients"),
 ("Daetwyler Holding AG", .1568, .0037, "COGS", -.1210, "Industrial"), ("Keurig Dr Pepper", .0129, .0036, "COGS", .0938, "Beverage"),
 ("Eastman Chemical", .0208, .0033, "COGS", -.0732, "Chemicals"), ("O-I Glass", .0245, .0029, "COGS", -.3876, "Packaging"),
 ("Huhtamaki Oyj", .0360, .0028, "COGS", .0304, "Packaging"), ("DSM-Firmenich AG", .0115, .0027, "COGS", .2196, "Flavours/ingredients"),
 ("ID Logistics Group", .0345, .0025, "COGS", -.0837, "Logistics"), ("Oracle Corp", .0017, .0020, "COGS", -.0146, "Technology"),
 ("Graphic Packaging Holding", .0149, .0020, "COGS", -.2019, "Packaging"), ("AptarGroup Inc", .0278, .0016, "COGS", -.0685, "Packaging"),
 ("XPO Inc", .0091, .0014, "COGS", -.0963, "Logistics"), ("Nestle India Ltd", .0278, .0013, "COGS", -.0392, "Related party"),
 ("Air Liquide SA", .0021, .0012, "COGS", -.0274, "Industrial"), ("Jabil Inc", .0018, .0010, "COGS", -.0792, "Technology"),
]
USUP = [
 ("Alibaba Group Holding", .0120, .0528, "SGA", -.0554, "Technology"), ("Barry Callebaut AG", .0420, .0248, "COGS", -.0676, "Flavours/ingredients"),
 ("International Flavors & Fragrances", .0437, .0130, "COGS", .1897, "Flavours/ingredients"), ("Amcor PLC", .0186, .0112, "COGS", -.0258, "Packaging"),
 ("Symrise AG", .0461, .0087, "COGS", .1061, "Flavours/ingredients"), ("Dassault Systemes SE", .0016, .0075, "CAPEX", .2190, "Technology"),
 ("Givaudan SA", .0238, .0068, "COGS", .1283, "Flavours/ingredients"), ("Huhtamaki Oyj", .0473, .0055, "COGS", .0304, "Packaging"),
 ("DSM-Firmenich AG", .0104, .0040, "COGS", .2196, "Flavours/ingredients"), ("AptarGroup Inc", .0337, .0040, "COGS", -.0685, "Packaging"),
 ("Silgan Holdings", .0213, .0035, "COGS", -.2143, "Packaging"), ("Ball Corp", .0084, .0031, "COGS", -.0061, "Packaging"),
 ("Keurig Dr Pepper", .0060, .0026, "COGS", .0938, "Beverage"), ("ID Logistics Group", .0159, .0023, "COGS", -.0837, "Logistics"),
 ("Jacobs Solutions", .0050, .0023, "SGA", .0952, "Technology"), ("Oracle Corp", .0008, .0021, "COGS", -.0146, "Technology"),
 ("Air Liquide SA", .0023, .0019, "COGS", -.0274, "Industrial"), ("Unilever Indonesia Tbk PT", .0277, .0019, "COGS", -.0509, "Related party"),
 ("O-I Glass", .0089, .0016, "COGS", -.3876, "Packaging"), ("Galaxy Surfactants", .0979, .0016, "COGS", .3004, "Chemicals"),
 ("Mondelez International", .0014, .0014, "COGS", .0656, "Beverage"), ("EPL Ltd", .0536, .0011, "COGS", -.0185, "Packaging"),
 ("Graphic Packaging Holding", .0044, .0010, "COGS", -.2019, "Packaging"), ("Ecolab Inc", .0024, .0010, "COGS", .0646, "Chemicals"),
]
CUST_TOP10 = {"NESN": [.0771, .0273, .0266, .0261, .0247, .0239, .0227, .0214, .0182, .0133],
              "ULVR": [.0712, .0278, .0211, .0157, .0154, .0148, .0121, .0104, .0094, .0090]}
SC = {}   # cell registry for the risk sheet

def build_supply(wb):
    ws = wb.create_sheet("Supply_Chain")
    title(ws, "Supply chain — Bloomberg SPLC (as of 15-Oct-2026)",
          "Blue = typed from SPLC screens. Only the rows visible on screen were captured, so every 'coverage' figure is a LOWER bound on what SPLC holds.")
    r = 4
    sec(ws, r, "A. SPLC summary panels", 8); r += 1
    hdr(ws, r, ["Metric", "Wilmar", "Nestlé", "Unilever"]); r += 1
    for lab, fmt, a, b, c in SPLC:
        put(ws, (r, 1), lab)
        for j, v in enumerate((a, b, c)): put(ws, (r, 2 + j), v, f_in, fmt)
        SPLCROW[lab] = r; r += 1
    base = SPLCROW["Suppliers listed (count)"]
    derived = [("Sanctioned + distressed suppliers, % of suppliers", lambda c: f"=({c}{SPLCROW['Suppliers with sanctions']}+{c}{SPLCROW['Suppliers distressed']})/{c}{base}", PCT, "sanc_dist"),
               ("Business-conduct-risk suppliers, %", lambda c: f"={c}{SPLCROW['Suppliers = business-conduct risk (count)']}/{c}{base}", PCT, "conduct"),
               ("High-GHG suppliers, %", lambda c: f"={c}{SPLCROW['Suppliers = high GHG vs peers (count)']}/{c}{base}", PCT, "ghg"),
               ("ESG-laggard suppliers, %", lambda c: f"={c}{SPLCROW['Suppliers = ESG-score laggards (count)']}/{c}{base}", PCT, "lag"),
               ("High-water-stress suppliers, %", lambda c: f"={c}{SPLCROW['Suppliers = high water stress (count)']}/{c}{base}", PCT, "water")]
    for lab, fn, fmt, key in derived:
        put(ws, (r, 1), lab, f_bold)
        for j, c in enumerate("BCD"): put(ws, (r, 2 + j), fn(c), f_calc, fmt)
        SC[key] = r; r += 1
    r += 1
    sec(ws, r, "B. Geography (revenue / own facilities / supplier facilities, % of total)", 8); r += 1
    for co, nm in (("WIL", "Wilmar"), ("NESN", "Nestlé"), ("ULVR", "Unilever")):
        hdr(ws, r, [nm, "Revenue %", "Facilities %", "Supplier facilities %"]); r += 1
        for ctry, a, b, c in GEO[co]:
            put(ws, (r, 1), ctry)
            for j, v in enumerate((a, b, c)): put(ws, (r, 2 + j), v, f_in, PCT)
            r += 1
        r += 1
    note(ws, f"A{r}", "Read-across: 47% of Wilmar's revenue is China; EU exposure is indirect (via customers). EUDR pressure reaches Wilmar through Unilever/Nestlé-type buyers, not through Wilmar's own EU sales — the ROI sheets use a low EU share for Wilmar for this reason.")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); ws.row_dimensions[r].height = 40; r += 2
    sec(ws, r, "C. Commodity exposures shown by SPLC (3-month price change)", 8); r += 1
    hdr(ws, r, ["Rank", "Wilmar", "3M chg", "Nestlé", "3M chg", "Unilever", "3M chg"]); r += 1
    for i in range(5):
        put(ws, (r, 1), i + 1)
        for j, co in enumerate(("WIL", "NESN", "ULVR")):
            put(ws, (r, 2 + 2 * j), COMM[co][i][0], f_in); put(ws, (r, 3 + 2 * j), COMM[co][i][1], f_in, PCT)
        r += 1
    note(ws, f"A{r}", "Palm oil is NOT among SPLC's top-5 commodity exposures for any of the three firms. For Unilever/Nestlé it is a small share of total COGS, so the investment case rests on regulatory, Scope 3 and reputational exposure — not on input-cost savings.")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); ws.row_dimensions[r].height = 40; r += 2

    # ---- D. Wilmar suppliers
    sec(ws, r, "D. Wilmar — suppliers visible on screen (24 of 30)", 8); r += 1
    hdr(ws, r, ["Supplier", "Supplier's revenue % from Wilmar", "Wilmar cost % (COGS/SGA)", "Type", "3M price chg", "Palm/plantation node? (Y/N)", "Related party / JV? (Y/N, verify)", "Cost share ex-related"], height=44); r += 1
    a = r
    for nm, rv, cs, ty, ch, pn, rp in WSUP:
        put(ws, (r, 1), nm); put(ws, (r, 2), rv, f_in, PCT); put(ws, (r, 3), cs, f_in, '0.00%'); put(ws, (r, 4), ty, f_in)
        put(ws, (r, 5), ch, f_in, PCT); put(ws, (r, 6), pn, f_in, align=center); put(ws, (r, 7), rp, f_in, align=center)
        put(ws, (r, 8), f'=IF(G{r}="N",N(C{r}),0)', f_calc, '0.00%'); r += 1
    b = r - 1
    SC["w_a"], SC["w_b"] = a, b
    stats = [("Visible supplier cost, % of Wilmar COGS+SGA (lower bound)", f"=SUM(C{a}:C{b})", '0.00%', "w_cov"),
             ("  of which palm / plantation nodes", f'=SUMIF(F{a}:F{b},"Y",C{a}:C{b})', '0.00%', "w_palm"),
             ("Palm/plantation nodes visible (count)", f'=COUNTIF(F{a}:F{b},"Y")', '0', "w_palmn"),
             ("Cost-weighted dependence of palm nodes on Wilmar (buyer leverage)", f'=SUMPRODUCT((F{a}:F{b}="Y")*C{a}:C{b}*B{a}:B{b})/SUMIF(F{a}:F{b},"Y",C{a}:C{b})', PCT, "w_lev"),
             ("HHI of visible cost shares, ex related parties (0–10,000)", f"=SUMPRODUCT(H{a}:H{b}^2)/SUM(H{a}:H{b})^2*10000", NUM0, "w_hhi"),
             ("Top-3 share of visible cost, ex related parties", f"=(LARGE(H{a}:H{b},1)+LARGE(H{a}:H{b},2)+LARGE(H{a}:H{b},3))/SUM(H{a}:H{b})", PCT, "w_top3")]
    for lab, f, fmt, key in stats:
        put(ws, (r, 1), lab, f_bold); put(ws, (r, 2), f, f_calc, fmt, fill=fill_key if key in ("w_palm", "w_lev") else None)
        SC[key] = r; r += 1
    note(ws, f"A{r}", "Finding: the plantation/mill nodes Bloomberg can see make up a few hundredths of one percent of Wilmar's cost base, yet palm products dominate Wilmar's business. "
         "Most palm is bought from third-party mills and smallholders that SPLC does not cover — which is the traceability gap the capstone is about. "
         "Palm-node and related-party flags are my judgement from company names; verify before use. Yihai Kerry Arawana, Wilmar Cahaya and AWL Agri are group companies or JVs.")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); ws.row_dimensions[r].height = 66; r += 2

    # ---- E / F. brand-owner suppliers
    for key, nm, data in (("n", "Nestlé", NSUP), ("u", "Unilever", USUP)):
        sec(ws, r, f"{'E' if key=='n' else 'F'}. {nm} — top 24 suppliers by cost share (SPLC)", 8); r += 1
        hdr(ws, r, ["Supplier", "Supplier's revenue % from " + nm, nm + " cost %", "Type", "3M price chg", "Category (my coding)"], height=44); r += 1
        a = r
        for nme, rv, cs, ty, ch, cat in data:
            put(ws, (r, 1), nme); put(ws, (r, 2), rv, f_in, PCT); put(ws, (r, 3), cs, f_in, '0.00%'); put(ws, (r, 4), ty, f_in)
            put(ws, (r, 5), ch, f_in, PCT); put(ws, (r, 6), cat, f_in); r += 1
        b = r - 1
        SC[key + "_a"], SC[key + "_b"] = a, b
        for lab, f, fmt, k2 in [("Visible supplier cost, % of COGS (lower bound)", f"=SUM(C{a}:C{b})", '0.00%', "cov"),
                                ("Palm / edible-oil / plantation nodes visible (count)", f'=COUNTIF(F{a}:F{b},"Palm*")', '0', "palmn"),
                                ("Packaging share of visible cost", f'=SUMIF(F{a}:F{b},"Packaging",C{a}:C{b})/SUM(C{a}:C{b})', PCT, "pack"),
                                ("HHI of visible cost shares (0–10,000)", f"=SUMPRODUCT(C{a}:C{b}^2)/SUM(C{a}:C{b})^2*10000", NUM0, "hhi")]:
            put(ws, (r, 1), lab, f_bold); put(ws, (r, 2), f, f_calc, fmt, fill=fill_key if k2 == "palmn" else None)
            SC[key + "_" + k2] = r; r += 1
        r += 1
    note(ws, f"A{r}", "Finding: none of the top-24 suppliers of Unilever or Nestlé is a palm oil trader, refiner or plantation, and Wilmar is not in either visible list (nor are Unilever/Nestlé among Wilmar's visible customers). "
         "So the draft's chain 'mill → Wilmar → Unilever/Nestlé' is NOT evidenced by SPLC. Your own news screen shows Nestlé renewing a palm partnership with Musim Mas and AAK (Jul-2025). "
         "Action: search the full SPLC supplier list for Wilmar / IOI / Musim Mas / AAK / Cargill, and add each brand owner's published mill and supplier lists as a second source.")
    ws.merge_cells(start_row=r, start_column=1, end_row=r, end_column=8); ws.row_dimensions[r].height = 66; r += 2
    sec(ws, r, "G. Customer concentration — top-10 retail customers, share of revenue", 8); r += 1
    hdr(ws, r, ["", "Nestlé", "Unilever"]); r += 1
    for i in range(10):
        put(ws, (r, 1), f"Customer #{i+1}")
        put(ws, (r, 2), CUST_TOP10["NESN"][i], f_in, PCT); put(ws, (r, 3), CUST_TOP10["ULVR"][i], f_in, PCT); r += 1
    put(ws, (r, 1), "Top-10 total", f_bold)
    put(ws, (r, 2), f"=SUM(B{r-10}:B{r-1})", f_calc, PCT); put(ws, (r, 3), f"=SUM(C{r-10}:C{r-1})", f_calc, PCT)
    SC["top10"] = r
    widths(ws, {"A": 62, "B": 18, "C": 18, "D": 16, "E": 14, "F": 20, "G": 20, "H": 16})
    ws.freeze_panes = "B4"
    return ws
