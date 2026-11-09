# Requisitos Funcionais
> Projeto: ProspectaUni · Fase 1 · Versão 2 · 2026-11-08 · Status: Aprovado

Prioridade: Alta = sem ele o processo central (oportunidade → compatibilidade → parceria) não funciona; Média = apoia o processo; Baixa = conveniência. As Regras de Negócio relacionadas (RN01…) aparecem na coluna Origem.

## Módulo Cadastros
| ID | Nome | Descrição | Prioridade | Ator | Origem |
|----|------|-----------|------------|------|--------|
| RF01 | Manter docentes | O sistema deve permitir que o Gestor inclua, altere e inative docentes do departamento, com nome, matrícula, e-mail, departamento e currículo resumido. | Alta | Gestor | RN-MM-01, RN-MM-02 |
| RF02 | Manter áreas de conhecimento | O sistema deve permitir que o Gestor inclua, altere e inative áreas de conhecimento, com nome, descrição e palavras-chave. | Alta | Gestor | RN-MM-02, RN-MM-10, D8 |
| RF03 | Manter expertises | O sistema deve permitir que o Docente associe e remova suas expertises, cada uma relacionada a uma área de conhecimento. | Alta | Docente | RN-MM-02, RN-MM-03, D8 |
| RF04 | Manter setores industriais e empresas | O sistema deve permitir que o Gestor mantenha setores industriais e empresas, vinculando cada empresa a um ou mais setores e registrando seus contatos. | Alta | Gestor | RN-MM-07, RN-MM-11, RN-MM-12, D8 |

## Módulo Portfólio
| ID | Nome | Descrição | Prioridade | Ator | Origem |
|----|------|-----------|------------|------|--------|
| RF05 | Manter portfólio acadêmico | O sistema deve permitir que o Docente registre e atualize os projetos acadêmicos de seu portfólio, informando título, descrição, período, objetivos, resultados, situação, as áreas de conhecimento do projeto e seu papel de coordenador ou orientador. | Alta | Docente | RN-MM-04, RN-MM-05, RN-MM-06, D8, D26 |

## Módulo Oportunidades
| ID | Nome | Descrição | Prioridade | Ator | Origem |
|----|------|-----------|------------|------|--------|
| RF06 | Registrar desafio/oportunidade | O sistema deve permitir que o Gestor registre um desafio/oportunidade em um setor industrial, com descrição, data de identificação, prioridade e áreas de conhecimento exigidas, iniciando no estado Identificada. | Alta | Gestor | RN-MM-08, RN-MM-09, RN-MM-10, D1, D8, RN08 |
| RF07 | Alterar estado da oportunidade | O sistema deve permitir que o Gestor altere o estado de uma oportunidade entre Identificada, Em análise, Docentes selecionados, Proposta em elaboração, Em negociação, Parceria firmada e Descartada, registrando data, autor e histórico de cada mudança, conforme as transições permitidas. | Alta | Gestor | D1, D7, RN08, RN09, RN13 |

## Módulo Compatibilidade
| ID | Nome | Descrição | Prioridade | Ator | Origem |
|----|------|-----------|------------|------|--------|
| RF08 | Calcular grau de aderência | O sistema deve calcular, para uma oportunidade selecionada pelo Gestor, o grau de aderência de cada docente, a partir das áreas de conhecimento exigidas e do portfólio acadêmico, e listar os docentes em ordem decrescente. | Alta | Gestor | RN-MM-13, RN-MM-15, D3, RN01, RN02, RN03, RN04 |
| RF09 | Validar compatibilidade | O sistema deve permitir que o Gestor valide, ajuste ou rejeite o grau de aderência sugerido de um docente para uma oportunidade, exigindo justificativa, e registre a compatibilidade. | Alta | Gestor | RN-MM-15, D3, RN04, RN05, RN06 |
| RF10 | Selecionar docentes da oportunidade | O sistema deve permitir que o Gestor selecione, entre os docentes com compatibilidade validada, os que participarão da oportunidade, indicando o coordenador, e avance a oportunidade ao estado Docentes selecionados. | Alta | Gestor | RN-MM-13, RN-MM-16, D1, RN07, RN08 |
| RF11 | Consultar projetos anteriores relacionados | O sistema deve permitir que o Gestor consulte, para uma oportunidade, os projetos acadêmicos dos portfólios que se relacionam às suas áreas de conhecimento, com o docente e o papel exercido. | Média | Gestor | RN-MM-16, Q-02, Q-07, RN03 |

## Módulo Interesse e Parceria
| ID | Nome | Descrição | Prioridade | Ator | Origem |
|----|------|-----------|------------|------|--------|
| RF12 | Registrar manifestação de interesse | O sistema deve permitir que o Representante de Empresa registre a manifestação de interesse de sua empresa em uma oportunidade de um setor em que ela atua, indicando se deseja implementar a solução. | Alta | Representante de Empresa | RN-MM-14, RN11 |
| RF13 | Registrar desfecho da parceria | O sistema deve permitir que o Gestor registre cada parceria firmada a partir de uma proposta aceita, com a empresa e os docentes envolvidos, as propostas não aceitas, ou o descarte da oportunidade com motivo. | Alta | Gestor | D1, RN-MM-14, RN09, RN10, D50 |
| RF18 | Registrar proposta | O sistema deve permitir que o Gestor registre as propostas de uma oportunidade no estado Proposta em elaboração, uma por empresa com manifestação de interesse, com resumo da solução e docentes selecionados. | Alta | Gestor | D1, D28, D30, RN13, D50 |

## Módulo Consultas
| ID | Nome | Descrição | Prioridade | Ator | Origem |
|----|------|-----------|------------|------|--------|
| RF14 | Consultar docentes e portfólios por área | O sistema deve permitir que o Gestor consulte docentes compatíveis com uma oportunidade ou área de conhecimento e veja os projetos do portfólio de cada um. | Alta | Gestor | RN-MM-16, Q-01, Q-02, RN06 |
| RF15 | Consultar setores compatíveis com as competências | O sistema deve permitir que o Gestor consulte os setores industriais cujas oportunidades são compatíveis com as expertises disponíveis no departamento. | Média | Gestor | Q-03 |
| RF16 | Consultar empresas por oportunidade | O sistema deve permitir que o Gestor consulte as empresas que atuam nos setores de uma oportunidade e as que já manifestaram interesse nela. | Média | Gestor | RN-MM-14, Q-04, Q-05 |
| RF17 | Listar oportunidades sem docentes compatíveis | O sistema deve permitir que o Gestor liste as oportunidades que ainda não possuem docentes compatíveis identificados. | Média | Gestor | Q-06, RN12 |

## Cobertura
- Cadastros simples: RF01 a RF05 e RF06 (registro da oportunidade, tratado como cadastro por prudência) = 6 de 18 (33%, limite de 40%). Transacionais: RF07 a RF18 = 12 de 18 (67%).
- Q-01: RF14 · Q-02: RF11, RF14 · Q-03: RF15 · Q-04: RF16 · Q-05: RF16 · Q-06: RF17 · Q-07: RF11.
