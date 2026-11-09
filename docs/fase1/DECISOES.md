# Registro de Decisões
> Projeto: ProspectaUni · Fase 1 · Versão 1 · 2026-11-08 · Status: Rascunho

| ID | Data | Pergunta | Resposta | Artefatos afetados |
|----|------|----------|----------|--------------------|
| D1 | 2026-11-08 | Escopo do sistema | Minimundo + ciclo de vida da oportunidade/parceria (da identificação até a parceria firmada ou descartada). | Todos |
| D2 | 2026-11-08 | Atores | Gestor de PD&I do Departamento (principal), Docente, Representante de Empresa. | 00, 01, 03, 05 |
| D3 | 2026-11-08 | Compatibilidade | O sistema calcula o grau de aderência docente×oportunidade; o Gestor valida, podendo ajustar, com justificativa obrigatória. Fórmula pendente (C5). | 03, 05 |
| D4 | 2026-11-08 | Formato de saída | Markdown em docs/fase1/ + um .docx consolidado com capa e índice. | Todos |
| D5 | 2026-11-08 | Nome do sistema na capa | "ProspectaUni — Sistema de Captação e Prospecção de Projetos Universitários" | Todos (capa) |
| D6 | 2026-11-08 | Dados da capa | Universidade: UFRB. Disciplina: "Análise de Sistemas · 2026.2 · Prof. Inácio Borges" (sem nome do curso). Equipe: marcador "[Equipe]"; o usuário pediu para não tratar de equipe/líder. | Consolidado (capa) |
| D7 | 2026-11-08 | Estados do ciclo de vida | Mantidos os 7 estados: Identificada → Em análise → Docentes selecionados → Proposta em elaboração → Em negociação → Parceria firmada \| Descartada. Transições a definir no C5. | 00, 05, diagrama 03 |
| D8 | 2026-11-08 | Quem cadastra os dados | Gestor cadastra setores, empresas, oportunidades e áreas; Docente mantém suas expertises e portfólio; Representante de Empresa manifesta interesse. | 00, 01, 03, 05 |
| D9 | 2026-11-08 | Um departamento e decisão final | Um único departamento; decisão final do Gestor de PD&I. | 00, 05 |
| D10 | 2026-11-08 | Aprovação do 00-premissas-e-escopo.md | Aprovado. | 00 |
| D11 | 2026-11-08 | Posição do diagrama de contexto | Vai no Apêndice B (Diagramas), junto com os demais. | Consolidado |
| D12 | 2026-11-08 | Premissa P5 (participação voluntária) | Mantida como premissa confirmada. | 00 |
| D13 | 2026-11-08 | Aprovação de 01-visao-e-escopo.md e 01-contexto.drawio | Aprovados. | 01, diagrama 01 |
| D14 | 2026-11-08 | Termos do glossário | Mantidos os 12 termos (inclui Empresa e Projeto Acadêmico). | 02, diagrama 02 |
| D15 | 2026-11-08 | Definição de Parceria | Mantida: acordo entre o departamento, docentes selecionados e empresa. | 02 |
| D16 | 2026-11-08 | Aprovação de 02-glossario.md e 02-mapa-dominio.drawio | Aprovados. | 02, diagrama 02 |
| D17 | 2026-11-08 | Quem mantém os dados cadastrais dos docentes (RF01) | O Gestor inclui e mantém os dados cadastrais dos docentes. | 03 |
| D18 | 2026-11-08 | Prioridades dos RFs | RF05 elevado para Alta; RF11, RF15, RF16 e RF17 permanecem Média. | 03 |
| D19 | 2026-11-08 | RF13 (desfecho da parceria) | Mantido como um único RF (17 RFs no total). | 03 |
| D20 | 2026-11-08 | Aprovação de 03-requisitos-funcionais.md | Aprovado, com o ajuste da D18. | 03 |
| D21 | 2026-11-08 | Fórmula do Grau de Aderência | GA = 70 × (áreas exigidas cobertas pelo docente ÷ áreas exigidas) + 30 × min(projetos anteriores relacionados, 3) ÷ 3, escala 0–100. | 05, 03 (RF08) |
| D22 | 2026-11-08 | Definição de "projeto anterior relacionado" | Projeto do portfólio do docente que compartilha ao menos 1 área de conhecimento exigida pela oportunidade. | 05, 02 |
| D23 | 2026-11-08 | Nota mínima para sugerir docente | GA ≥ 50; abaixo disso o Gestor pode registrar a compatibilidade manualmente, com justificativa. | 05 |
| D24 | 2026-11-08 | Transições do ciclo de vida | Tabela aprovada: o Gestor executa todas; Descartada a partir de qualquer estado ativo, com motivo; Parceria firmada e Descartada são estados finais. | 05, diagrama 03 |
| D25 | 2026-11-08 | Mínimos | Ao menos 1 docente validado, que deve ser o coordenador; justificativa com no mínimo 30 caracteres. | 05 |
| D26 | 2026-11-08 | Vínculo entre Projeto Acadêmico e Área de Conhecimento (RN03) | O Docente indica as áreas de conhecimento de cada projeto ao registrá-lo. | 03 (RF05), 05 (RN03), 02, diagrama 02 |
| D27 | 2026-11-08 | Autorização para alterar RF05 aprovado | Autorizado, somente para incluir as áreas de conhecimento do projeto (sem mudar prioridade nem ator). | 03 (RF05) |
| D28 | 2026-11-08 | Condição extra para Proposta em elaboração → Em negociação | O usuário escolheu exigir proposta registrada antes de negociar. Cria o conceito novo "Proposta"; definição, RF, RN e atualização de glossário/diagramas AGUARDAM respostas (pendente). | 02, 03, 05, diagramas 02 e 03 |
| D29 | 2026-11-08 | Aprovação de 05-regras-de-negocio.md e 03-fluxo-parceria.drawio | Aprovados, com D26 aplicada e D28 a incorporar; status só passa a Aprovado após aplicar D28. | 05, diagrama 03 |
| D30 | 2026-11-08 | Definição de Proposta | Documento elaborado pelo departamento, a partir de uma oportunidade, que descreve a solução a oferecer, os docentes selecionados e a empresa interessada. | 02, 03, 05 |
| D31 | 2026-11-08 | Requisito para a Proposta | Criado o RF18 "Registrar proposta", prioridade Alta, ator Gestor; 18 RFs autorizados. | 03 |
| D32 | 2026-11-08 | Regra para a Proposta | Criada a RN13 (Restrição): exige proposta registrada, vinculada aos docentes selecionados e a ao menos uma empresa com manifestação de interesse, para passar de Proposta em elaboração a Em negociação. 13 RNs autorizadas. | 05 |
| D33 | 2026-11-08 | Atualização de artefatos aprovados | Autorizado atualizar glossário (13 termos; Proposta; Projeto Acadêmico com áreas), mapa do domínio e fluxo; ajustar RN08, RN10 e RF07 só no necessário. | 02, 03, 05, diagramas 02 e 03 |
| D34 | 2026-11-08 | Aprovação consolidada de 02, 03, 05 e diagramas 02 e 03 | Aprovados, com D26 a D33 aplicadas. | 02, 03, 05, diagramas |
| D35 | 2026-11-08 | Valores de desempenho (RNF01, RNF02) | Consulta de compatíveis em até 3 s (95% das consultas); cálculo de aderência em até 10 s (95%); com 500 docentes e 200 oportunidades. | 04 |
| D36 | 2026-11-08 | Valores de privacidade, usabilidade e disponibilidade | RNF04: exclusão/anonimização em até 30 dias. RNF05: Gestor novo conclui a tarefa em até 30 min, com 80% de sucesso em teste com 5 usuários. RNF06: disponibilidade de 95% em horário comercial (seg–sex, 8h–18h). | 04 |
| D37 | 2026-11-08 | Manutenibilidade (RNF07) | Nota mínima, pesos da fórmula e teto de projetos configuráveis; histórico de mudanças de estado guardado por 5 anos. | 04 |
| D38 | 2026-11-08 | Lista de RNFs | Mantidos os 7 RNFs. | 04 |
| D39 | 2026-11-08 | Aprovação de 04-requisitos-nao-funcionais.md | Aprovado; critérios de RNF03 e RNF04 aceitos como propostos. | 04 |
| D40 | 2026-11-08 | Exportação dos diagramas para PNG | O usuário exporta manualmente pelo VS Code (Draw.io Integration) para docs/fase1/diagramas/ com os nomes 01-contexto.png, 02-mapa-dominio.png e 03-fluxo-parceria.png. Nada é instalado pelo agente. | Consolidado (Apêndice B) |
| D41 | 2026-11-08 | Ferramenta do .docx | Pandoc; o usuário instala com sudo apt install pandoc. Nada é instalado pelo agente. | Consolidado |
| D42 | 2026-11-08 | Geração do .docx | Ainda não: pandoc não instalado e PNGs não exportados. Pendente. | Consolidado |
| D43 | 2026-11-08 | Aprovação da matriz de rastreabilidade e do Fase1_Consolidado.md; Proposta na Visão | Aprovados. Autorizado acrescentar uma frase sobre a Proposta na Visão (≤ 450 palavras), sincronizada no Consolidado. | 01, 06, Consolidado |
| D44 | 2026-11-08 | Git commit | Não fazer commit agora; um único commit após a geração do .docx. | Todos |
| D45 | 2026-11-08 | Detalhe do mapa do domínio | Só os nomes dos termos, agrupados por cor (Universidade, Indústria, Prospecção e Parceria), com cardinalidade compacta (1, N, 0..1, 0..N) nas pontas das linhas. | Diagrama 02 |
| D46 | 2026-11-08 | Formato do fluxo da parceria | Raias por ator (Gestor, ProspectaUni, Docente, Empresa); condição de cada transição escrita por extenso com a RN; descarte em seta única a partir dos estados ativos. | Diagrama 03 |
| D47 | 2026-11-08 | Diagramas novos | Nenhum; só refazer os 3 existentes. | Diagramas |
| D48 | 2026-11-08 | Responsável pela revisão dos diagramas | Sessão principal (Claude), com gerador de layout e verificação automática de sobreposições; arquivos continuam editáveis no draw.io. | Diagramas 01–03 |
| D49 | 2026-11-08 | Setas sem RF no diagrama de contexto | Removidas as setas Sistema→Docente e Sistema→Empresa; cada fluxo restante (F1–F6) cita seus RFs. | Diagrama 01 |
| D50 | 2026-11-08 | Quantidade de propostas e parcerias por oportunidade | Várias: uma proposta por empresa interessada (vinculada à sua manifestação de interesse); cada proposta aceita gera uma parceria. | 02, 03, 05, diagrama 02, diagrama 03, Consolidado |
| D51 | 2026-11-08 | Estado final com várias parcerias | Parceria firmada continua estado final (não muda de estado), mas aceita registrar novas parcerias das propostas pendentes ou marcá-las como não aceitas. | 05 (RN09, RN10), diagrama 03 |
| D52 | 2026-11-09 | Imagens do .docx | PNGs gerados direto dos .drawio pelo renderizador do projeto (docs/ferramentas/render_drawio.py), sem esperar a exportação pelo draw.io. | Consolidado, diagramas |
| D53 | 2026-11-09 | Formatação do .docx | ABNT: Arial 12, margens 3/3/2/2 cm, espaçamento 1,5, justificado, recuo 1,25 cm, títulos de seção em caixa alta, número de página no canto superior direito a partir do texto. | Consolidado |
| D54 | 2026-11-09 | Orientação do Apêndice B | Diagramas em A4 paisagem; o restante do documento em retrato. | Consolidado |
| D55 | 2026-11-09 | Legibilidade dos diagramas | Diagramas reconstruídos com fonte de 16 px (≈ 7,5–7,8 pt impressos); título e "Como ler" passam para a legenda e a nota da figura; a tabela de fluxos do contexto vira o Quadro 12. | Diagramas 01–03, Consolidado |
| D56 | 2026-11-09 | Quadros e figuras ABNT | Título numerado acima ("Quadro n —", "Figura n —") e "Fonte: elaborado pelos autores (2026)." abaixo. | Consolidado |
| D57 | 2026-11-09 | Local da capa | Cruz das Almas – BA, 2026. | Consolidado (capa) |
| D58 | 2026-11-09 | Numeração de subseções | Subseções continuam sem número; só as seções principais são numeradas. | Consolidado |
| D59 | 2026-11-09 | Ferramentas e versionamento | Gerador de diagramas, renderizador, modelo de estilos e build_docx.sh versionados em docs/; commit em uma branch nova fase-1. | Repositório |
| D60 | 2026-11-09 | Sumário do documento | Índice nativo do Google Docs (Inserir → Índice, com números de página), inserido pelo usuário na página SUMÁRIO reservada; passo a passo em COMO_INSERIR_SUMARIO.md. Títulos de nível 1, capa e "SUMÁRIO" gravados em maiúsculas reais, porque o Docs ignora a caixa alta por formatação. | Consolidado, pos_docx.py |
| D61 | 2026-11-09 | Listas de quadros e de figuras | Não incluir. | Consolidado |
| D62 | 2026-11-09 | Formato do sumário | Dois níveis, o 2º recuado; nível 1 em negrito (aplicado no Docs). | Consolidado |
| D63 | 2026-11-09 | Seção "Cobertura" | Reescrita como "Natureza dos requisitos funcionais", com o novo Quadro 8 (cadastro 6, processamento e regras 7, consultas cruzadas 5); retirada a lista Q→RF, que divergia do Apêndice A; quadros renumerados de 1 a 13. | 03, Consolidado |
| D64 | 2026-11-09 | Códigos de decisão (D) no documento | Removidos da coluna Origem do Fase1_Consolidado; ficam só neste registro interno e nos arquivos de trabalho (02 a 06). | Consolidado |
| D65 | 2026-11-09 | Origem de RN08, RN09 e RN13 sem os códigos D | RN08 e RN09: "Minimundo, seção 4" (exemplo prático: selecionar docentes, elaborar proposta, iniciar negociação); RN13: "RN-MM-14, Minimundo, seção 4". | Consolidado |
| D66 | 2026-11-09 | Origem "Diretriz" | RNF04: "LGPD (Lei 13.709/2018)"; RNF06: "—". | Consolidado |
| D67 | 2026-11-09 | Explicação dos códigos | Nota abaixo de cada quadro, junto da Fonte, definindo só os códigos presentes (RF, RNF, RN, RN-MM, Q, F, LGPD); gerada por docs/ferramentas/notas_quadros.py. | Consolidado |
