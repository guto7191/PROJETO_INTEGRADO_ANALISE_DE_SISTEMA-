"""Limpa a coluna Origem e escreve, abaixo de cada quadro, a nota que explica os códigos usados nele.

Uso: python3 -I docs/ferramentas/notas_quadros.py docs/fase1/Fase1_Consolidado.md

1. Coluna Origem (última coluna "Origem"): remove códigos de decisão interna (D1, D21…), que ficam
   só em DECISOES.md; aplica as origens fixas de ORIGEM_FIXA; troca "Diretriz".
2. Para cada quadro, troca o bloco "Fonte" por "Fonte: … + Nota: <códigos presentes no quadro>".
Pode ser rodado de novo: a nota é sempre recalculada. Para com erro se a numeração dos quadros
não bater com CODIGOS ou se alguma célula de Origem ficar vazia.
"""
import re
import sys

PATH = sys.argv[1]

# origem a usar quando, sem os códigos D, a célula ficaria vazia ou precisa de fonte específica
ORIGEM_FIXA = {
    "RN08": "Minimundo, seção 4",
    "RN09": "Minimundo, seção 4",
    "RN13": "RN-MM-14, Minimundo, seção 4",
    "RNF04": "LGPD (Lei 13.709/2018)",
    "RNF06": "—",
}

# (código, regex de detecção, definição, quadros onde está definido, trecho esperado na legenda)
CODIGOS = [
    ("RF", r"\bRF\d\d\b", "RF = requisito funcional", range(2, 8), "Requisitos funcionais"),
    ("RNF", r"\bRNF\d\d\b", "RNF = requisito não funcional", range(9, 10), "Requisitos não funcionais"),
    ("RN", r"\bRN\d\d\b", "RN = regra de negócio do sistema", range(10, 11), "Regras de negócio"),
    ("RN-MM", r"\bRN-MM-\d\d\b", "RN-MM-nn = regra nº nn da seção 2 do minimundo", range(11, 12), "Regras do minimundo"),
    ("Q", r"\bQ-\d\d\b", "Q-nn = pergunta nº nn da seção 5 do minimundo", range(12, 13), "Perguntas do minimundo"),
    ("F", r"\bF[1-6]\b", "F1 a F6 = fluxos de informação da Figura 1", None, None),
    ("LGPD", r"\bLGPD\b", "LGPD = Lei Geral de Proteção de Dados Pessoais (Lei 13.709/2018)", None, None),
]

FONTE_RE = re.compile(r'::: \{custom-style="Fonte"\}\nFonte: elaborado pelos autores \(2026\)\.(?:\\\nNota: [^\n]*)?\n:::')


def ref(quadros, atual):
    if quadros is None or atual in quadros:
        return ""
    q = list(quadros)
    return f" (Quadro {q[0]})" if len(q) == 1 else f" (Quadros {q[0]} a {q[-1]})"


def main():
    s = open(PATH, encoding="utf-8").read()
    legendas = {int(n): t for n, t in re.findall(r"^Table: Quadro (\d+) — (.+)$", s, re.M)}
    if sorted(legendas) != list(range(1, len(legendas) + 1)):
        sys.exit(f"ERRO: quadros fora de sequência: {sorted(legendas)}")
    for cod, _, _, quadros, trecho in CODIGOS:
        for q in quadros or []:
            if trecho not in legendas.get(q, ""):
                sys.exit(f"ERRO: o Quadro {q} deveria ser '{trecho}…' (é '{legendas.get(q)}'); ajuste CODIGOS")

    lines = s.split("\n")
    out, i, n = [], 0, 0
    while i < len(lines):
        if not (lines[i].startswith("|") and i + 1 < len(lines) and re.fullmatch(r"\|[-: |]+\|", lines[i + 1])):
            out.append(lines[i])
            i += 1
            continue
        header = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        origem_ultima = header[-1] == "Origem"
        block = [lines[i], lines[i + 1]]
        i += 2
        while i < len(lines) and lines[i].startswith("|"):
            row = lines[i]
            if origem_ultima:
                cells = row.strip().strip("|").split("|")
                rid = cells[0].strip()
                orig = [x.strip() for x in cells[-1].split(",")]
                orig = [x for x in orig if x and not re.fullmatch(r"D\d+", x) and x != "Diretriz"]
                novo = ORIGEM_FIXA.get(rid, ", ".join(orig))
                if not novo:
                    sys.exit(f"ERRO: {rid} ficaria sem origem; acrescente em ORIGEM_FIXA")
                cells[-1] = f" {novo} "
                row = "|" + "|".join(cells) + "|"
            block.append(row)
            i += 1
        n += 1
        texto = "\n".join(block)
        presentes = [c for c in CODIGOS if re.search(c[1], texto)]
        nota = "; ".join(defn + ref(q, n) for _, _, defn, q, _ in presentes)
        out += block
        # copiar até o bloco Fonte deste quadro e substituí-lo
        resto = "\n".join(lines[i:])
        m = FONTE_RE.search(resto)
        if not m or "\n# " in resto[:m.start()] or "|" in resto[:m.start()].replace("Table:", ""):
            sys.exit(f"ERRO: bloco Fonte do quadro {n} não encontrado logo após a tabela")
        fonte = '::: {custom-style="Fonte"}\nFonte: elaborado pelos autores (2026).' + \
                (f"\\\nNota: {nota}." if nota else "") + "\n:::"
        novo_resto = resto[:m.start()] + fonte + resto[m.end():]
        lines = lines[:i] + novo_resto.split("\n")
    if n != len(legendas):
        sys.exit(f"ERRO: {n} tabelas para {len(legendas)} legendas")
    s = "\n".join(out)
    if re.search(r"\bD\d{1,2}\b", s) or "Diretriz" in s:
        sys.exit("ERRO: ainda há código D ou 'Diretriz' no documento")
    open(PATH, "w", encoding="utf-8").write(s)
    print(f"{n} quadros: origem limpa e notas atualizadas")


if __name__ == "__main__":
    main()
