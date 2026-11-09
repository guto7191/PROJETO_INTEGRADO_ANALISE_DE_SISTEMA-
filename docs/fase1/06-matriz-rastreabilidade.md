# Matriz de Rastreabilidade
> Projeto: ProspectaUni · Fase 1 · Versão 1 · 2026-11-08 · Status: Aprovado

## Regras do minimundo (RN-MM) × requisitos
| Origem | Descrição resumida | RFs | RNs |
|--------|--------------------|-----|-----|
| RN-MM-01 | Departamento com vários docentes | RF01 | — |
| RN-MM-02 | Docente com dados cadastrais e expertises por área | RF01, RF02, RF03 | — |
| RN-MM-03 | Expertise compartilhada entre docentes (N:N) | RF03 | — |
| RN-MM-04 | Portfólio com projetos coordenados ou orientados | RF05 | RN03 |
| RN-MM-05 | Dados do projeto acadêmico | RF05 | — |
| RN-MM-06 | Um coordenador e um ou mais orientadores por projeto | RF05 | RN07 |
| RN-MM-07 | Setores industriais com descrição e atuação | RF04 | — |
| RN-MM-08 | Setor com vários desafios e oportunidades | RF06 | — |
| RN-MM-09 | Dados do desafio/oportunidade | RF06 | — |
| RN-MM-10 | Oportunidade exige várias áreas de conhecimento | RF02, RF06 | RN01 |
| RN-MM-11 | Empresas vinculadas a setores, com contatos | RF04, RF12 | RN11 |
| RN-MM-12 | Empresa em vários setores; setor com várias empresas | RF04 | RN11 |
| RN-MM-13 | Compatibilidade N:N entre oportunidades e docentes | RF08, RF09, RF10 | RN01, RN04, RN07, RN12 |
| RN-MM-14 | Interesse e implementação de projetos pelas empresas | RF12, RF13, RF16, RF18 | RN10, RN11, RN13 |
| RN-MM-15 | Registro de compatibilidade com justificativa e grau de aderência | RF08, RF09 | RN02, RN04, RN05, RN06 |
| RN-MM-16 | Consulta de portfólios para apoiar a seleção | RF10, RF11, RF14 | RN03 |

## Perguntas do minimundo (Q) × requisitos
| Origem | Pergunta | RFs | RNs |
|--------|----------|-----|-----|
| Q-01 | Docentes com conhecimentos compatíveis com um desafio | RF08, RF14 | RN01, RN02 |
| Q-02 | Projetos anteriores no portfólio desses docentes | RF11, RF14 | RN03 |
| Q-03 | Setores com oportunidades compatíveis com as competências | RF15 | RN04 |
| Q-04 | Empresas dos setores de uma oportunidade | RF16 | RN11 |
| Q-05 | Empresas que já demonstraram interesse | RF12, RF16 | RN11 |
| Q-06 | Oportunidades sem docentes compatíveis | RF17 | RN12 |
| Q-07 | Docentes com experiência em projetos semelhantes | RF11 | RN03 |

## RFs × RNFs de apoio
RF08: RNF02 · RF14: RNF01 · todos: RNF03, RNF04, RNF06 · RF06 e RF08: RNF05 · RF07, RN02, RN04: RNF07.

## Lacunas
Nenhuma linha vazia: toda RN-MM e toda Q está atendida por ao menos um RF. As RN-MM sem RN associada (01, 02, 03, 05, 07, 08, 09) são cadastrais e atendidas por RFs.
