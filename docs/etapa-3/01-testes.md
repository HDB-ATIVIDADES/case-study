# Testes Automatizados

## Ferramentas

| Pacote | Versão | Finalidade |
| --- | --- | --- |
| `pytest` | 8.4.2 | Runner de testes |

## Estrutura

```bash
todo_project/tests/
├── conftest.py          # Fixtures (client, auth_client, user, user_with_tasks, app_context)
├── test_forms.py        # Testes de validação dos formulários (9 testes)
├── test_models.py       # Testes dos modelos User e Task (8 testes)
└── test_routes.py       # Testes das rotas (26 testes)
```

> Total: 43 testes

## Fixtures (`conftest.py`)

| Fixture | Descrição |
| --- | --- |
| `client` | App Flask em modo TEST, SQLite `:memory:`, CSRF desabilitado, logger INFO, tabelas criadas/removidas por teste |
| `auth_client` | Cliente autenticado (registra + loga usuário `testuser`) |
| `user` | Usuário `alice` com senha hasheada via bcrypt |
| `user_with_tasks` | Usuário `alice` com 1 task associada |
| `app_context` | Contexto da aplicação para acesso ao banco |

## Testes de modelos (`test_models.py` — 8 testes)

| Teste | Descrição |
| --- | --- |
| `test_create_user` | Criar usuário e salvar no banco |
| `test_password_hashing` | Verificar hash bcrypt (senha correta e incorreta) |
| `test_password_with_special_chars` | Senha com caracteres especiais |
| `test_create_task` | Criar task associada a um usuário |
| `test_user_tasks_relationship` | Verificar relacionamento User.tasks |
| `test_task_content_edge_cases` | Content vazio e com caracteres especiais |
| `test_task_default_date` | Verificar data padrão na criação |
| `test_user_repr` | Representação string do User |
| `test_task_repr` | Representação string da Task |

## Testes de rotas (`test_routes.py` — 26 testes)

### Autenticação (7 testes)

| Teste | Descrição |
| --- | --- |
| `test_login_page` | GET `/login` → 200 |
| `test_register_page` | GET `/register` → 200 |
| `test_register_user` | POST `/register` com dados válidos → flash "Account Created" |
| `test_login_success` | POST `/login` com credenciais corretas → flash "Login Successfull" |
| `test_login_failure` | POST `/login` com credenciais erradas → flash "Login Unsuccessful" |
| `test_logout_redirects_to_login` | GET `/logout` → redirect p/ login |
| `test_register_duplicate_username` | Registrar username duplicado → erro |

### Autorização — before_request (5 testes)

| Teste | Descrição |
| --- | --- |
| `test_all_tasks_requires_auth` | GET `/all_tasks` sem auth → redirect p/ login |
| `test_add_task_requires_auth` | POST `/add_task` sem auth → redirect p/ login |
| `test_account_requires_auth` | GET `/account` sem auth → redirect p/ login |
| `test_about_requires_auth` | GET `/` sem auth → redirect p/ login |
| `test_about_page_requires_auth` | GET `/about` sem auth → redirect p/ login |

### CRUD de tarefas (4 testes)

| Teste | Descrição |
| --- | --- |
| `test_add_task` | POST `/add_task` → flash "Task Created" |
| `test_all_tasks_shows_tasks` | GET `/all_tasks` autenticado → lista as tasks |
| `test_update_task` | POST `/update_task/<id>` com task_id dinâmico → flash "Task Updated" |
| `test_delete_task` | GET `/delete_task/<id>` com task_id dinâmico → flash "Task Deleted" |

### Isolamento entre usuários (2 testes)

| Teste | Descrição |
| --- | --- |
| `test_update_other_users_task_returns_403` | user2 tenta update task de user1 → 403 |
| `test_delete_other_users_task_returns_403` | user2 tenta delete task de user1 → 403 |

### Conta (3 testes)

| Teste | Descrição |
| --- | --- |
| `test_account_page` | GET `/account` autenticado → 200 |
| `test_change_password` | POST `/change_password` senha correta → "Password Changed" |
| `test_change_password_wrong_old` | POST `/change_password` senha errada → "Please Enter Correct Password" |

### Syslog (4 testes)

| Teste | Descrição |
| --- | --- |
| `test_login_success_logs` | caplog contém `LOGIN_SUCCESS` |
| `test_login_failure_logs` | caplog contém `LOGIN_FAILURE` |
| `test_register_success_logs` | caplog contém `REGISTER_SUCCESS` |
| `test_add_task_logs` | caplog contém `OPERATION_SUCCESS` |

Testes de log usam o fixture `caplog` do pytest para capturar chamadas ao `app.logger` sem depender do syslog real.

## Testes de formulários (`test_forms.py` — 9 testes)

| Teste | Descrição |
| --- | --- |
| `test_valid_data` | RegistrationForm com dados válidos |
| `test_username_too_short` | Username < 3 caracteres → erro |
| `test_password_mismatch` | Passwords diferentes → erro |
| `test_duplicate_username_validated` | Username existente → erro "Username Exists" (usa bcrypt real) |
| `test_valid_login_form` | LoginForm com dados válidos |
| `test_missing_password` | LoginForm sem senha → erro |
| `test_missing_username` | LoginForm sem username → erro |
| `test_valid_task` | TaskForm com descrição |
| `test_empty_task` | TaskForm vazio → erro |

## Como executar

```bash
# Dentro do container em execução
docker compose exec -w /app/todo_project app python -m pytest tests/ -v

# Instalar pytest se necessário
docker compose exec app pip install pytest

# Ou via container temporário
docker compose run --rm app sh -c \
  "pip install -q -r /app/requirements.txt pytest && cd /app/todo_project && python -m pytest tests/ -v"
```

## Resultado

```bash
43 passed, 2 warnings in 15.94s
```
