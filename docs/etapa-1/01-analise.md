---
title: "Análise de Requisitos"
---

# Análise de Requisitos

## Requisitos Obrigatórios

| ID | Requisito | Descrição |
| --- | --- | --- |
| RQ-01 | Autenticação obrigatória | O sistema deve exigir autenticação antes de qualquer ação |
| RQ-02 | Log via syslog | A aplicação deve gerar logs de atividades via syslog |
| RQ-03 | Log de autenticação | Registrar sucesso ou falha nas tentativas de autenticação |

## Requisitos Funcionais

| ID | Requisito | Descrição |
| --- | --- | --- |
| RQ-04 | Criar tarefa | Usuário autenticado pode criar uma nova tarefa |
| RQ-05 | Editar tarefa | Usuário autenticado pode editar uma tarefa existente |
| RQ-06 | Excluir tarefa | Usuário autenticado pode excluir uma tarefa |
| RQ-07 | Visualizar tarefas | Usuário autenticado pode listar/visualizar suas tarefas |
| RQ-08 | Pesquisar tarefas | Usuário autenticado pode pesquisar tarefas por palavra-chave |

## Requisitos de Segurança

| ID | Requisito | Descrição |
| --- | --- | --- |
| RQ-09 | Proteção de dados | Dados dos usuários (senhas, informações pessoais) devem ser protegidos |
| RQ-10 | Mitigação DoS | O sistema deve implementar mecanismos contra negação de serviço |
| RQ-11 | Log de violações | Definir e registrar eventos considerados violação de segurança |
