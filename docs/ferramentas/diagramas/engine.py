"""Motor mínimo de diagramas: modelo -> .drawio (XML não comprimido) + prévia PNG (PIL) + verificações.

Coordenadas sempre absolutas (grade de 10 px); filhos de containers são convertidos para
coordenadas relativas ao gravar o .drawio.
"""
import html
import math
import re
from xml.sax.saxutils import quoteattr

from PIL import Image, ImageDraw, ImageFont

FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"   # métrica = Helvetica/Arial
FONTB = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONTI = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
_fc = {}


def font(size, bold=False, italic=False):
    k = (round(size), bold, italic)
    if k not in _fc:
        _fc[k] = ImageFont.truetype(FONTB if bold else FONTI if italic else FONT, k[0])
    return _fc[k]


# (preenchimento, borda, cor do texto) — sempre com o mesmo significado nos 3 diagramas
PAL = {
    "uni": ("#DAE8FC", "#6C8EBF", "#000000"),
    "ind": ("#FFE6CC", "#D79B00", "#000000"),
    "pro": ("#D5E8D4", "#82B366", "#000000"),
    "sis": ("#1F4E79", "#1F4E79", "#FFFFFF"),
    "ator": ("#F5F5F5", "#666666", "#000000"),
    "ponte": ("#E1D5E7", "#9673A6", "#000000"),
    "fora": ("none", "#999999", "#555555"),
    "nota": ("#FFF9DB", "#C9B458", "#333333"),
    "branco": ("#FFFFFF", "#666666", "#000000"),
    "preto": ("#000000", "#000000", "#FFFFFF"),
    "uniC": ("#F4F8FE", "#6C8EBF", "#2B4A7A"),
    "indC": ("#FFF8F0", "#D79B00", "#8A5A00"),
    "proC": ("#F3FAF2", "#82B366", "#3D6B2A"),
}

FS_BOX, FS_EDGE, FS_END = 16, 15, 15     # tamanhos padrão (px)


class Node:
    def __init__(s, id, label, x, y, w, h, kind="box", pal="branco", fs=FS_BOX, bold=False,
                 parent=None, dashed=False, sw=1, align="center", valign="middle",
                 fit=True, rounded=True, extra="", term=None):
        s.__dict__.update({k: v for k, v in locals().items() if k != "s"})


class Edge:
    def __init__(s, id, src, dst, pts, label="", t=0.5, off=(0, 0), ends=None, style="solid",
                 arrow=True, fs=FS_EDGE, extra=""):
        # pts: pontos absolutos [(x, y), ...] incluindo a porta de saída e a de entrada
        s.__dict__.update({k: v for k, v in locals().items() if k != "s"})


def runs(label):
    """Texto HTML simples -> linhas de (texto, negrito, itálico)."""
    lines, cur, b, i = [], [], False, False
    for tok in re.split(r"(<[^>]+>)", label.replace("<br>", "\n")):
        if tok.startswith("<"):
            t = tok.lower()
            b = True if t == "<b>" else False if t == "</b>" else b
            i = True if t == "<i>" else False if t == "</i>" else i
            continue
        parts = html.unescape(tok).split("\n")
        for j, p in enumerate(parts):
            if j:
                lines.append(cur)
                cur = []
            if p:
                cur.append((p, b, i))
    lines.append(cur)
    return lines


def line_width(line, fs, bold0=False):
    return sum(font(fs, b or bold0, i).getlength(t) for t, b, i in line)


class Diagram:
    def __init__(s, name, W, H):
        s.name, s.W, s.H = name, W, H
        s.nodes, s.edges, s.errors = [], [], []

    def n(s, *a, **k):
        nd = Node(*a, **k)
        s.nodes.append(nd)
        return nd

    def e(s, *a, **k):
        ed = Edge(*a, **k)
        s.edges.append(ed)
        return ed

    def get(s, id):
        return next(n for n in s.nodes if n.id == id)

    # ---------- geometria ----------
    @staticmethod
    def polyline_point(pts, t):
        L = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
        d = sum(L) * t
        for i, l in enumerate(L):
            if d <= l or i == len(L) - 1:
                f = 0 if l == 0 else min(d / l, 1)
                return (pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f,
                        pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f)
            d -= l

    def text_size(s, text, fs, bold=False):
        lines = runs(text)
        return max(line_width(l, fs, bold) for l in lines), len(lines) * fs * 1.25

    def label_box(s, ed):
        if not ed.label:
            return None
        cx, cy = s.polyline_point(ed.pts, ed.t)
        cx += ed.off[0]
        cy += ed.off[1]
        w, h = s.text_size(ed.label, ed.fs)
        return (cx - w / 2 - 2, cy - h / 2 - 1, cx + w / 2 + 2, cy + h / 2 + 1)

    END_DIST = 16

    def end_label_boxes(s, ed):
        out = []
        tot = sum(math.dist(a, b) for a, b in zip(ed.pts, ed.pts[1:]))
        for txt, from_end, (dx, dy) in ed.ends or []:
            f = s.END_DIST / tot
            px, py = s.polyline_point(ed.pts, 1 - f if from_end else f)
            w, h = s.text_size(txt, FS_END, True)
            cx, cy = px + dx, py + dy
            out.append((txt, from_end, (dx, dy), (cx - w / 2 - 1, cy - h / 2, cx + w / 2 + 1, cy + h / 2)))
        return out

    # ---------- verificações ----------
    @staticmethod
    def seg_hits_box(p, q, b, pad=1):
        x0, y0, x1, y1 = b[0] + pad, b[1] + pad, b[2] - pad, b[3] - pad
        if p[0] == q[0]:
            ya, yb = sorted((p[1], q[1]))
            return x0 < p[0] < x1 and ya < y1 and yb > y0
        if p[1] == q[1]:
            xa, xb = sorted((p[0], q[0]))
            return y0 < p[1] < y1 and xa < x1 and xb > x0
        return False

    def check(s, glossary=None, rfs=(), rns=()):
        E = s.errors
        leaves = [n for n in s.nodes if n.kind in ("box", "text", "ellipse")]
        bb = lambda n: (n.x, n.y, n.x + n.w, n.y + n.h)
        inter = lambda a, b: a[0] < b[2] and b[0] < a[2] and a[1] < b[3] and b[1] < a[3]
        for i, a in enumerate(leaves):                                   # 1 sobreposição
            for b in leaves[i + 1:]:
                if inter(bb(a), bb(b)):
                    E.append(f"sobreposição: {a.id} x {b.id}")
        for n in s.nodes:                                                # dentro do container / página
            if n.parent:
                p = s.get(n.parent)
                if not (n.x >= p.x and n.y >= p.y and n.x + n.w <= p.x + p.w and n.y + n.h <= p.y + p.h):
                    E.append(f"fora do container: {n.id} em {p.id}")
            if n.x < 0 or n.y < 0 or n.x + n.w > s.W or n.y + n.h > s.H:
                E.append(f"fora da página: {n.id}")
        lbls = []                                                        # 2 rótulos
        for ed in s.edges:
            lb = s.label_box(ed)
            if lb:
                lbls.append((ed.id, lb))
            for txt, fe, d, b in s.end_label_boxes(ed):
                lbls.append((f"{ed.id}:{txt}", b))
            for (x0, y0, x1, y1) in [b for _, b in lbls[-3:]]:
                if x0 < 0 or y0 < 0 or x1 > s.W or y1 > s.H:
                    E.append(f"rótulo fora da página: {ed.id}")
        for i, (ida, a) in enumerate(lbls):
            for n in leaves:
                if inter(a, bb(n)):
                    E.append(f"rótulo sobre caixa: {ida} x {n.id}")
            for idb, b in lbls[i + 1:]:
                if inter(a, b):
                    E.append(f"rótulos sobrepostos: {ida} x {idb}")
            owner = ida.split(":")[0]
            for ed in s.edges:
                if ed.id != owner and any(s.seg_hits_box(p, q, a) for p, q in zip(ed.pts, ed.pts[1:])):
                    E.append(f"seta {ed.id} cruza rótulo {ida}")
        for ed in s.edges:                                               # 3 setas
            for p, q in zip(ed.pts, ed.pts[1:]):
                if p[0] != q[0] and p[1] != q[1]:
                    E.append(f"segmento não ortogonal: {ed.id} {p}->{q}")
                for n in leaves:
                    if n.id not in (ed.src, ed.dst) and s.seg_hits_box(p, q, bb(n)):
                        E.append(f"seta {ed.id} atravessa {n.id}")
            for nid, pt in ((ed.src, ed.pts[0]), (ed.dst, ed.pts[-1])):
                x0, y0, x1, y1 = bb(s.get(nid))
                onb = ((abs(pt[0] - x0) < .5 or abs(pt[0] - x1) < .5) and y0 <= pt[1] <= y1) or \
                      ((abs(pt[1] - y0) < .5 or abs(pt[1] - y1) < .5) and x0 <= pt[0] <= x1)
                if not onb:
                    E.append(f"porta fora da borda: {ed.id} em {nid} {pt}")
        for n in s.nodes:                                                # 4 texto cabe
            if not n.fit or not n.label:
                continue
            lines = runs(n.label)
            for l in lines:
                w = line_width(l, n.fs, n.bold)
                if w > n.w - 10:
                    E.append(f"texto não cabe ({w:.0f}>{n.w - 10}): {n.id} '{''.join(t for t, _, _ in l)}'")
            if n.kind != "container" and len(lines) * n.fs * 1.25 > n.h - 4:
                E.append(f"texto alto demais: {n.id}")
        if glossary is not None:                                         # 5 glossário
            for n in s.nodes:
                if n.term and n.term not in glossary:
                    E.append(f"termo fora do glossário: '{n.term}'")
        alltxt = " ".join([n.label for n in s.nodes] + [e.label for e in s.edges])
        for kind, ok in (("RF", rfs), ("RN", rns)):                      # 6 RF/RN existentes
            for m in re.finditer(kind + r"(\d\d)(?:–" + kind + r"?(\d\d))?", alltxt):
                for k in range(int(m.group(1)), int(m.group(2) or m.group(1)) + 1):
                    if f"{kind}{k:02d}" not in ok:
                        E.append(f"{kind}{k:02d} inexistente")
        return E

    # ---------- XML draw.io ----------
    def style_of(s, n):
        fill, stroke, fc = PAL[n.pal]
        base = (f"html=1;whiteSpace=wrap;fontFamily=Helvetica;fontSize={n.fs};fontColor={fc};"
                f"align={n.align};verticalAlign={n.valign};")
        if n.bold:
            base += "fontStyle=1;"
        if n.kind == "text":
            return base + "text;strokeColor=none;fillColor=none;" + n.extra
        if n.kind == "ellipse":
            return base + f"ellipse;fillColor={fill};strokeColor={stroke};strokeWidth={n.sw};" + n.extra
        if n.kind == "lane":
            return (f"swimlane;horizontal=0;startSize=34;html=1;fontFamily=Helvetica;fontSize={n.fs};fontStyle=1;"
                    f"fillColor={fill};strokeColor={stroke};swimlaneFillColor=#FFFFFF;" + n.extra)
        st = base + f"fillColor={fill};strokeColor={stroke};strokeWidth={n.sw};"
        st += "rounded=1;arcSize=12;" if n.rounded else "rounded=0;"
        if n.dashed:
            st += "dashed=1;"
        if n.kind == "container":
            st += "container=1;collapsible=0;recursiveResize=0;"
        return st + n.extra

    def to_xml(s):
        out = ['<mxfile host="app.diagrams.net" type="device">',
               f'  <diagram id="{s.name}" name="{s.name}">',
               f'    <mxGraphModel dx="{s.W}" dy="{s.H}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
               f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{s.W}" pageHeight="{s.H}" math="0" shadow="0">',
               '      <root>', '        <mxCell id="0" />', '        <mxCell id="1" parent="0" />']
        for n in s.nodes:
            px, py, pid = 0, 0, "1"
            if n.parent:
                p = s.get(n.parent)
                px, py, pid = p.x, p.y, p.id
            out.append(f'        <mxCell id="{n.id}" value={quoteattr(n.label)} style={quoteattr(s.style_of(n))} '
                       f'vertex="1" parent="{pid}">')
            out.append(f'          <mxGeometry x="{n.x - px}" y="{n.y - py}" width="{n.w}" height="{n.h}" as="geometry" />')
            out.append('        </mxCell>')
        for ed in s.edges:
            src, dst = s.get(ed.src), s.get(ed.dst)
            (sx, sy), (tx, ty) = ed.pts[0], ed.pts[-1]
            st = ("edgeStyle=orthogonalEdgeStyle;rounded=1;orthogonalLoop=1;html=1;fontFamily=Helvetica;"
                  f"fontSize={ed.fs};labelBackgroundColor=#FFFFFF;strokeColor=#333333;strokeWidth=1.5;"
                  f"exitX={(sx - src.x) / src.w:.4f};exitY={(sy - src.y) / src.h:.4f};exitDx=0;exitDy=0;exitPerimeter=0;"
                  f"entryX={(tx - dst.x) / dst.w:.4f};entryY={(ty - dst.y) / dst.h:.4f};entryDx=0;entryDy=0;entryPerimeter=0;")
            st += "endArrow=block;endFill=1;" if ed.arrow else "endArrow=none;"
            if ed.style == "dashed":
                st += "dashed=1;dashPattern=8 4;"
            if ed.style == "dotted":
                st += "dashed=1;dashPattern=2 3;"
            st += ed.extra
            out.append(f'        <mxCell id="{ed.id}" value={quoteattr(ed.label)} style={quoteattr(st)} edge="1" '
                       f'parent="1" source="{ed.src}" target="{ed.dst}">')
            out.append(f'          <mxGeometry x="{2 * ed.t - 1:.3f}" relative="1" as="geometry">')
            out.append(f'            <mxPoint as="offset" x="{ed.off[0]}" y="{ed.off[1]}" />')
            if len(ed.pts) > 2:
                out.append('            <Array as="points">')
                out += [f'              <mxPoint x="{x}" y="{y}" />' for x, y in ed.pts[1:-1]]
                out.append('            </Array>')
            out += ['          </mxGeometry>', '        </mxCell>']
            tot = sum(math.dist(a, b) for a, b in zip(ed.pts, ed.pts[1:]))
            for i, (txt, fe, (dx, dy), _) in enumerate(s.end_label_boxes(ed)):
                f = s.END_DIST / tot
                x = (1 - 2 * f) if fe else (-1 + 2 * f)
                out.append(f'        <mxCell id="{ed.id}_c{i}" value={quoteattr(txt)} style="edgeLabel;html=1;'
                           f'align=center;verticalAlign=middle;resizable=0;points=[];fontFamily=Helvetica;'
                           f'fontSize={FS_END};fontStyle=1;fontColor=#B00000;labelBackgroundColor=none;" vertex="1" '
                           f'connectable="0" parent="{ed.id}">')
                out.append(f'          <mxGeometry x="{x:.3f}" relative="1" as="geometry"><mxPoint as="offset" '
                           f'x="{dx}" y="{dy}" /></mxGeometry>')
                out.append('        </mxCell>')
        out += ['      </root>', '    </mxGraphModel>', '  </diagram>', '</mxfile>', '']
        return "\n".join(out)
