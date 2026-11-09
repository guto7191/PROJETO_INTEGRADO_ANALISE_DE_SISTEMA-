#!/usr/bin/env bash
# Gera o documento Word (ABNT) de uma fase do projeto.
#
# Uso (na raiz do repositório):
#   bash docs/build_docx.sh docs/fase1 [Fase1_Consolidado] [--modelo]
#
#   1º argumento: pasta da fase (com o .md e a subpasta diagramas/)
#   2º argumento: nome do .md sem extensão (padrão: Fase1_Consolidado)
#   --modelo     : regera docs/modelo/reference.docx antes
#
# Etapas: modelo de estilos -> PNGs dos .drawio -> pandoc -> pós-processamento ABNT.
set -euo pipefail

DIR="${1:?informe a pasta da fase, ex.: docs/fase1}"
NOME="${2:-Fase1_Consolidado}"
[[ "$NOME" == --* ]] && NOME="Fase1_Consolidado"
RAIZ="$(cd "$(dirname "$0")/.." && pwd)"
FERR="$RAIZ/docs/ferramentas"
MODELO="$RAIZ/docs/modelo/reference.docx"

if [[ ! -f "$MODELO" || " $* " == *" --modelo "* ]]; then
  python3 -I "$FERR/make_reference.py" "$MODELO"
fi

shopt -s nullglob
for f in "$DIR"/diagramas/*.drawio; do
  python3 -I "$FERR/render_drawio.py" "$f" "${f%.drawio}.png" 2
done

( cd "$DIR" && pandoc "$NOME.md" -f markdown -o "$NOME.docx" --reference-doc="$MODELO" --resource-path=. )
python3 -I "$FERR/pos_docx.py" "$DIR/$NOME.docx"
echo "pronto: $DIR/$NOME.docx"
