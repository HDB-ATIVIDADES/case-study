---
title: "Ameaças de Segurança e Medidas de Mitigação"
---

# Ameaças de Segurança e Medidas de Mitigação

## Matriz de Ameaças

| ID | Ameaça | Impacto | Probabilidade | Mitigação | Log |
| --- | --- | --- | --- | --- | --- |
| AM-01 | Acesso não autorizado a rotas protegidas | Alto | Média | Autenticação obrigatória em todas as rotas via decorator/ middleware | `UNAUTHORIZED_ACCESS` com IP, endpoint e timestamp |
| AM-02 | Ataque de força bruta no login | Alto | Alta | Rate limiting (max 5 tentativas/min), bloqueio temporário (30 min) | `LOGIN_FAILURE` + `RATE_LIMIT_EXCEEDED` com contagem de tentativas |
| AM-03 | Ataque de negação de serviço (DoS) | Alto | Média | Rate limiting global por IP, limitar tamanho de payload | `RATE_LIMIT_EXCEEDED` com IP e endpoint |
| AM-04 | Vazamento de dados do usuário | Alto | Média | Senhas hasheadas (bcrypt/argon2), nunca expor dados sensíveis em respostas | Não aplicável (prevenção, não detecção) |
| AM-05 | Cross-Site Scripting (XSS) | Médio | Alta | Sanitizar entradas, escapar saídas no template | `INVALID_INPUT` quando padrão suspeito for detectado |
| AM-06 | SQL Injection | Alto | Média | Usar ORM (SQLAlchemy) com queries parametrizadas | `INVALID_INPUT` para entradas com caracteres suspeitos |
| AM-07 | Escalação de privilégio horizontal | Alto | Média | Verificar propriedade do recurso antes de qualquer operação | `SECURITY_VIOLATION` ao tentar acessar recurso de outro usuário |
| AM-08 | Vazamento de informação em logs | Médio | Média | Nunca logar senhas, tokens ou dados sensíveis | Revisão periódica de logs |

## Mecanismos de Defesa

### Camada 1 — Prevenção

- Autenticação obrigatória em todas as rotas
- Hash de senhas com bcrypt
- ORM com queries parametrizadas (SQLAlchemy)
- Sanitização de entrada (HTML escaping nos templates Jinja2)

### Camada 2 — Detecção

- Syslog centralizado com eventos de segurança
- Alertas para múltiplas falhas de login consecutivas
- Monitoramento de acessos a recursos não autorizados

### Camada 3 — Resposta

- Bloqueio temporário de IP após rate limit excedido
- Registro forense de todas as violações para auditoria
- Notificação via monitoramento (Etapa 7)
