# Estudo de Caso: DevSecOps

Repositórios:

- **Código:** [github.com/HDB-ATIVIDADES/Task-Manager-using-Flask](https://github.com/HDB-ATIVIDADES/Task-Manager-using-Flask)
- **Documentação:** [github.com/HDB-ATIVIDADES/case-study](https://github.com/HDB-ATIVIDADES/case-study)

## Etapa 1: Planejamento e Requisitos

## Etapa 2: Containerização e Modificações de Segurança

## Etapa 3: Testes e Pipeline CI

## Etapa 4: Análise Estática de Segurança (SAST)

## Etapa 5: Análise Dinâmica de Segurança (DAST)

## Etapa 6: Entrega Contínua (CD)

## Etapa 7: Monitoramento (Promtail + Loki + Grafana)

## Pipeline CI/CD Final

Arquivo `.github/workflows/ci.yml` — 8 jobs: build, test, sast, dast, deploy-review, deploy-staging, dast-staging, monitoring.

{{CI_YML}}

## Considerações Finais

### Riscos Aceitos

16 vulnerabilidades de dependências foram **aceitas como risco** devido à incompatibilidade do Flask 1.1.4 com versões corrigidas dos pacotes. A atualização quebraria a aplicação. Recomenda-se um refactor para Flask 2.x+ em versão futura.

### Pendências Técnicas

<!-- PENDENCIAS -->

### Ferramentas Utilizadas (visão geral)

| Categoria | Ferramentas |
| --- | --- |
| Containerização | Docker, Docker Compose |
| Testes | pytest |
| SAST | Bandit, pip-audit |
| DAST | OWASP ZAP |
| CI/CD | GitHub Actions |
| Monitoramento | Promtail, Loki, Grafana |
| Controle de versão | Git, GitFlow |
