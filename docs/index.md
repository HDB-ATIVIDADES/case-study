# Estudo de Caso: DevSecOps

![Logo Hackers do Bem](assets/logo-hb.svg)

Aplicação de conceitos DevOps e DevSecOps em um sistema de gerenciamento de tarefas Flask.

## Documentos

| Documento | Descrição |
| --- | --- |
| [Relatório Final (PDF)](relatorio-final.pdf) | Relatório consolidado do estudo de caso |
| {doc}`Enunciado do Caso <CASO>` | Descrição das etapas do estudo de caso |
| [Todo / Pendências](https://github.com/HDB-ATIVIDADES/case-study/blob/main/todo.md) | Ações pendentes e próximos passos |

## Etapas

| Etapa | Descrição | Documentação |
| --- | --- | --- |
| 1 | Planejamento e Requisitos | {doc}`ver <etapa-1/01-analise>` |
| 2 | Containerização e Segurança | {doc}`ver <etapa-2/01-container-execucao>` |
| 3 | Testes e Pipeline CI | {doc}`ver <etapa-3/01-testes>` |
| 4 | Análise Estática (SAST) | {doc}`ver <etapa-4/01-sast>` |
| 5 | Análise Dinâmica (DAST) | {doc}`ver <etapa-5/01-dast>` |
| 6 | Entrega Contínua (CD) | {doc}`ver <etapa-6/01-cd>` |
| 7 | Monitoramento | {doc}`ver <etapa-7/01-monitoramento>` |

## Repositório do Projeto

[github.com/HDB-ATIVIDADES/Task-Manager-using-Flask](https://github.com/HDB-ATIVIDADES/Task-Manager-using-Flask)

Pipeline CI/CD: GitHub Actions com 8 jobs (build, test, sast, dast, deploy-review, deploy-staging, dast-staging, monitoring).

```{toctree}
:caption: Documentos
:maxdepth: 1
:hidden:

CASO
Relatório Final <relatorio-final>
```

```{toctree}
:caption: Etapa 1 — Planejamento
:maxdepth: 1
:hidden:

etapa-1/01-analise
etapa-1/02-requisitos
etapa-1/03-casos-de-uso
etapa-1/04-fluxos-de-sistema
etapa-1/05-ameacas
```

```{toctree}
:caption: Etapa 2 — Containerização
:maxdepth: 1
:hidden:

etapa-2/01-container-execucao
etapa-2/02-modificacoes-seguranca
```

```{toctree}
:caption: Etapa 3 — Testes e Pipeline CI
:maxdepth: 1
:hidden:

etapa-3/01-testes
etapa-3/02-pipeline
```

```{toctree}
:caption: Etapa 4 — SAST
:maxdepth: 1
:hidden:

etapa-4/01-sast
```

```{toctree}
:caption: Etapa 5 — DAST
:maxdepth: 1
:hidden:

etapa-5/01-dast
```

```{toctree}
:caption: Etapa 6 — CD
:maxdepth: 1
:hidden:

etapa-6/01-cd
```

```{toctree}
:caption: Etapa 7 — Monitoramento
:maxdepth: 1
:hidden:

etapa-7/01-monitoramento
```
