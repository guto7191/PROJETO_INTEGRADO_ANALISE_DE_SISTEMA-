# Como inserir o sumário no Google Docs

O `Fase1_Consolidado.docx` já vem com a página **SUMÁRIO** reservada (logo depois da capa) e com todos os
títulos marcados como **Título 1** (seções principais) e **Título 2** (subseções). O sumário em si é o
**índice nativo do Google Docs**: clicável, com números de página e atualizável com um clique.

1. No Google Drive, abra o `.docx` e use **Arquivo → Salvar como Documentos Google**
   (o índice só existe em documento do Docs).
2. Clique no parágrafo vazio logo abaixo do título **SUMÁRIO**.
3. **Inserir → Índice** → escolha o estilo **com números de página**
   (se aparecer a opção **pontilhado**, prefira-a).
4. O índice sai com dois níveis, o 2º recuado. Selecione as linhas das seções principais
   (as em MAIÚSCULAS) e aplique **negrito**.
5. Depois de qualquer edição no documento: clique no índice → botão **↻ Atualizar**.
6. Entrega em PDF: **Arquivo → Fazer download → Documento PDF**. As linhas do sumário continuam
   clicáveis no PDF.

Conferência rápida: o índice deve ter 7 itens principais (1 a 5, Apêndice A, Apêndice B) e 16 subitens;
clicar em cada linha deve levar ao título correspondente.

Para regerar o `.docx` depois de mudar o Markdown ou os diagramas: `bash docs/build_docx.sh docs/fase1`
(na raiz do repositório). Depois disso, repita os passos acima no novo arquivo.
