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

    # 4 repetir cabeçalho das tabelas
    doc = re.sub(r"(<w:tbl>.*?<w:tr>)(?!\s*<w:trPr>)", r"\1<w:trPr><w:tblHeader/></w:trPr>", doc, flags=re.S)

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
