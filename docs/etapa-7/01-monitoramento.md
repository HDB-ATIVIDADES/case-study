---
title: "Monitoramento (Promtail + Loki + Grafana)"
---

# Etapa 7: Monitoramento (Promtail + Loki + Grafana)

## Stack de Monitoramento

| Componente | Função | Imagem |
| --- | --- | --- |
| **Flask FileHandler** | Escreve logs em `logs/app.log` | (código Python) |
| **Promtail** | Coleta logs do arquivo e envia ao Loki | `grafana/promtail:3.4.2` |
| **Loki** | Armazena e indexa logs | `grafana/loki:3.4.2` |
| **Grafana** | Visualização + alertas via LogQL | `grafana/grafana:11.4.0` |

## Fluxo de Dados

```{mermaid}
flowchart LR
    A["Flask App"] -->|FileHandler| B["logs/app.log"]
    B -->|Promtail tail| C["Promtail"]
    C -->|TCP 3100| D["Loki"]
    D -->|Loki datasource| E["Grafana"]
    E -->|LogQL alert| F["Alerta brute-force"]
```

## Arquivos de Configuração

### `docker-compose.yml` — Serviços adicionados

```yaml
services:
  app:
    # ... configuração existente ...
    volumes:
      - .:/app
      - /dev/log:/dev/log
      - app_logs:/app/todo_project/logs    # ← volume para logs

  loki:
    image: grafana/loki:3.4.2
    ports: ["3100:3100"]
    volumes:
      - ./config/loki/loki-config.yml:/etc/loki/loki-config.yml:ro
    command: -config.file=/etc/loki/loki-config.yml

  promtail:
    image: grafana/promtail:3.4.2
    volumes:
      - ./config/promtail/promtail-config.yml:/etc/promtail/config.yml:ro
      - app_logs:/logs:ro                  # ← mesmo volume, só leitura
    command: -config.file=/etc/promtail/config.yml

  grafana:
    image: grafana/grafana:11.4.0
    ports: ["3000:3000"]
    volumes:
      - ./config/grafana/datasources:/etc/grafana/provisioning/datasources:ro
      - ./config/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./config/grafana/alerting:/etc/grafana/provisioning/alerting:ro
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin

volumes:
  app_logs:
  loki_data:
  grafana_data:
```

### `__init__.py` — FileHandler adicionado

```python
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(log_dir, exist_ok=True)
file_handler = logging.FileHandler(os.path.join(log_dir, 'app.log'))
file_handler.setFormatter(formatter)
app.logger.addHandler(file_handler)
```

### `config/loki/loki-config.yml`

```yaml
auth_enabled: false
server:
  http_listen_port: 3100
schema_config:
  configs:
    - from: 2020-10-24
      store: boltdb-shipper
      object_store: filesystem
      schema: v11
limits_config:
  retention_period: 24h
```

### `config/promtail/promtail-config.yml`

```yaml
scrape_configs:
  - job_name: flask-app
    static_configs:
      - targets: [localhost]
        labels:
          job: flask-app
          __path__: /logs/app.log
```

### `config/grafana/datasources/datasource.yml`

```yaml
datasources:
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    isDefault: true
```

## Dashboard — 7 Painéis

| # | Painel | Tipo | Query LogQL |
| --- | --- | --- | --- |
| 1 | Timeline de Logs | Logs | `{job="flask-app"}` |
| 2 | LOGIN_FAILURE/min | Time series | `sum by(level) (count_over_time({job="flask-app"} \|= "LOGIN_FAILURE" [\$__interval]))` |
| 3 | LOGIN_SUCCESS/min | Time series | `sum by(level) (count_over_time({job="flask-app"} \|= "LOGIN_SUCCESS" [\$__interval]))` |
| 4 | Tasks Criadas (24h) | Stat | `count_over_time({job="flask-app"} \|= "OPERATION_SUCCESS" \|= "create" [\$__range])` |
| 5 | Acessos Não Autorizados (24h) | Stat | `count_over_time({job="flask-app"} \|= "UNAUTHORIZED_ACCESS" [\$__range])` |
| 6 | Eventos por Severidade (24h) | Pie chart | `sum by(level) (count_over_time({job="flask-app"} \| regexp "(INFO\|WARNING\|ERROR)" [\$__range]))` |
| 7 | Falhas de Login (1 min) | Time series + threshold | `count_over_time({job="flask-app"} \|= "LOGIN_FAILURE" [1m])` (threshold: 5) |

## Alerta de Brute-force (LogQL)

```text
count_over_time({job="flask-app"} |= "LOGIN_FAILURE" [1m]) > 5
```

- **Gatilho**: mais de 5 falhas de login no último minuto
- **Severidade**: warning
- **Mensagem**: "Possível ataque de força bruta — múltiplas falhas de login"

O alerta é provisionado automaticamente via `config/grafana/alerting/rules.yml`.

## Pipeline — Job `monitoring`

Adicionado em `.github/workflows/ci.yml`, executado após `dast-staging` no push para `staging`:

```yaml
monitoring:
  if: github.event_name == 'push' && github.ref == 'refs/heads/staging'
  runs-on: ubuntu-latest
  timeout-minutes: 15
  needs: dast-staging
  steps:
    - run: docker compose -p staging up -d
    - name: Wait for services
      run: |
        # Aguarda app (5000) + grafana (3000) + loki (3100)
    - name: Generate traffic (normal + brute-force)
      run: python scripts/generate_traffic.py http://localhost:5000
    - name: Verify logs in Loki
      run: |
        curl -s "http://localhost:3100/loki/api/v1/query_range" \
          --data-urlencode 'query={job="flask-app"}' \
          --data-urlencode 'limit=1'
    - name: Verify brute-force logs
      run: |
        curl -s "http://localhost:3100/loki/api/v1/query_range" \
          --data-urlencode 'query={job="flask-app"} |= "LOGIN_FAILURE"'
    - name: Export Grafana dashboard
      run: curl -s "http://admin:admin@localhost:3000/api/dashboards/uid/app-logs"
    - name: Upload monitoring report
      uses: actions/upload-artifact@v4
      with:
        name: monitoring-report
        path: monitoring-dashboard.json
```

## Resultados do Teste Local

### Logs gerados no arquivo

```text
2026-06-15 00:44:57,845 TaskManager[11]: INFO REGISTER_SUCCESS user=u84297
2026-06-15 00:44:58,067 TaskManager[11]: INFO LOGIN_SUCCESS user=u84297 ip=172.20.0.1
2026-06-15 00:44:58,092 TaskManager[11]: INFO OPERATION_SUCCESS user=u84297 action=create task_id=9
2026-06-15 00:44:58,108 TaskManager[11]: INFO OPERATION_SUCCESS user=u84297 action=create task_id=10
2026-06-15 00:44:58,124 TaskManager[11]: INFO OPERATION_SUCCESS user=u84297 action=create task_id=11
2026-06-15 00:44:58,348 TaskManager[11]: WARNING LOGIN_FAILURE user=alice ip=172.20.0.1
... (10 tentativas)
2026-06-15 00:45:00,524 TaskManager[11]: INFO LOGIN_SUCCESS user=u84297 ip=172.20.0.1
```

### Verificações

| Verificação | Resultado |
| --- | --- |
| Logs no arquivo `logs/app.log` | ✅ 15 entradas |
| Loki recebendo logs | ✅ 1 stream, múltiplas entradas |
| Grafana datasource Loki | ✅ Configurado automaticamente |
| Dashboard "App Logs - Task Manager" | ✅ Provisionado com 7 painéis |
| Alerta brute-force provisionado | ✅ "Possivel ataque de forca bruta" |

## Como executar localmente

```bash
# Sobe todos os serviços
docker compose up -d

# Gera tráfego normal + brute-force
python scripts/generate_traffic.py http://localhost:5000

# Acessa o Grafana
open http://localhost:3000  # admin / admin

# No Grafana: Explore → Loki → {job="flask-app"}
# Dashboard: App Logs - Task Manager
```
