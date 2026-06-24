# Etapa 2: Containerização e Execução

## Objetivo

Executar a aplicação Flask base em container Docker usando imagem oficial Python, sem Dockerfile, sem imagem commitada, com o mínimo de alterações no código original.

## Pré-requisitos

- Docker 29.5.3
- Repositório forkado em `/home/wagner/github/Task-Manager-using-Flask`

## Ajustes realizados

### requirements.txt — 3 mudanças do original

| Linha | Original | Final | Motivo |
| --- | --- | --- | --- |
| Flask | `==2.3.2` | `==1.1.4` | Flask 2.3.x exige Werkzeug >= 2.3.3, que removeu `safe_str_cmp` usado por Flask-Login/Bcrypt/WTF |
| MarkupSafe | *(transitivo)* | `==2.0.1` | `soft_unicode` removido no MarkupSafe 2.1+; Jinja2 2.11.3 depende dele |
| SQLAlchemy | *(transitivo)* | `<2.0` | Flask-SQLAlchemy 2.4.1 incompatível com SQLAlchemy 2.x (`__all__` removido) |

Demais pacotes mantidos **exatamente nas versões originais**.

### run.py

Adicionado `host='0.0.0.0'` para o Flask escutar em todas as interfaces dentro do container.

## docker-compose.yml

```yaml
services:
  app:
    image: python:3.9-slim
    ports:
      - "5000:5000"
    volumes:
      - .:/app
      - /dev/log:/dev/log
    working_dir: /app/todo_project
    command: >
      sh -c "pip install --no-cache-dir -r /app/requirements.txt && python run.py"
```

## Execução

```bash
cd /home/wagner/github/Task-Manager-using-Flask
docker compose up -d
```

## Validação

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:5000
# 200
```

| Endpoint | Status | Comportamento |
| --- | --- | --- |
| `GET /` | 200 | Página inicial |
| `GET /login` | 200 | Formulário de login |
| `GET /register` | 200 | Formulário de registro |
| `GET /about` | 200 | Página sobre |
| `GET /all_tasks` | 302 | Redireciona para login (não autenticado) |

## Comandos úteis

```bash
docker compose up -d       # iniciar app
docker compose logs app -f # acompanhar logs
docker compose down        # parar app
```

## Arquivos

| Arquivo | Ação |
| --- | --- |
| `requirements.txt` | 2 valores alterados + 2 pins adicionados |
| `todo_project/run.py` | Adicionado `host='0.0.0.0'` |
| `docker-compose.yml` | Criado |
