"""Renderiza em PNG (PIL) os .drawio do projeto — o subconjunto do draw.io usado por docs/ferramentas/diagramas:
caixas, elipses, textos, raias, containers, arestas ortogonais com pontos, rótulos e cardinalidades.
Uso: python3 -I render_drawio.py <entrada.drawio> <saida.png> [escala=2]"""
import html, math, re, sys
import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw, ImageFont

SRC, DST = sys.argv[1], sys.argv[2]
K = float(sys.argv[3]) if len(sys.argv) > 3 else 2.0
FR = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
FB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FI = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
FD = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
_c = {}
def font(sz, b=False, i=False):
    k = (round(sz * K), b, i)
    if k not in _c:
        _c[k] = ImageFont.truetype(FB if b else FI if i else FR, k[0])
    return _c[k]

def sty(s):
    d = {}
    for p in (s or "").split(";"):
        if "=" in p:
            a, b = p.split("=", 1); d[a] = b
        elif p:
            d[p] = "1"
    return d

root = ET.parse(SRC).getroot()
model = root.find(".//mxGraphModel")
W, H = int(model.get("pageWidth")), int(model.get("pageHeight"))
cells = {c.get("id"): c for c in root.iter("mxCell")}

def abspos(cid):
    c = cells[cid]; g = c.find("mxGeometry")
    x, y = float(g.get("x", 0)), float(g.get("y", 0))
    p = c.get("parent")
    if p in cells and cells[p].get("vertex") == "1":
        px, py = abspos(p); x += px; y += py
    return x, y

im = Image.new("RGB", (int(W * K), int(H * K)), "white")
d = ImageDraw.Draw(im)
S = lambda v: v * K

def runs(label):
    """-> lista de linhas; cada linha = lista de (texto, bold, italic)."""
    lines, cur, b, i = [], [], False, False
    for tok in re.split(r"(<[^>]+>)", label.replace("<br>", "\n")):
        if tok.startswith("<"):
            t = tok.lower()
            if t == "<b>": b = True
            elif t == "</b>": b = False
            elif t == "<i>": i = True
            elif t == "</i>": i = False
            continue
        parts = html.unescape(tok).split("\n")
        for j, p in enumerate(parts):
            if j: lines.append(cur); cur = []
            if p: cur.append((p, b, i))
    lines.append(cur)
    return lines

def wrap(lines, fs, bold0, maxw):
    out = []
    for ln in lines:
        words = []
        for t, b, i in ln:
            for w in re.split(r"(\s+)", t):
                if w: words.append((w, b or bold0, i))
        cur, cw = [], 0
        for w, b, i in words:
            ww = font(fs, b, i).getlength(w) / K
            if cur and cw + ww > maxw and not w.isspace():
                out.append(cur); cur, cw = [], 0
            if w.isspace() and not cur: continue
            cur.append((w, b, i)); cw += ww
        out.append(cur)
    return out

def draw_text(label, x, y, w, h, st, color=None):
    fs = float(st.get("fontSize", 12)); bold0 = st.get("fontStyle") in ("1",)
    ital0 = st.get("fontStyle") == "2"
    col = color or st.get("fontColor", "#000000")
    sl = float(st.get("spacingLeft", 0))
    lines = wrap(runs(label), fs, bold0, w - 8 - sl)
    lh = fs * 1.25
    tot = lh * len(lines)
    va = st.get("verticalAlign", "middle")
    yy = y + 4 + float(st.get("spacingTop", 0)) if va == "top" else y + (h - tot) / 2
    for li, ln in enumerate(lines):
        lw = sum(font(fs, b, i or ital0).getlength(t) / K for t, b, i in ln)
        xx = x + 4 + sl if st.get("align") == "left" else x + (w - lw) / 2
        for t, b, i in ln:
            f = font(fs, b, i or ital0)
            if any(ord(ch) > 0x2000 and ch not in "—–→≥×·" for ch in t):
                f = ImageFont.truetype(FD, round(fs * K))
            d.text((S(xx), S(yy + li * lh)), t, fill=col, font=f)
            xx += f.getlength(t) / K

def dashed(p, q, on, off, col="#333333", w=2):
    L = math.dist(p, q)
    if L == 0: return
    ux, uy = (q[0] - p[0]) / L, (q[1] - p[1]) / L; t = 0
    while t < L:
        e = min(t + on * K, L)
        d.line([(p[0] + ux * t, p[1] + uy * t), (p[0] + ux * e, p[1] + uy * e)], fill=col, width=w); t = e + off * K

def rect(box, st, rounded):
    fill = st.get("fillColor", "#FFFFFF"); fill = None if fill == "none" else fill
    stroke = st.get("strokeColor", "#000000"); sw = max(1, round(float(st.get("strokeWidth", 1)) * K))
    if st.get("dashed") == "1":
        if fill: d.rectangle(box, fill=fill)
        x0, y0, x1, y1 = box
        for p, q in (((x0, y0), (x1, y0)), ((x1, y0), (x1, y1)), ((x1, y1), (x0, y1)), ((x0, y1), (x0, y0))):
            dashed(p, q, 6, 4, stroke, sw)
    else:
        d.rounded_rectangle(box, radius=S(8) if rounded else 0, fill=fill, outline=stroke, width=sw)

vertices = [c for c in root.iter("mxCell") if c.get("vertex") == "1" and not (c.get("style") or "").startswith("edgeLabel")]
depth = lambda c: 0 if cells[c.get("parent")].get("vertex") != "1" else 1 + depth(cells[c.get("parent")])
vertices.sort(key=depth)
geo = {}
for c in vertices:
    st = sty(c.get("style")); g = c.find("mxGeometry")
    x, y = abspos(c.get("id")); w, h = float(g.get("width")), float(g.get("height"))
    geo[c.get("id")] = (x, y, w, h)
    box = [S(x), S(y), S(x + w), S(y + h)]
    lab = c.get("value") or ""
    if "swimlane" in st:
        stroke = st.get("strokeColor", "#666666")
        d.rectangle(box, fill="white", outline=stroke, width=max(1, int(K)))
        ss = float(st.get("startSize", 30))
        d.rectangle([box[0], box[1], box[0] + S(ss), box[3]], fill=st.get("fillColor"), outline=stroke, width=max(1, int(K)))
        t = html.unescape(lab); f = font(float(st.get("fontSize", 13)), True)
        tmp = Image.new("RGBA", (int(S(h)), int(S(ss))), (0, 0, 0, 0)); td = ImageDraw.Draw(tmp)
        bb = f.getbbox(t); td.text(((S(h) - f.getlength(t)) / 2, (S(ss) - (bb[3] - bb[1])) / 2 - bb[1]), t, fill="black", font=f)
        r = tmp.rotate(90, expand=True); im.paste(r, (int(box[0]), int(box[1])), r)
        continue
    if "text" in st and lab.startswith("<table"):
        rows = re.findall(r"<tr>(.*?)</tr>", lab)
        rh = h / len(rows); yy = y
        for ri, r in enumerate(rows):
            tds = re.findall(r'<td style="([^"]*)">(.*?)</td>', r); xx = x
            for cs, ct in tds:
                cw = float(re.search(r"width:(\d+)px", cs).group(1)) + 10
                d.rectangle([S(xx), S(yy), S(xx + cw), S(yy + rh)], fill="#EEEEEE" if ri == 0 else "white",
                            outline="#999999", width=max(1, int(K)))
                draw_text(ct, xx, yy, cw, rh, {"fontSize": "11", "align": "left", "verticalAlign": "top",
                                                 "fontStyle": "1" if ri == 0 else "0"})
                xx += cw
            yy += rh
        continue
    if "ellipse" in st:
        sw = max(1, round(float(st.get("strokeWidth", 1)) * K))
        if st.get("shape") == "doubleEllipse":
            d.ellipse(box, fill="white", outline="#000000", width=max(2, int(2 * K)))
            p = S(5); d.ellipse([box[0] + p, box[1] + p, box[2] - p, box[3] - p], fill="#000000")
        else:
            f = st.get("fillColor"); d.ellipse(box, fill=None if f == "none" else f, outline=st.get("strokeColor"), width=sw)
    elif "text" not in st and w > 2:
        rect(box, st, st.get("rounded") == "1")
    if lab:
        draw_text(lab, x, y, w, h, st)

def port(cid, fx, fy):
    x, y, w, h = geo[cid]; return (x + w * fx, y + h * fy)

def poly_at(pts, dist_or_t, frac=True):
    L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]; tot = sum(L)
    dd = tot * dist_or_t if frac else dist_or_t
    for i, l in enumerate(L):
        if dd <= l or i == len(L) - 1:
            f = 0 if l == 0 else min(dd / l, 1)
            return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
        dd -= l

edges = [c for c in root.iter("mxCell") if c.get("edge") == "1"]
labels = []
for e in edges:
    st = sty(e.get("style")); g = e.find("mxGeometry")
    p0 = port(e.get("source"), float(st["exitX"]), float(st["exitY"]))
    p1 = port(e.get("target"), float(st["entryX"]), float(st["entryY"]))
    arr = g.find("Array")
    mids = [(float(p.get("x")), float(p.get("y"))) for p in arr.findall("mxPoint")] if arr is not None else []
    pts = [p0] + mids + [p1]
    P = [(S(a), S(b)) for a, b in pts]
    for p, q in zip(P, P[1:]):
        if st.get("dashed") == "1":
            on, off = (8, 4) if st.get("dashPattern", "8 4").startswith("8") else (2, 3)
            dashed(p, q, on, off, "#333333", max(2, int(1.3 * K)))
        else:
            d.line([p, q], fill="#333333", width=max(2, int(1.3 * K)))
    if st.get("endArrow") == "block":
        (x0, y0), (x1, y1) = P[-2], P[-1]; a = math.atan2(y1 - y0, x1 - x0); L = 10 * K
        d.polygon([(x1, y1), (x1 - L * math.cos(a - .38), y1 - L * math.sin(a - .38)),
                   (x1 - L * math.cos(a + .38), y1 - L * math.sin(a + .38))], fill="#333333")
    lab = e.get("value") or ""
    off = g.find("mxPoint[@as='offset']")
    ox, oy = (float(off.get("x")), float(off.get("y"))) if off is not None else (0, 0)
    tot = sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))
    if lab:
        t = (float(g.get("x", 0)) + 1) / 2
        cx, cy = poly_at(pts, t); labels.append((lab, cx + ox, cy + oy, float(st.get("fontSize", 11)), False, True, "#000000"))
    for ch in root.iter("mxCell"):
        if ch.get("parent") == e.get("id"):
            cg = ch.find("mxGeometry"); co = cg.find("mxPoint")
            t = (float(cg.get("x")) + 1) / 2
            cx, cy = poly_at(pts, t)
            cs = sty(ch.get("style"))
            labels.append((ch.get("value"), cx + float(co.get("x")), cy + float(co.get("y")),
                           float(cs.get("fontSize", 11)), cs.get("fontStyle") == "1", False, cs.get("fontColor", "#000000")))
for lab, cx, cy, fs, bold, bg, col in labels:
    ls = wrap(runs(lab), fs, bold, 10000)
    lw = max(sum(font(fs, b, i).getlength(t) / K for t, b, i in l) for l in ls); lh = fs * 1.25 * len(ls)
    if bg:
        d.rectangle([S(cx - lw / 2 - 2), S(cy - lh / 2 - 1), S(cx + lw / 2 + 2), S(cy + lh / 2 + 1)], fill="white")
    draw_text(lab, cx - lw / 2 - 6, cy - lh / 2 - 2, lw + 12, lh + 4,
              {"fontSize": str(fs), "fontStyle": "1" if bold else "0"}, color=col)
im.save(DST, dpi=(int(96 * K), int(96 * K)))
print("ok", DST, im.size)
