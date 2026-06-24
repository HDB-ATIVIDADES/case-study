# Ações Pendentes

## Segurança
- [ ] SECRET_KEY hardcoded em `todo_project/todo_project/__init__.py:11` — migrar para variável de ambiente (ex: `os.environ.get('SECRET_KEY')` com fallback)

## Dependências
- [ ] 16 vulnerabilidades conhecidas em Flask 1.1.4, Jinja2 2.11.3, Werkzeug 1.0.1 e pytest 7.4.4 — documentar como risco aceito no relatório final (Etapa 8)

## Etapas Concluídas
- [x] Etapa 1: Planejamento e requisitos
- [x] Etapa 2: Containerização (Docker Compose)
- [x] Etapa 3: Pipeline CI (build, test)
- [x] Etapa 4: SAST (Bandit + pip-audit)
- [x] Etapa 5: DAST (OWASP ZAP Baseline) — resultados reais preenchidos
- [x] Etapa 6: CD (review + staging deploy + DAST staging)
- [x] Etapa 7: Monitoramento (Promtail + Loki + Grafana)
- [x] CI: corrigido `--junitxml` (path) e ZAP `--workdir` (arquivos de report)
- [x] DAST: rodado localmente, 16 alertas (0 HIGH, 3 MEDIUM, 7 LOW, 6 INFO)
- [x] **Etapa 8: Relatório final PDF** — `docs/relatorio-final.pdf` (11 páginas, 108 KB)

## Pendências (não críticas)
- [ ] Migrar SECRET_KEY hardcoded → env var (opcional)
- [ ] Rate limit (RNF-03) não implementado — apenas alerta Grafana
- [ ] Aprovar `deploy-staging` no GitHub UI para validar pipeline completo
