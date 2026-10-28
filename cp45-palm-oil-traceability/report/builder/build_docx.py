import sys, os, re, subprocess, json, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
import lib, ch_front, ch1, ch2, ch3, ch4, ch5, ch6, ch7, appx

OUT = str(ROOT / "report" / "output") + "/"
os.makedirs(OUT, exist_ok=True)
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pages_cache.json")
HEADER = "CP-45  ·  Blockchain Sustainable Palm Oil Traceability  ·  Woxsen University MBA-BA Capstone"


PPR = "pStyle keepNext keepLines pageBreakBefore framePr widowControl numPr suppressLineNumbers pBdr shd tabs suppressAutoHyphens kinsoku wordWrap overflowPunct topLinePunct autoSpaceDE autoSpaceDN bidi adjustRightInd snapToGrid spacing ind contextualSpacing mirrorIndents suppressOverlap jc textDirection textAlignment textboxTightWrap outlineLvl divId cnfStyle rPr sectPr pPrChange".split()
TBLPR = "tblStyle tblpPr tblOverlap bidiVisual tblStyleRowBandSize tblStyleColBandSize tblW jc tblCellSpacing tblInd tblBorders shd tblLayout tblCellMar tblLook tblCaption tblDescription".split()
TCPR = "cnfStyle tcW gridSpan hMerge vMerge tcBorders shd noWrap tcMar textDirection tcFitText vAlign hideMark".split()
RPR = "rStyle rFonts b bCs i iCs caps smallCaps strike dstrike outline shadow emboss imprint noProof snapToGrid vanish webHidden color spacing w kern position sz szCs highlight u effect bdr shd fitText vertAlign rtl cs em lang eastAsianLayout specVanish oMath".split()
def _reorder(root):
    for tag, order in (("pPr", PPR), ("tblPr", TBLPR), ("tcPr", TCPR), ("rPr", RPR)):
        idx = {qn("w:" + n): i for i, n in enumerate(order)}
        for el in root.iter(qn("w:" + tag)):
            kids = list(el)
            srt = sorted(kids, key=lambda k: idx.get(k.tag, 999))
            if srt != kids:
                for k in kids: el.remove(k)
                for k in srt: el.append(k)

def fix_schema(doc):
    _reorder(doc.element)
    for sec in doc.sections:
        for part in (sec.header, sec.footer, sec.first_page_header, sec.first_page_footer):
            try: _reorder(part._element)
            except Exception: pass
    st = doc.settings.element
    for z in st.iter(qn("w:zoom")):
        if z.get(qn("w:percent")) is None: z.set(qn("w:percent"), "100")

def build_doc(entries, lof_entries):
    lib.CTX.fig = {}; lib.CTX.tab = {}; lib.CTX.lof = []; lib.CTX.headings = []
    doc = Document(); setup(doc); header_footer(doc, HEADER)
    cp = doc.core_properties; cp.title = "Blockchain Sustainable Palm Oil Traceability (CP-45)"; cp.subject = "Woxsen MBA-BA capstone: Bloomberg-based EUDR / Scope 3 analysis"; cp.author = "Capstone team"; cp.keywords = "EUDR, palm oil, blockchain, Bloomberg, Monte Carlo"
    ch_front.cover(doc); ch_front.toc_page(doc, entries, lof_entries); ch_front.exec_summary(doc)
    for m in (ch1, ch2, ch3, ch4, ch5, ch6, ch7): m.build(doc)
    appx.build(doc); appx.references(doc)
    fix_schema(doc)
    return doc

def to_pdf(docx):
    subprocess.run([shutil.which("soffice") or "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", os.path.dirname(docx), docx], check=True, capture_output=True, timeout=300)
    return docx[:-5] + ".pdf"

def page_texts(pdf):
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    out = []
    for i in range(1, n + 1):
        t = subprocess.run(["pdftotext", "-f", str(i), "-l", str(i), "-layout", pdf, "-"], capture_output=True, text=True).stdout
        out.append(re.sub(r"\s+", " ", t))
    return out

def locate(pages, entries, lof):
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    first = next(i for i, t in enumerate(pages) if "The problem." in t)  # exec summary page (0-based)
    cur = first; ep = []
    for lvl, text, _ in entries:
        key = norm(text); found = None
        for i in range(cur, len(pages)):
            if key in pages[i]: found = i; break
        if found is None: found = cur; print("  [warn] heading not found:", text)
        cur = found; ep.append((lvl, text, found + 1))
    lp = []; cur = first
    for label, text, _ in lof:
        key = norm(f"{label} — {text}"); found = None
        for i in range(first, len(pages)):
            if key[:60] in pages[i]: found = i; break
        if found is None: print("  [warn] caption not found:", label, text); found = cur
        lp.append((label, text, found + 1))
    return ep, lp

NAME = "CP45_Executive_Capstone_Report.docx"

def main(argv=None):
    import argparse
    ap = argparse.ArgumentParser(description="Build the CP-45 capstone report (DOCX, and PDF when LibreOffice + poppler are installed).")
    ap.add_argument("--no-pdf", action="store_true", help="build the DOCX only and reuse cached page numbers for the table of contents")
    a = ap.parse_args(argv)

    build_doc([(1, "x", "0")], [("x", "x", "0")])                       # pass 0: collect headings and captions
    entries = [(l, t, "0") for l, t in lib.CTX.headings]; lof = [(x, y, "0") for x, y in lib.CTX.lof]
    print("headings", len(entries), "captions", len(lof))
    path = OUT + NAME
    tools = all(shutil.which(t) for t in ("soffice", "pdfinfo", "pdftotext"))
    if a.no_pdf or not tools:
        if not a.no_pdf: print("[warn] soffice/poppler not found: building the DOCX only.")
        if os.path.exists(CACHE):
            c = json.load(open(CACHE))
            if [e[1] for e in c["entries"]] == [e[1] for e in entries]:
                entries = [tuple(e) for e in c["entries"]]; lof = [tuple(e) for e in c["lof"]]
        build_doc(entries, lof).save(path)
        print("done (TOC page numbers from cache; in Word: right-click the TOC > Update field)", path)
        return path
    prev = None
    for it in range(3):                                                  # two-pass TOC: build, paginate, rebuild with real page numbers
        build_doc(entries, lof).save(path)
        pdf = to_pdf(path); pages = page_texts(pdf)
        ep, lp = locate(pages, entries, lof)
        print(f"iteration {it}: {len(pages)} pages")
        if prev == (ep, lp): break
        prev = (ep, lp); entries = ep; lof = lp
    json.dump({"entries": ep, "lof": lp, "pages": len(pages)}, open(CACHE, "w"), indent=1)
    print("done", path, "and", path[:-5] + ".pdf")
    return path

if __name__ == "__main__":
    main()
