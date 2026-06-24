---
title: "Casos de Uso"
---

# Casos de Uso

**Ator principal:** Usuário

## UC-01: Autenticar Usuário

| Campo | Descrição |
| --- | --- |
| **Objetivo** | Permitir que o usuário acesse o sistema |
| **Pré-condição** | Usuário não autenticado |
| **Fluxo principal** | 1. Usuário informa credenciais (usuário/senha) |
| | 2. Sistema valida as credenciais |
| | 3. Sistema concede acesso |
| | 4. Sistema registra log de autenticação bem-sucedida |
| **Fluxo de exceção** | 3a. Credenciais inválidas → Sistema nega acesso |
| | 3b. Sistema registra log de falha de autenticação |
| | 3c. Se ≥ 5 tentativas falhas em 1 minuto, sistema bloqueia temporariamente |

## UC-02: Criar Tarefa

| Campo | Descrição |
| --- | --- |
| **Objetivo** | Usuário cria uma nova tarefa |
| **Pré-condição** | Usuário autenticado |
| **Fluxo principal** | 1. Usuário acessa formulário de nova tarefa |
| | 2. Usuário preenche título, descrição e data |
| | 3. Sistema valida os campos |
| | 4. Sistema salva a tarefa |
| | 5. Sistema registra log da operação |
| **Fluxo de exceção** | 3a. Campos obrigatórios vazios → Sistema exibe erro de validação |

## UC-03: Visualizar Tarefas

| Campo | Descrição |
| --- | --- |
| **Objetivo** | Usuário visualiza a lista de tarefas |
| **Pré-condição** | Usuário autenticado |
| **Fluxo principal** | 1. Usuário acessa a página inicial |
| | 2. Sistema exibe lista de tarefas do usuário |
| | 3. Sistema registra log da consulta |

## UC-04: Editar Tarefa

| Campo | Descrição |
| --- | --- |
| **Objetivo** | Usuário modifica uma tarefa existente |
| **Pré-condição** | Usuário autenticado e tarefa existe |
| **Fluxo principal** | 1. Usuário seleciona tarefa para editar |
| | 2. Sistema exibe formulário preenchido |
| | 3. Usuário altera os campos desejados |
| | 4. Sistema valida e salva as alterações |
| | 5. Sistema registra log da operação |
| **Fluxo de exceção** | 4a. Tarefa não pertence ao usuário → Sistema nega operação |

## UC-05: Excluir Tarefa

| Campo | Descrição |
| --- | --- |
| **Objetivo** | Usuário remove uma tarefa |
| **Pré-condição** | Usuário autenticado e tarefa existe |
| **Fluxo principal** | 1. Usuário seleciona tarefa para excluir |
| | 2. Sistema solicita confirmação |
| | 3. Usuário confirma exclusão |
| | 4. Sistema remove a tarefa |
| | 5. Sistema registra log da operação |

## UC-06: Pesquisar Tarefas

| Campo | Descrição |
| --- | --- |
| **Objetivo** | Usuário busca tarefas por palavra-chave |
| **Pré-condição** | Usuário autenticado |
| **Fluxo principal** | 1. Usuário informa termo de busca |
| | 2. Sistema filtra tarefas que contêm o termo |
| | 3. Sistema exibe resultados |
| | 4. Sistema registra log da pesquisa |
