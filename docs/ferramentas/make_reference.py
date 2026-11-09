"""Gera o modelo de estilos ABNT (reference.docx) usado pelo pandoc.

Uso: python3 -I docs/ferramentas/make_reference.py docs/modelo/reference.docx

Parte do reference.docx padrão do pandoc e substitui: padrões do documento, estilos de parágrafo
(corpo, títulos, tabelas, legendas, capa, sumário) e a seção final (A4 paisagem — usada pelo
Apêndice B; as seções em retrato são inseridas por pos_docx.py). Só biblioteca padrão.
"""
import re
import subprocess
import sys
import zipfile

OUT = sys.argv[1]
CM = 567                       # twips por centímetro
ARIAL = '<w:rFonts w:ascii="Arial" w:hAnsi="Arial" w:eastAsia="Arial" w:cs="Arial"/>'
TEXT_W_PORTRAIT = 21 * CM - 3 * CM - 2 * CM      # largura útil em retrato (16 cm)


def style(sid, name, based="Normal", ppr="", rpr="", custom=True, next_=None, typ="paragraph", extra=""):
    return (f'<w:style w:type="{typ}"{" w:customStyle=\"1\"" if custom else ""} w:styleId="{sid}">'
            f'<w:name w:val="{name}"/>' + (f'<w:basedOn w:val="{based}"/>' if based else "") +
            (f'<w:next w:val="{next_}"/>' if next_ else "") + '<w:qFormat/>' +
            (f"<w:pPr>{ppr}</w:pPr>" if ppr else "") + (f"<w:rPr>{rpr}</w:rPr>" if rpr else "") + extra +
            "</w:style>")


def sp(before=0, after=0, line=240):
    return f'<w:spacing w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'


B, CAPS, BLACK = "<w:b/><w:bCs/>", "<w:caps/>", '<w:color w:val="000000"/>'
sz = lambda pt: f'<w:sz w:val="{pt * 2}"/><w:szCs w:val="{pt * 2}"/>'
CENTER, LEFT, BOTH = '<w:jc w:val="center"/>', '<w:jc w:val="left"/>', '<w:jc w:val="both"/>'
KEEP = "<w:keepNext/><w:keepLines/>"
BORDER = '<w:{0} w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
BORDERS = "<w:tblBorders>" + "".join(BORDER.format(b) for b in
                                      ("top", "left", "bottom", "right", "insideH", "insideV")) + "</w:tblBorders>"

STYLES = [
    style("Normal", "Normal", based=None, custom=False, ppr=sp(), rpr=ARIAL + sz(12) + BLACK),
    style("BodyText", "Body Text", custom=False,
          ppr=sp(0, 120, 360) + f'<w:ind w:firstLine="{int(1.25 * CM)}"/>' + BOTH),
    style("FirstParagraph", "First Paragraph", based="BodyText", next_="BodyText"),
    style("Compact", "Compact", ppr=sp(20, 20) + '<w:ind w:firstLine="0"/>' + LEFT, rpr=sz(10)),
    style("Heading1", "heading 1", custom=False, next_="BodyText",
          ppr=KEEP + "<w:pageBreakBefore/>" + sp(0, 360, 360) + LEFT + '<w:outlineLvl w:val="0"/>',
          rpr=ARIAL + B + CAPS + sz(12) + BLACK),
    style("Heading2", "heading 2", custom=False, next_="BodyText",
          ppr=KEEP + sp(240, 120, 360) + LEFT + '<w:outlineLvl w:val="1"/>', rpr=ARIAL + B + sz(12) + BLACK),
    style("Heading3", "heading 3", custom=False, next_="BodyText",
          ppr=KEEP + sp(240, 120, 360) + LEFT + '<w:outlineLvl w:val="2"/>', rpr=ARIAL + B + sz(12) + BLACK),
    style("Caption", "caption", custom=False, ppr="<w:keepNext/>" + sp(240, 60) + CENTER, rpr=sz(10)),
    style("TableCaption", "Table Caption", based="Caption", ppr="<w:keepNext/>"),
    style("ImageCaption", "Image Caption", based="Caption"),
    style("Legenda", "Legenda", based="Caption", ppr="<w:keepNext/>"),
    style("Fonte", "Fonte", ppr=sp(60, 240) + LEFT, rpr=sz(10)),
    style("Figure", "Figure", ppr="<w:keepNext/>" + sp() + CENTER),
    style("CaptionedFigure", "Captioned Figure", based="Figure", ppr="<w:keepNext/>"),
    style("Figura", "Figura", ppr="<w:keepNext/>" + sp() + CENTER),
    style("CapaInstituicao", "Capa Instituição", ppr=sp(0, 120, 360) + CENTER, rpr=B + CAPS + sz(12)),
    style("CapaAutores", "Capa Autores", ppr=sp(3 * CM, 0, 360) + CENTER, rpr=B + CAPS + sz(12)),
    style("CapaTitulo", "Capa Título", ppr=sp(6 * CM, 240, 360) + CENTER, rpr=B + CAPS + sz(14)),
    style("CapaSubtitulo", "Capa Subtítulo", ppr=sp(0, 0, 360) + CENTER, rpr=sz(12)),
    style("CapaLocal", "Capa Local", ppr=sp(7 * CM, 0, 360) + CENTER, rpr=B + sz(12)),
    style("SumarioTitulo", "Sumário Título", ppr="<w:pageBreakBefore/>" + sp(0, 480, 360) + CENTER,
          rpr=B + CAPS + sz(12)),
    style("TOC1", "toc 1", custom=False, next_="Normal",
          ppr=f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_W_PORTRAIT}"/></w:tabs>' + sp(120, 60, 360),
          rpr=B + CAPS + sz(12)),
    style("TOC2", "toc 2", custom=False, next_="Normal",
          ppr=f'<w:tabs><w:tab w:val="right" w:leader="dot" w:pos="{TEXT_W_PORTRAIT}"/></w:tabs>' + sp(0, 60, 360),
          rpr=sz(12)),
    style("Header", "header", custom=False, ppr=sp() + '<w:jc w:val="right"/>', rpr=sz(10)),
    style("Table", "Table", based="TableNormal", typ="table",
          extra=("<w:tblPr>" + BORDERS +
                 '<w:tblCellMar><w:top w:w="57" w:type="dxa"/><w:left w:w="57" w:type="dxa"/>'
                 '<w:bottom w:w="57" w:type="dxa"/><w:right w:w="57" w:type="dxa"/></w:tblCellMar></w:tblPr>'
                 '<w:tblStylePr w:type="firstRow"><w:rPr>' + B + '</w:rPr><w:tcPr>'
                 '<w:shd w:val="clear" w:color="auto" w:fill="D9D9D9"/></w:tcPr></w:tblStylePr>')),
]

DOC_DEFAULTS = ("<w:docDefaults><w:rPrDefault><w:rPr>" + ARIAL + sz(12) +
                '<w:lang w:val="pt-BR" w:eastAsia="pt-BR" w:bidi="ar-SA"/></w:rPr></w:rPrDefault>'
                "<w:pPrDefault><w:pPr>" + sp() + "</w:pPr></w:pPrDefault></w:docDefaults>")

# seção final = Apêndice B: A4 paisagem, margens ABNT (sup. 3, esq. 3, inf. 2, dir. 2)
SECT_LANDSCAPE = (f'<w:sectPr><w:pgSz w:w="16838" w:h="11906" w:orient="landscape"/>'
                  f'<w:pgMar w:top="{3 * CM}" w:right="{2 * CM}" w:bottom="{2 * CM}" w:left="{3 * CM}" '
                  f'w:header="{int(1.25 * CM)}" w:footer="{int(1.25 * CM)}" w:gutter="0"/></w:sectPr>')


def main():
    default = subprocess.run(["pandoc", "--print-default-data-file", "reference.docx"],
                             check=True, capture_output=True).stdout
    tmp = OUT + ".tmp"
    open(tmp, "wb").write(default)
    zin = zipfile.ZipFile(tmp)
    files = {n: zin.read(n) for n in zin.namelist()}
    zin.close()

    st = files["word/styles.xml"].decode("utf-8")
    st = re.sub(r"<w:docDefaults>.*?</w:docDefaults>", DOC_DEFAULTS, st, count=1, flags=re.S)
    for s in STYLES:
        sid = re.search(r'w:styleId="([^"]+)"', s).group(1)
        st = re.sub(r'<w:style [^>]*w:styleId="%s".*?</w:style>' % sid, "", st, flags=re.S)
    st = st.replace("</w:styles>", "".join(STYLES) + "</w:styles>")
    files["word/styles.xml"] = st.encode("utf-8")

    doc = files["word/document.xml"].decode("utf-8")
    assert doc.count("<w:sectPr />") == 1, "sectPr inesperado no modelo do pandoc"
    files["word/document.xml"] = doc.replace("<w:sectPr />", SECT_LANDSCAPE).encode("utf-8")

    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for n, b in files.items():
            z.writestr(n, b)
    import os
    os.remove(tmp)
    print("modelo gerado:", OUT)


if __name__ == "__main__":
    main()
