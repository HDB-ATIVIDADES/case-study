---
title: "Requisitos Funcionais e Não Funcionais"
---

# Requisitos Funcionais e Não Funcionais

## Requisitos Funcionais (RF)

| ID | Descrição | Classificação |
| --- | --- | --- |
| RF-01 | Autenticar usuário (login/logout) com verificação de credenciais | Obrigatório |
| RF-02 | Impedir qualquer ação sem autenticação prévia | Obrigatório |
| RF-03 | Permitir que o usuário crie uma nova tarefa | Essencial |
| RF-04 | Permitir que o usuário edite uma tarefa existente | Essencial |
| RF-05 | Permitir que o usuário exclua uma tarefa | Essencial |
| RF-06 | Permitir que o usuário visualize a lista de tarefas | Essencial |
| RF-07 | Permitir que o usuário pesquise tarefas por palavra-chave | Desejável |
| RF-08 | Gerar logs de autenticação via syslog (sucesso/falha) | Obrigatório |
| RF-09 | Registrar eventos de violação de segurança via syslog | Obrigatório |

## Requisitos Não Funcionais (RNF)

| ID | Descrição | Categoria |
| --- | --- | --- |
| RNF-01 | Senhas devem ser armazenadas com hash | Segurança |
| RNF-02 | Comunicação deve usar HTTPS em produção | Segurança |
| RNF-03 | Implementar rate limiting para evitar brute-force em login | Segurança |
| RNF-04 | Validar e sanitizar entradas do usuário (SQL Injection) | Segurança |
| RNF-05 | Sistema deve responder em até 2 segundos sob carga normal | Desempenho |
| RNF-06 | Interface deve ser utilizável em navegadores modernos | Usabilidade |
| RNF-07 | Sistema deve estar disponível em container Docker | Portabilidade |
| RNF-08 | Logs devem ser centralizados via syslog para monitoramento | Manutenibilidade |
