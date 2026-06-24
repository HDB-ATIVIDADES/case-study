---
title: "Modificações de Segurança"
---

# Implementação — Modificações de Segurança (Etapa 2, parte 2)

## 1. Autenticação global via `before_request`

### `todo_project/todo_project/__init__.py`

Adicionado no final do arquivo (antes de `from todo_project import routes`):

```python
@app.before_request
def require_auth():
    from flask import request, redirect, url_for
    from flask_login import current_user
    public_routes = ['login', 'register', 'logout', 'static']
    if request.endpoint not in public_routes and not current_user.is_authenticated:
        app.logger.warning(
            f'UNAUTHORIZED_ACCESS ip={request.remote_addr} endpoint={request.endpoint}'
        )
        return redirect(url_for('login'))
```

A rota `logout` foi incluída nas públicas para permitir limpeza de sessão mesmo sem autenticação.

### `todo_project/todo_project/routes.py`

- Removido `@login_required` de todas as rotas (`all_tasks`, `add_task`, `update_task`, `delete_task`, `account`, `change_password`)
- Removido `login_required` do import
- Adicionado `abort` ao import do Flask

---

## 2. Syslog

### `todo_project/todo_project/__init__.py`

Adicionado no topo do arquivo:

```python
import logging
import logging.handlers

try:
    syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
    syslog_handler.setFormatter(logging.Formatter(
        'TaskManager[%(process)d]: %(levelname)s %(message)s'
    ))
    app.logger.addHandler(syslog_handler)
except (OSError, ConnectionError):
    app.logger.warning('Syslog not available')
```

O `try/except` garante que a aplicação não quebre se `/dev/log` não existir (ex: durante testes).

### `todo_project/todo_project/routes.py`

Logs adicionados nos seguintes eventos:

| Local | Evento | Nível | Mensagem |
| --- | --- | --- | --- |
| `login()` — sucesso (após `login_user`) | LOGIN_SUCCESS | INFO | `user={form.username.data} ip={request.remote_addr}` |
| `login()` — falha (após flash) | LOGIN_FAILURE | WARNING | `user={form.username.data} ip={request.remote_addr}` |
| `register()` — sucesso (após commit) | REGISTER_SUCCESS | INFO | `user={form.username.data}` |
| `add_task()` — sucesso (após commit) | OPERATION_SUCCESS | INFO | `user={current_user.username} action=create task_id={task.id}` |
| `update_task()` — sucesso (após commit) | OPERATION_SUCCESS | INFO | `user={current_user.username} action=update task_id={task_id}` |
| `delete_task()` — sucesso (após commit) | OPERATION_SUCCESS | INFO | `user={current_user.username} action=delete task_id={task_id}` |

---

## 3. Verificação de dono da tarefa

### `todo_project/todo_project/routes.py`

Adicionado em `update_task()` (após carregar a task) e `delete_task()` (após carregar a task):

```python
    if task.author != current_user:
        app.logger.warning(
            f'SECURITY_VIOLATION user={current_user.username} '
            f'action=unauthorized_attempt resource=task/{task_id}'
        )
        abort(403)
```

---

## Testes automatizados

As modificações são validadas por 8 novos testes (total 43):

| Classe | Teste | O que verifica |
| --- | --- | --- |
| `TestAuthorization` | `test_about_requires_auth` | GET `/` sem auth → redirect login |
| `TestAuthorization` | `test_about_page_requires_auth` | GET `/about` sem auth → redirect login |
| `TestTaskIsolation` | `test_update_other_users_task_returns_403` | user2 tenta update task de user1 → 403 |
| `TestTaskIsolation` | `test_delete_other_users_task_returns_403` | user2 tenta delete task de user1 → 403 |
| `TestSyslog` | `test_login_success_logs` | caplog contém `LOGIN_SUCCESS` |
| `TestSyslog` | `test_login_failure_logs` | caplog contém `LOGIN_FAILURE` |
| `TestSyslog` | `test_register_success_logs` | caplog contém `REGISTER_SUCCESS` |
| `TestSyslog` | `test_add_task_logs` | caplog contém `OPERATION_SUCCESS` |

## Como testar manualmente

```bash
# Reiniciar o container (código montado via volume)
docker compose restart

# Ver logs com syslog
docker compose logs app -f

# Testar acesso sem auth a /all_tasks (deve redirecionar)
curl -v http://localhost:5000/all_tasks

# Testar login inválido
curl -X POST -d "username=invalido&password=errada" http://localhost:5000/login

# Testar login válido (após registrar um usuário)
```
