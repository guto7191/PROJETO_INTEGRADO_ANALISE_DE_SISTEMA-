"""Pós-processa o .docx gerado pelo pandoc para o padrão ABNT do projeto.

Uso: python3 -I docs/ferramentas/pos_docx.py <arquivo.docx>

1. Cria dois cabeçalhos: vazio (capa e sumário) e com número de página à direita.
2. Troca os marcadores do Markdown por quebras de seção:
     @@SECAO_SEM_NUMERO@@ -> fim da seção 1 (capa + sumário, retrato, sem número visível)
     @@SECAO_RETRATO@@    -> fim da seção 2 (texto, retrato, com número)
   A seção final (Apêndice B) vem do reference.docx em paisagem e recebe o cabeçalho com número.
3. Evita página em branco: o primeiro título de cada seção nova não quebra página de novo.
4. Repete a linha de cabeçalho das tabelas em cada página.
5. Pede ao Word para atualizar os campos (sumário) ao abrir.
Para com erro se algum marcador não aparecer exatamente uma vez.
"""
import re
import sys
import zipfile

PATH = sys.argv[1]
CM = 567
W_NS = 'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"'
R_NS = 'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
HDR_TYPE = "application/vnd.openxmlformats-officedocument.wordprocessingml.header+xml"
HDR_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/header"

HDR_VAZIO = f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {W_NS} {R_NS}><w:p/></w:hdr>'
HDR_NUM = (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><w:hdr {W_NS} {R_NS}><w:p><w:pPr>'
           '<w:pStyle w:val="Header"/><w:jc w:val="right"/></w:pPr>'
           '<w:r><w:fldChar w:fldCharType="begin"/></w:r><w:r><w:instrText xml:space="preserve"> PAGE </w:instrText></w:r>'
           '<w:r><w:fldChar w:fldCharType="separate"/></w:r><w:r><w:t>1</w:t></w:r>'
           '<w:r><w:fldChar w:fldCharType="end"/></w:r></w:p></w:hdr>')


def sect_portrait(hdr_rid):
    return (f'<w:sectPr><w:headerReference w:type="default" r:id="{hdr_rid}"/>'
            f'<w:type w:val="nextPage"/><w:pgSz w:w="11906" w:h="16838"/>'
            f'<w:pgMar w:top="{3 * CM}" w:right="{2 * CM}" w:bottom="{2 * CM}" w:left="{3 * CM}" '
            f'w:header="{int(1.25 * CM)}" w:footer="{int(1.25 * CM)}" w:gutter="0"/></w:sectPr>')


TEXT_W_PORTRAIT = 21 * CM - 5 * CM           # 16 cm úteis
TEXT_W_LANDSCAPE = int(29.7 * CM) - 5 * CM   # 24,7 cm úteis
CELL_PAD = 2 * 57 + 40                       # margens internas da célula + folga (twips)
_FONTS = {}


def text_twips(word, bold):
    """Largura de uma palavra em Arial 10 pt (métrica Liberation Sans), em twips."""
    from PIL import ImageFont
    if bold not in _FONTS:
        _FONTS[bold] = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-%s.ttf"
                                          % ("Bold" if bold else "Regular"), 100)
    return _FONTS[bold].getlength(word) / 10 * 20        # 100 px -> 10 pt; 1 pt = 20 twips


def fix_table(tbl, width):
    rows = re.findall(r"<w:tr>.*?</w:tr>", tbl, re.S)
    cells = [[re.sub(r"<[^>]+>", " ", c).split() for c in re.findall(r"<w:tc>.*?</w:tc>", r, re.S)] for r in rows]
    ncol = max(len(r) for r in cells)
    minw = [0.0] * ncol
    weight = [0.0] * ncol
    for ri, r in enumerate(cells):
        for ci, words in enumerate(r):
            for w in words:
                minw[ci] = max(minw[ci], text_twips(w, ri == 0) + CELL_PAD)
            weight[ci] += text_twips(" ".join(words), ri == 0)
    rest = width - sum(minw)
    if rest < 0:
        sys.exit(f"ERRO: tabela não cabe sem quebrar palavras ({sum(minw):.0f} > {width} twips)")
    total = sum(weight) or 1
    cols = [int(minw[i] + rest * weight[i] / total) for i in range(ncol)]
    cols[-1] += width - sum(cols)
    tbl = re.sub(r'<w:tblW [^>]*/>', f'<w:tblW w:type="dxa" w:w="{width}" /><w:tblLayout w:type="fixed" />', tbl, 1)
    tbl = re.sub(r"<w:tblGrid>.*?</w:tblGrid>",
                 "<w:tblGrid>" + "".join(f'<w:gridCol w:w="{c}" />' for c in cols) + "</w:tblGrid>", tbl, 1, re.S)

    def fix_row(m):
        row = m.group(0)
        i = iter(cols)
        row = re.sub(r"<w:tcPr />|<w:tcPr>", lambda _: f'<w:tcPr><w:tcW w:type="dxa" w:w="{next(i)}" />'
                     + ("</w:tcPr>" if _.group(0) == "<w:tcPr />" else ""), row)
        if "<w:trPr>" in row:
            row = row.replace("<w:trPr>", "<w:trPr><w:cantSplit />", 1)
        else:
            row = row.replace("<w:tr>", "<w:tr><w:trPr><w:cantSplit /></w:trPr>", 1)
        return row
    tbl = re.sub(r"<w:tr>.*?</w:tr>", fix_row, tbl, flags=re.S)
    if tbl.count("tblHeader") != 1:
        sys.exit("ERRO: o cabeçalho repetido deve estar só na primeira linha da tabela")
    return tbl


def build_toc(doc):
    """Preenche o campo TOC com os títulos (níveis 1 e 2) e links para eles, já no arquivo.

    Editores que não calculam campos (Google Docs) mostram o sumário pronto; o Word ainda pode
    recalculá-lo (com números de página) porque o campo TOC continua em volta das entradas.
    """
    entries = []

    def mark(m):
        k = len(entries)
        lvl, body = m.group(1), m.group(0)
        text = "".join(re.findall(r"<w:t[^>]*>([^<]*)</w:t>", body))
        entries.append((lvl, text, f"_Toc{k:04d}"))
        body = body.replace("</w:pPr>", f'</w:pPr><w:bookmarkStart w:id="{900 + k}" w:name="_Toc{k:04d}"/>', 1)
        return body[:-len("</w:p>")] + f'<w:bookmarkEnd w:id="{900 + k}"/></w:p>'
    doc = re.sub(r'<w:p><w:pPr><w:pStyle w:val="Heading([12])" />(?:(?!</w:p>).)*</w:p>', mark, doc, flags=re.S)
    if not entries:
        sys.exit("ERRO: nenhum título encontrado para o sumário")

    def entry(lvl, text, anchor, prefix="", suffix=""):
        return (f'<w:p><w:pPr><w:pStyle w:val="TOC{lvl}"/></w:pPr>{prefix}'
                f'<w:hyperlink w:anchor="{anchor}" w:history="1"><w:r><w:t xml:space="preserve">{text}</w:t></w:r>'
                f'</w:hyperlink>{suffix}</w:p>')
    begin = ('<w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r><w:r><w:instrText xml:space="preserve">'
             ' TOC \\o "1-2" \\h \\z \\u </w:instrText></w:r><w:r><w:fldChar w:fldCharType="separate"/></w:r>')
    end = '<w:r><w:fldChar w:fldCharType="end"/></w:r>'
    paras = []
    for i, (lvl, text, anchor) in enumerate(entries):
        paras.append(entry(lvl, text, anchor, begin if i == 0 else "", end if i == len(entries) - 1 else ""))
    pat = re.compile(r'<w:p><w:r><w:fldChar w:fldCharType="begin" w:dirty="true"/></w:r>.*?Atualize o sumário.*?</w:p>', re.S)
    if len(pat.findall(doc)) != 1:
        sys.exit("ERRO: campo do sumário não encontrado exatamente uma vez")
    return pat.sub(lambda _: "".join(paras), doc), len(entries)


def no_break_on_next_heading(doc, start):
    """Desliga a quebra de página do primeiro Heading1 depois de 'start'."""
    i = doc.index('<w:pStyle w:val="Heading1" />', start)
    return doc[:i] + '<w:pStyle w:val="Heading1" /><w:pageBreakBefore w:val="0"/>' + doc[i + len('<w:pStyle w:val="Heading1" />'):]


def main():
    z = zipfile.ZipFile(PATH)
    files = {n: z.read(n) for n in z.namelist()}
    z.close()
    doc = files["word/document.xml"].decode("utf-8")

    # 1 cabeçalhos
    files["word/header_vazio.xml"] = HDR_VAZIO.encode()
    files["word/header_numero.xml"] = HDR_NUM.encode()
    rels = files["word/_rels/document.xml.rels"].decode()
    rels = rels.replace("</Relationships>",
                        f'<Relationship Id="rIdHdrVazio" Type="{HDR_REL}" Target="header_vazio.xml"/>'
                        f'<Relationship Id="rIdHdrNum" Type="{HDR_REL}" Target="header_numero.xml"/></Relationships>')
    files["word/_rels/document.xml.rels"] = rels.encode()
    ct = files["[Content_Types].xml"].decode()
    ct = ct.replace("</Types>", f'<Override PartName="/word/header_vazio.xml" ContentType="{HDR_TYPE}"/>'
                                f'<Override PartName="/word/header_numero.xml" ContentType="{HDR_TYPE}"/></Types>')
    files["[Content_Types].xml"] = ct.encode()

    # 2 marcadores -> quebras de seção
    for marker, rid in (("@@SECAO_SEM_NUMERO@@", "rIdHdrVazio"), ("@@SECAO_RETRATO@@", "rIdHdrNum")):
        pat = re.compile(r"<w:p>\s*<w:r>\s*<w:t>" + marker + r"</w:t>\s*</w:r>\s*</w:p>")
        found = pat.findall(doc)
        if len(found) != 1:
            sys.exit(f"ERRO: marcador {marker} encontrado {len(found)} vez(es)")
        doc = pat.sub(f"<w:p><w:pPr>{sect_portrait(rid)}</w:pPr></w:p>", doc)
        # 3 primeiro título da seção seguinte não quebra página de novo
        doc = no_break_on_next_heading(doc, doc.index(f'r:id="{rid}"'))
    if "@@" in doc:
        sys.exit("ERRO: sobrou marcador @@ no documento")

    # seção final (paisagem, do modelo) recebe o cabeçalho com número
    body = doc.rindex("<w:sectPr")
    if 'w:orient="landscape"' not in doc[body:]:
        sys.exit("ERRO: a seção final não está em paisagem — confira o reference.docx")
    doc = doc[:body] + doc[body:].replace("<w:sectPr>", '<w:sectPr><w:headerReference w:type="default" r:id="rIdHdrNum"/>', 1)
    if 'xmlns:r=' not in doc[:2000]:
        doc = doc.replace("<w:document ", f"<w:document {R_NS} ", 1)

    # 4 tabelas: larguras pela palavra mais longa, cabeçalho repetido só na 1ª linha, linhas sem quebra
    landscape_from = doc.index('r:id="rIdHdrNum"')          # depois desta quebra, a seção é paisagem
    doc = re.sub(r"<w:tbl>.*?</w:tbl>",
                 lambda m: fix_table(m.group(0), TEXT_W_LANDSCAPE if m.start() > landscape_from else TEXT_W_PORTRAIT),
                 doc, flags=re.S)

    # 4b sumário já preenchido (títulos + links)
    doc, n_toc = build_toc(doc)
    print("sumário com", n_toc, "entradas")

    files["word/document.xml"] = doc.encode("utf-8")

    # 5 atualizar campos ao abrir
    st = files["word/settings.xml"].decode()
    if "updateFields" not in st:
        st = re.sub(r"(<w:zoom [^>]*/>)", r'\1<w:updateFields w:val="true"/>', st, count=1)
    files["word/settings.xml"] = st.encode()

    with zipfile.ZipFile(PATH, "w", zipfile.ZIP_DEFLATED) as out:
        for n, b in files.items():
            out.writestr(n, b)
    print("pós-processado:", PATH)


if __name__ == "__main__":
    main()
