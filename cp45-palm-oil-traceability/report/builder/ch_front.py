from lib import *
import json
N = J("nums.json"); det = N["det"]
mcdf = {(r["profile"], r["regime"], r["option"]): r for r in N["mc"]}

def cover(doc):
    for _ in range(3): pfmt(doc.add_paragraph(), 0, 18)
    p = doc.add_paragraph(); runs(p, "WOXSEN UNIVERSITY  ·  MBA (BUSINESS ANALYTICS)", 10, TEAL, bold=True); pfmt(p, 0, 2, 1.0, False, WD_ALIGN_PARAGRAPH.LEFT)
    p = doc.add_paragraph(); runs(p, "Blockchain Supply Chain & Predictive Analytics  ·  Bloomberg Capstone Project CP-45", 10, GREY); pfmt(p, 0, 36, 1.0, False, WD_ALIGN_PARAGRAPH.LEFT)
    p = doc.add_paragraph(); runs(p, "Blockchain Sustainable Palm Oil Traceability", 32, NAVY, bold=True); pfmt(p, 0, 8, 1.0, False, WD_ALIGN_PARAGRAPH.LEFT)
    para_border_bottom(p, "0B6E8A", 18, 8)
    p = doc.add_paragraph(); runs(p, "Assessing EUDR and Scope 3 risk with Bloomberg supply-chain data, a composite exposure index, and a Monte Carlo stress test of central-database versus permissioned-blockchain traceability", 13, GREY); pfmt(p, 8, 30, 1.15, False, WD_ALIGN_PARAGRAPH.LEFT)
    p = doc.add_paragraph(); runs(p, "Case firms:  **Unilever PLC**  ·  **Nestlé S.A.**  ·  **Wilmar International Ltd**", 11); pfmt(p, 0, 4, 1.1, False, WD_ALIGN_PARAGRAPH.LEFT)
    p = doc.add_paragraph(); runs(p, "Bloomberg data captured 15 October 2026 at the Woxsen Bloomberg Lab / Terminal", 10, GREY); pfmt(p, 0, 60, 1.1, False, WD_ALIGN_PARAGRAPH.LEFT)
    t = doc.add_table(rows=5, cols=2); t.autofit = False; t.alignment = WD_TABLE_ALIGNMENT.LEFT
    from lib import _tbl_props; _tbl_props(t, [4.2, 12.2])
    rows = [("Submitted by", "[Team member names and student IDs — to be completed]"), ("Programme / course", "MBA BA — Blockchain Supply Chain & Predictive Analytics"), ("Faculty supervisor", "[Name — to be completed]"), ("Submission date", "[DD Month 2026 — to be completed]"), ("Companion files", "Palm_Oil_Traceability_Capstone_Workbook.xlsx (16 sheets)  ·  CP45_Palm_Oil_Traceability_Notebook.ipynb  ·  palm_oil_traceability_model.py")]
    for i, (a, b) in enumerate(rows):
        c0, c1 = t.rows[i].cells; c0.width = Cm(4.2); c1.width = Cm(12.2)
        for c in (c0, c1): cell_margins(c, 60, 60, 60, 60); cell_borders(c, bottom=(4, "D5DAE1"), top=None, left=None, right=None)
        runs(c0.paragraphs[0], a, 9.5, GREY, bold=True); pfmt(c0.paragraphs[0], 0, 0, 1.05, False, WD_ALIGN_PARAGRAPH.LEFT)
        r = c1.paragraphs[0]; runs(r, b, 9.5, INKC); pfmt(r, 0, 0, 1.05, False, WD_ALIGN_PARAGRAPH.LEFT)
        if "[" in b:
            for run in r.runs: run.font.highlight_color = 7  # yellow
    p = doc.add_paragraph(); pfmt(p, 0, 40, 1.0)
    p = doc.add_paragraph(); runs(p, "Data and licence note. Bloomberg figures were transcribed from Terminal screens (SPLC, FA, ESG, CN, HP/GP, DES) on 15 October 2026 and are used here for academic purposes under the Woxsen Bloomberg licence. Figures marked ASSUMPTION in Chapters 5–6 are modelling inputs that Bloomberg cannot supply; they are not Bloomberg data.", 8.5, GREY, italic=True); pfmt(p, 0, 0, 1.1, False, WD_ALIGN_PARAGRAPH.JUSTIFY)

def toc_page(doc, entries, lof_entries):
    p = doc.add_paragraph(); p.paragraph_format.page_break_before = True
    r = p.add_run("Contents"); set_font(r, 21, True, False, NAVY); para_border_bottom(p, "142B4D", 12, 6); pfmt(p, 0, 10, 1.0, True)
    # TOC field with cached entries
    for i, (lvl, text, pg) in enumerate(entries):
        q = doc.add_paragraph(); q.paragraph_format.tab_stops.add_tab_stop(Cm(TEXT_W), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        ind = 0 if lvl == 1 else 0.6
        pfmt(q, 5 if lvl == 1 else 0, 1.5, 1.0, False, WD_ALIGN_PARAGRAPH.LEFT, ind)
        if i == 0:
            for t_ in ("begin",):
                rr = q.add_run(); e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "begin"); rr._element.append(e)
            rr = q.add_run(); it = OxmlElement("w:instrText"); it.set(qn("xml:space"), "preserve"); it.text = ' TOC \\o "1-2" \\h \\z \\u '; rr._element.append(it)
            rr = q.add_run(); e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "separate"); rr._element.append(e)
        r1 = q.add_run(text + "\t" + str(pg)); set_font(r1, 10.5 if lvl == 1 else 9.5, lvl == 1, False, NAVY if lvl == 1 else INKC)
        if i == len(entries) - 1:
            rr = q.add_run(); e = OxmlElement("w:fldChar"); e.set(qn("w:fldCharType"), "end"); rr._element.append(e)
    # lists of figures and tables
    p = doc.add_paragraph(); runs(p, "**List of figures and tables**", 12, NAVY); pfmt(p, 16, 4, 1.0, True, WD_ALIGN_PARAGRAPH.LEFT)
    for label, text, pg in lof_entries:
        q = doc.add_paragraph(); q.paragraph_format.tab_stops.add_tab_stop(Cm(TEXT_W), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        pfmt(q, 0, 0.5, 1.0, False, WD_ALIGN_PARAGRAPH.LEFT, 0)
        r1 = q.add_run(f"{label}  {text}\t{pg}"); set_font(r1, 8.5, False, False, INKC)

def exec_summary(doc):
    h1(doc, "Executive Summary")
    S = lambda k, s, o: det[f"{k}_{s}"][o]["benefit"]
    para(doc, "**The problem.** From 30 December 2026 the EU Deforestation Regulation (EUDR, Regulation (EU) 2023/1115) obliges operators that place palm oil and derived products on the EU market to show that each product is deforestation-free, legally produced and traceable to the plot of land where it was grown, and obliges traders and downstream operators to keep the evidence chain. The maximum fine must be at least 4% of the operator’s annual EU turnover. The dominant sourcing practice, RSPO *mass balance*, lets certified and uncertified oil mix physically, so it cannot supply plot-level evidence. Unilever, Nestlé and Wilmar sit at different points of this chain and face the same regulatory clock.", 10, 5)
    para(doc, "**What we did.** We captured Bloomberg screens (SPLC, FA, ESG, CN, HP/GP) for the three firms on 15 October 2026 and built (i) a sourced evidence workbook, (ii) a ten-indicator **Sustainable Palm Oil Exposure Index (SPOEI)**, and (iii) a cost-benefit model that compares *status quo*, a *central traceability database* and a *permissioned blockchain* under base, adverse and severe enforcement scenarios, with a 20,000-draw Monte Carlo (common random numbers) and sensitivity tests. A supervised classifier is fully specified but **not estimated**: the screens give 21 firm-years, whereas about 85 labelled observations (≈17 events) are needed to show an AUC of 0.70 against chance (Chapter 4).", 10, 5)
    para(doc, "**What we found.**", 10, 2, keep_next=True)
    bullets(doc, [
        f"**Wilmar is the highest-risk node** (SPOEI {N['score']['base'][2]:.1f} vs Unilever {N['score']['base'][0]:.1f} and Nestlé {N['score']['base'][1]:.1f}; the ranking holds under four weightings). The drivers are thin interest cover (2.1×), supplier conduct flags (37% of listed suppliers) and a 2026 news record of legal and governance events, not deforestation events.",
        "**Bloomberg cannot see the palm chain.** None of the top-24 suppliers of Unilever or Nestlé is a palm trader or plantation, and Wilmar appears in neither list; visible plantation nodes are only 0.4% of Wilmar’s cost base. This opacity is the traceability problem itself, and the evidence for it.",
        f"**Traceability pays; the blockchain premium is conditional.** Relative to the status quo, a permissioned blockchain has an NPV benefit of USD {S('ULVR','Base','BC'):.0f} / {S('ULVR','Adverse','BC'):.0f} / {S('ULVR','Severe','BC'):.0f} m (Unilever), {S('NESN','Base','BC'):.0f} / {S('NESN','Adverse','BC'):.0f} / {S('NESN','Severe','BC'):.0f} m (Nestlé) and {S('WIL','Base','BC'):.0f} / {S('WIL','Adverse','BC'):.0f} / {S('WIL','Severe','BC'):.0f} m (Wilmar) in the base / adverse / severe case. A plain central database does as well or better in the base case for Unilever and Wilmar, and the blockchain wins only if enforcement tightens or its assurance value is high (parity at 0.82–0.96 versus 0.80 for the database). In mixed-regime simulations the blockchain beats the database in 35–42% of worlds.",
    ], 10, False, 2)
    para(doc, "**Recommendation.** Adopt a *database-first, ledger-ready* programme: build the central traceability stack (plot geolocation, satellite checks, audits) now, with hash-anchored records that can migrate to a permissioned consortium ledger, and escalate to the ledger when pre-agreed triggers fire: regulatory-event probability at about 1.8–2.1 times the base rate for Unilever and Wilmar (the adverse case; Nestlé is already past parity at base inputs), consortium co-funding that cuts the ledger’s programme cost by 3–11%, or audited evidence that the ledger’s assurance value clears the parity point. Unilever and Nestlé should use Wilmar’s measurable leverage over its plantation suppliers (Wilmar supplies 27% of the revenue of the visible palm nodes, weighted by cost) through traceability covenants rather than exit on a Bloomberg ESG score, which tracks disclosure, not footprint.", 10, 5)
    callout(doc, "Read this before relying on the numbers", "All risk probabilities, fine rates, programme costs and effectiveness values are labelled ASSUMPTION and are placeholders for calibration; the results show *decision logic and ranges*, not forecasts. The predictive-model results (RQ3) are not reported because the data to estimate them are not yet available; Chapter 4 states exactly what is needed.", "warn")
