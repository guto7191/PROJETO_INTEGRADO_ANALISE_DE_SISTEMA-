"""Gera os diagramas da Fase 1 do ProspectaUni (.drawio editáveis) e verifica o layout.

Uso (na raiz do repositório):
    python3 -I docs/ferramentas/diagramas/gen_diagramas.py docs/fase1 [pasta_previa] [01 02 03]

Fonte base de 16 px numa tela de 1400 px: impresso a ~24 cm de largura, o texto fica com ~7,8 pt.
Título e "Como ler" de cada figura ficam no documento (legenda ABNT), não na imagem.
"""
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from engine import Diagram, font  # noqa: E402

FASE1 = sys.argv[1]
PREV = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].isdigit() else None
ONLY = [a for a in sys.argv[2:] if a.isdigit()] or ["01", "02", "03"]
RENDER = os.path.join(HERE, "..", "render_drawio.py")


def read(p):
    return open(os.path.join(FASE1, p), encoding="utf-8").read()


GLOSS = set(re.findall(r"^\| ([^|]+?) \|", read("02-glossario.md"), re.M)) - {"Termo"}
RFS = set(re.findall(r"^\| (RF\d\d) \|", read("03-requisitos-funcionais.md"), re.M))
RNS = set(re.findall(r"^\| (RN\d\d) \|", read("05-regras-de-negocio.md"), re.M))

UP, RT, LF = (0, -12), (14, 0), (-14, 0)     # deslocamentos de cardinalidade
BELOW = (0, 14)                               # verbo abaixo de linhas horizontais


def legend_col(D, x, y, w, items):
    """Legenda vertical. items: (rótulo, tipo, paleta) — tipo: box | dashed | dline | dotted."""
    rowh = 30
    D.n("leg", "", x, y, w, 40 + rowh * len(items), kind="container", rounded=False, fit=False)
    D.n("leg_t", "Legenda", x + 12, y + 6, 100, 26, kind="text", fs=15, bold=True, align="left", parent="leg")
    for i, (txt, typ, pal) in enumerate(items):
        yy = y + 38 + i * rowh
        if typ in ("box", "dashed"):
            D.n(f"leg_s{i}", "", x + 12, yy + 3, 44, 20, pal=pal, dashed=typ == "dashed", parent="leg", fit=False)
        else:
            a = D.n(f"leg_a{i}", "", x + 12, yy + 12, 1, 1, kind="text", parent="leg", fit=False)
            b = D.n(f"leg_b{i}", "", x + 56, yy + 12, 1, 1, kind="text", parent="leg", fit=False)
            D.e(f"leg_e{i}", a.id, b.id, [(x + 13, yy + 13), (x + 56, yy + 13)],
                style="dotted" if typ == "dotted" else "solid", arrow=typ == "dline")
        D.n(f"leg_l{i}", txt, x + 66, yy, w - 74, 26, kind="text", fs=14, align="left", parent="leg")


def legend_row(D, x, y, w, items, note):
    D.n("leg", "", x, y, w, 46, kind="container", rounded=False, fit=False)
    D.n("leg_t", "Legenda", x + 12, y + 10, 76, 26, kind="text", fs=15, bold=True, align="left", parent="leg")
    xx = x + 96
    for i, (txt, pal) in enumerate(items):
        D.n(f"leg_s{i}", "", xx, y + 13, 40, 20, pal=pal, parent="leg", fit=False, sw=2 if pal == "ponte" else 1)
        tw = font(14).getlength(txt) + 14
        D.n(f"leg_l{i}", txt, xx + 46, y + 10, tw, 26, kind="text", fs=14, align="left", parent="leg")
        xx += 46 + tw + 12
    D.n("leg_n", note, xx, y + 10, x + w - xx - 8, 26, kind="text", fs=14, align="left", parent="leg")


# =====================================================================
def d01():
    D = Diagram("01-contexto", 1400, 690)
    D.n("fronteira", "Fronteira do sistema", 560, 190, 520, 330, kind="container", pal="fora", dashed=True,
        rounded=False, fs=15, align="left", valign="top", fit=False, extra="spacingLeft=8;spacingTop=2;")
    D.n("sistema", "<b>ProspectaUni</b><br>Sistema de Captação e Prospecção<br>de Projetos Universitários",
        620, 250, 400, 150, pal="sis", fs=17, parent="fronteira")
    D.n("gestor", "<b>Gestor de PD&amp;I</b><br>do Departamento<br><i>ator principal</i>", 40, 250, 240, 130, pal="ator")
    D.n("docente", "<b>Docente</b>", 720, 30, 200, 60, pal="ator")
    D.n("repr", "<b>Representante</b><br><b>de Empresa</b>", 720, 600, 200, 70, pal="ator")
    D.n("externo", "Sistemas acadêmicos externos<br>(ex.: Lattes)<br><i>fora do escopo — evolução futura</i>",
        40, 560, 300, 100, pal="fora", dashed=True, fs=15)
    for i, (y, l) in enumerate(zip((270, 305, 340), ("F1 cadastros", "F2 oportunidades e estados",
                                                       "F3 validação, propostas, desfecho"))):
        D.e(f"f{i + 1}", "gestor", "sistema", [(280, y), (620, y)], label=l, t=0.41)
    D.e("f4", "sistema", "gestor", [(620, 370), (280, 370)], label="F4 aderências e consultas", t=0.59)
    D.e("f5", "docente", "sistema", [(820, 90), (820, 250)], label="F5 expertises e portfólio", t=0.31)
    D.e("f6", "repr", "sistema", [(820, 600), (820, 400)], label="F6 manifestação de interesse", t=0.2)
    D.e("fx", "externo", "fronteira", [(340, 610), (600, 610), (600, 520)], label="sem integração",
        t=0.37, style="dotted", arrow=False)
    legend_col(D, 1120, 440, 270, [("Ator", "box", "ator"), ("Sistema", "box", "sis"),
                                   ("Fronteira / fora do escopo", "dashed", "fora"),
                                   ("Fluxo de informação (F1–F6)", "dline", None),
                                   ("Relação sem integração", "dotted", None)])
    return D


# =====================================================================
def d02():
    D = Diagram("02-mapa-dominio", 1400, 800)
    cont = dict(kind="container", rounded=False, fs=16, bold=True, align="left", valign="top", fit=False,
                extra="spacingLeft=10;spacingTop=4;")
    D.n("g_uni", "Universidade", 20, 20, 470, 360, pal="uniC", **cont)
    D.n("g_ind", "Indústria", 830, 20, 550, 360, pal="indC", **cont)
    D.n("g_pro", "Prospecção e Parceria", 20, 410, 1360, 310, pal="proC", **cont)

    def T(id, term, x, y, w=170, h=60, pal="uni", parent=None, label=None, **k):
        return D.n(id, label or term, x, y, w, h, pal=pal, parent=parent, term=term, **k)

    T("docente", "Docente", 50, 80, parent="g_uni")
    T("expertise", "Expertise", 310, 80, parent="g_uni")
    T("portfolio", "Portfólio Acadêmico", 50, 270, parent="g_uni", label="Portfólio<br>Acadêmico")
    T("projeto", "Projeto Acadêmico", 310, 270, parent="g_uni", label="Projeto<br>Acadêmico")
    T("area", "Área de Conhecimento", 560, 145, 200, 110, pal="ponte", sw=3,
      label="<b>Área de</b><br><b>Conhecimento</b><br><i>critério de cruzamento</i><br><i>docente × oportunidade</i>")
    T("setor", "Setor Industrial", 860, 80, 190, pal="ind", parent="g_ind")
    T("empresa", "Empresa", 1160, 80, 190, pal="ind", parent="g_ind")
    T("oport", "Desafio/Oportunidade", 860, 230, 190, pal="ind", parent="g_ind", label="Desafio/<br>Oportunidade")
    T("ga", "Grau de Aderência", 60, 500, 190, pal="pro", parent="g_pro")
    T("compat", "Compatibilidade", 380, 500, 190, pal="pro", parent="g_pro")
    T("proposta", "Proposta", 860, 520, 190, pal="pro", parent="g_pro")
    T("manif", "Manifestação de Interesse", 1160, 520, 190, pal="pro", parent="g_pro",
      label="Manifestação de<br>Interesse")
    T("parceria", "Parceria", 860, 650, 190, pal="pro", parent="g_pro")
    D.n("nota_ga", "<b>Grau de Aderência</b> (0 a 100) = 70 × cobertura das áreas exigidas + 30 × projetos "
        "relacionados (até 3) ÷ 3.<br>O sistema sugere o docente quando o grau é ≥ 50; o Gestor valida com "
        "justificativa (RN01–RN05).", 60, 610, 760, 70, pal="nota", fs=15, align="left", parent="g_pro",
        extra="spacingLeft=8;")
    A = dict(arrow=False)
    D.e("r1", "docente", "expertise", [(220, 110), (310, 110)], "domina", off=BELOW, ends=[("N", 0, UP), ("N", 1, UP)], **A)
    D.e("r2", "docente", "portfolio", [(135, 140), (135, 270)], "possui", ends=[("1", 0, RT), ("1", 1, RT)], **A)
    D.e("r3", "portfolio", "projeto", [(220, 300), (310, 300)], "reúne", off=BELOW, ends=[("1", 0, UP), ("N", 1, UP)], **A)
    D.e("r4", "expertise", "area", [(480, 110), (600, 110), (600, 145)], "pertence a", t=0.42, off=BELOW,
        ends=[("N", 0, UP), ("1", 1, RT)], **A)
    D.e("r5", "projeto", "area", [(480, 300), (620, 300), (620, 255)], "aborda", t=0.38, off=BELOW,
        ends=[("N", 0, UP), ("N", 1, RT)], **A)
    D.e("r6", "oport", "area", [(860, 245), (760, 245)], "exige", off=BELOW, ends=[("N", 0, UP), ("N", 1, UP)], **A)
    D.e("r7", "setor", "oport", [(955, 140), (955, 230)], "apresenta", ends=[("1", 0, RT), ("N", 1, RT)], **A)
    D.e("r8", "setor", "empresa", [(1050, 110), (1160, 110)], "reúne", off=BELOW, ends=[("N", 0, UP), ("N", 1, UP)], **A)
    D.e("r9", "compat", "docente", [(420, 500), (420, 395), (35, 395), (35, 110), (50, 110)], "avalia", t=0.373,
        ends=[("N", 0, RT), ("1", 1, UP)], **A)
    D.e("r10", "compat", "oport", [(520, 500), (520, 440), (900, 440), (900, 290)], "refere-se a", t=0.42,
        ends=[("N", 0, RT), ("1", 1, LF)], **A)
    D.e("r11", "compat", "ga", [(380, 530), (250, 530)], "é medida por", off=BELOW, ends=[("1", 0, UP), ("1", 1, UP)], **A)
    D.e("r12", "empresa", "manif", [(1255, 140), (1255, 520)], "registra", ends=[("1", 0, RT), ("N", 1, RT)], **A)
    D.e("r13", "manif", "oport", [(1200, 520), (1200, 260), (1050, 260)], "refere-se a", t=0.82, off=BELOW,
        ends=[("N", 0, LF), ("1", 1, UP)], **A)
    D.e("r14", "oport", "proposta", [(980, 290), (980, 520)], "origina", t=0.6,
        ends=[("1", 0, RT), ("0..N", 1, (22, 0))], **A)
    D.e("r15", "proposta", "manif", [(1050, 550), (1160, 550)], "responde a", off=BELOW,
        ends=[("0..1", 0, (6, -12)), ("1", 1, UP)], **A)
    D.e("r16", "proposta", "compat", [(860, 550), (570, 550)], "inclui", off=BELOW, ends=[("N", 0, UP), ("N", 1, UP)], **A)
    D.e("r17", "proposta", "parceria", [(955, 580), (955, 650)], "pode resultar em", off=(86, 0),
        ends=[("1", 0, LF), ("0..1", 1, (-22, 0))], **A)
    legend_row(D, 20, 740, 1360, [("Universidade", "uni"), ("Indústria", "ind"), ("Prospecção e Parceria", "pro"),
                                   ("Critério de cruzamento", "ponte")],
               "1 = um · N = vários · 0..1 = nenhum ou um · 0..N = nenhum ou vários")
    return D


# =====================================================================
def d03():
    D = Diagram("03-fluxo-parceria", 1400, 760)
    for id, lab, y, h in (("lane_g", "Gestor de PD&amp;I", 20, 340), ("lane_s", "ProspectaUni", 360, 110),
                          ("lane_d", "Docente", 470, 100), ("lane_e", "Empresa", 570, 110)):
        D.n(id, lab, 20, y, 1370, h, kind="lane", pal="ator", fit=False)
    G = "lane_g"
    D.n("frame", "estados ativos", 88, 128, 1033, 136, kind="container", pal="fora", dashed=True, rounded=False,
        fs=13, align="left", valign="top", parent=G, fit=False, extra="spacingLeft=6;spacingTop=-1;fontStyle=2;")
    D.n("ini", "", 60, 188, 24, 24, kind="ellipse", pal="preto", parent=G, fit=False)
    st = [("s0", "<b>Identificada</b><br>oportunidade<br>registrada (RF06)"),
          ("s1", "<b>Em análise</b><br>aderência calculada<br>e validada (RF09)"),
          ("s2", "<b>Docentes</b><br><b>selecionados</b><br>coordenador<br>definido (RF10)"),
          ("s3", "<b>Proposta em</b><br><b>elaboração</b><br>uma proposta por<br>empresa (RF18)"),
          ("s4", "<b>Em negociação</b><br>negociação com<br>as empresas"),
          ("s5", "<b>Parceria firmada</b><br>parcerias<br>registradas (RF13)")]
    xs = [100 + 211 * i for i in range(6)]
    for (id, lab), x in zip(st, xs):
        D.n(id, lab, x, 150, 165, 100, pal="pro", parent=G, sw=3 if id == "s5" else 1)
    D.e("t_ini", "ini", "s0", [(84, 200), (100, 200)])
    guards = ["[≥ 1 área<br>exigida]<br>(RN08)", "[≥ 1 docente validado,<br>com coordenador]<br>(RN07)",
              "[seleção<br>confirmada]<br>(RN08)", "[≥ 1 proposta<br>registrada]<br>(RN13)",
              "[≥ 1 proposta<br>aceita]<br>(RN10)"]
    for i, g in enumerate(guards):
        D.e(f"t{i}", st[i][0], st[i + 1][0], [(xs[i] + 165, 200), (xs[i + 1], 200)], g, off=(0, -102))
    D.n("fim1", "", 1340, 188, 24, 24, kind="ellipse", pal="preto", parent=G, fit=False, extra="shape=doubleEllipse;")
    D.e("t_fim1", "s5", "fim1", [(1320, 200), (1340, 200)])
    D.n("desc", "<b>Descartada</b><br>motivo registrado (RF13)", 505, 295, 200, 56, pal="pro", parent=G, sw=3)
    D.e("t_desc", "frame", "desc", [(605, 264), (605, 295)], "[motivo informado] (RN09)", off=(102, -3), style="dashed")
    D.n("fim2", "", 725, 311, 24, 24, kind="ellipse", pal="preto", parent=G, fit=False, extra="shape=doubleEllipse;")
    D.e("t_fim2", "desc", "fim2", [(705, 323), (725, 323)])
    D.n("nota_val", "Em análise: a validação exige<br>justificativa ≥ 30 caracteres (RN05);<br>"
        "o valor ajustado prevalece (RN06).", 60, 272, 280, 76, pal="nota", fs=15, align="left", parent=G,
        extra="spacingLeft=6;")
    D.n("nota_par", "Propostas pendentes ainda<br>podem virar parcerias (RN10).", 1140, 272, 240, 56,
        pal="nota", fs=15, align="left", parent=G, extra="spacingLeft=6;")
    D.n("calc", "Calcula o grau de aderência e sugere<br>docentes com grau ≥ 50 (RN01–RN04)",
        253, 380, 280, 70, pal="sis", fs=15, parent="lane_s")
    D.e("i_calc", "calc", "s1", [(393, 380), (393, 250)], "sugestões", style="dotted")
    D.n("doc", "Mantém expertises e<br>portfólio (RF03, RF05)", 60, 490, 250, 60, pal="uni", fs=15, parent="lane_d")
    D.e("i_doc", "doc", "calc", [(310, 520), (430, 520), (430, 450)], "dados de entrada", t=0.82, off=(72, 0),
        style="dotted")
    D.n("emp", "Representante manifesta interesse em<br>oportunidade do seu setor (RF12, RN11)",
        665, 592, 300, 64, pal="ind", fs=15, parent="lane_e")
    D.e("i_emp", "emp", "s3", [(815, 592), (815, 250)], "requisito da proposta (RN13)", t=0.52, style="dotted")
    legend_row(D, 20, 700, 1370, [("Estado da oportunidade", "pro"), ("Atividade do sistema", "sis"),
                                   ("Atividade do Docente", "uni"), ("Atividade da Empresa", "ind")],
               "● início · ◉ fim · borda grossa = estado final")
    return D


# =====================================================================
def run(D):
    errs = D.check(GLOSS, RFS, RNS)
    out = os.path.join(FASE1, "diagramas", D.name + ".drawio")
    open(out, "w", encoding="utf-8").write(D.to_xml())
    print(f"{D.name}: {len(errs)} problema(s)")
    for e in errs:
        print("   -", e)
    if PREV:
        subprocess.run([sys.executable, "-I", RENDER, out, os.path.join(PREV, D.name + ".png"), "1"], check=True)
    return len(errs)


builders = {"01": d01, "02": d02, "03": d03}
total = sum(run(builders[k]()) for k in ONLY)
print("TOTAL de problemas:", total)
sys.exit(1 if total else 0)
