---
title: "Pipeline CI"
---

# Pipeline CI

## Ferramenta

**GitHub Actions** — máquina com 16 GB RAM (>8 GB), mas o repositório original está no GitHub, permitindo um fork e posso reaproveitar o Actions

## Controle de versão

### Branches

| Branch | Finalidade |
| --- | --- |
| `master` | Produção |
| `staging` | Estágio / homologação |
| `develop` | Desenvolvimento |
| `feature/*` | Trabalhos específicos (opcional) |

### Tags

Versões semânticas: `v1.0.0`, `v1.1.0`, etc.

## Pipeline

Arquivo: `.github/workflows/ci.yml`

```yaml
name: CI

on:
  push:
    branches: [master, staging, develop]
  pull_request:
    branches: [master, staging]
  workflow_dispatch:

concurrency:
  group: ${{ github.workflow }}-${{ github.ref }}
  cancel-in-progress: true

env:
  PYTHON_VERSION: '3.9'

jobs:
  build:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      - name: Install dependencies
        run: pip install --no-cache-dir -r requirements.txt
      - name: Validate application startup
        run: |
          cd todo_project
          python -c "from todo_project import app; print('Application loaded successfully')"

  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    needs: build
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      - uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
          restore-keys: |
            ${{ runner.os }}-pip-
      - name: Install dependencies
        run: pip install --no-cache-dir -r requirements.txt
      - name: Run tests
        run: |
          cd todo_project
          python -m pytest tests/ -v --junitxml=report.xml
      - name: Upload test report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-report
          path: report.xml
```

### Jobs

| Job | Depende de | Descrição | Timeout |
| --- | --- | --- | --- |
| `build` | — | Checkout + Python + cache + dependências + validação | 10 min |
| `test` | `build` | Instala deps + executa testes + upload relatório XML | 10 min |

### Estágios

| Estágio | Descrição | Comando |
| --- | --- | --- |
| Setup | Checkout + Python 3.9 | `actions/checkout` + `setup-python` |
| Cache | Cache de pacotes pip | `actions/cache@v4` por hash de `requirements.txt` |
| Dependencies | Instalar deps | `pip install -r requirements.txt` |
| Validate | Validar interpretação | `python -c "from todo_project import app"` |
| Test | Executar testes | `pytest tests/ -v --junitxml=report.xml` |
| Upload | Artefatos de relatórios | `actions/upload-artifact@v4` |

### Gatilhos

- **Push** para `master`, `staging`, `develop`
- **Pull Request** apontando para `master` ou `staging`
- **workflow_dispatch** — execução manual via interface do GitHub

### Concorrência

O campo `concurrency` cancela execuções anteriores do mesmo workflow no mesmo branch, evitando filas desnecessárias em pushes consecutivos.
