# Requisitos Não Funcionais
> Projeto: ProspectaUni · Fase 1 · Versão 1 · 2026-11-08 · Status: Aprovado

| ID | Categoria | Descrição | Critério de aceitação | Origem |
|----|-----------|-----------|-----------------------|--------|
| RNF01 | Desempenho | A consulta de docentes compatíveis com uma oportunidade (RF14) deve retornar o resultado rapidamente. | 95% das consultas em até 3 s, com 500 docentes e 200 oportunidades cadastrados. | RF14, D35 |
| RNF02 | Desempenho | O cálculo do grau de aderência de uma oportunidade para todos os docentes (RF08) deve ser concluído em tempo adequado ao uso interativo. | 95% dos cálculos em até 10 s, com 500 docentes e 200 oportunidades cadastrados. | RF08, RN02, D35 |
| RNF03 | Segurança | O acesso deve exigir identificação do usuário, e cada ator (Gestor, Docente, Representante de Empresa) só pode executar as funções do seu papel; por exemplo, só o Gestor altera o estado da oportunidade (RN08). | Em testes de acesso, 100% das tentativas de executar função de outro papel são bloqueadas e registradas. | D2, D8, RN08 |
| RNF04 | Privacidade/LGPD | Os dados pessoais de docentes e os contatos de empresas só devem ser visíveis a quem tem papel autorizado e devem poder ser excluídos ou anonimizados a pedido do titular. | Pedido de exclusão ou anonimização atendido em até 30 dias; em testes de acesso, 0 acessos a dados pessoais por papel não autorizado. | RN-MM-02, RN-MM-11, Diretriz (LGPD) |
| RNF05 | Usabilidade | Um Gestor sem treinamento prévio deve conseguir registrar uma oportunidade e calcular a aderência dos docentes sem ajuda externa. | Em teste com 5 usuários, ao menos 80% concluem a tarefa em até 30 minutos. | RF06, RF08 |
| RNF06 | Disponibilidade | O sistema deve estar disponível no horário de uso do departamento. | Disponibilidade mínima de 95% por mês, em horário comercial (segunda a sexta, das 8h às 18h). | Diretriz |
| RNF07 | Manutenibilidade | A nota mínima de sugestão, os pesos da fórmula do grau de aderência e o teto de projetos anteriores devem poder ser alterados sem reescrever o sistema, e o histórico de mudanças de estado das oportunidades deve ser conservado. | Cada parâmetro (RN02, RN04) é alterável por configuração, sem nova versão do sistema; histórico de mudanças de estado guardado por 5 anos. | RN02, RN04, RF07, D21, D23, D37 |
