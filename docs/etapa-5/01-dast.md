# Etapa 5: Análise Dinâmica de Segurança (DAST)

## Ferramenta

| Ferramenta | Finalidade | Imagem Docker |
| --- | --- | --- |
| **OWASP ZAP** | Varredura dinâmica de vulnerabilidades em aplicações web | `ghcr.io/zaproxy/zaproxy:stable` |

## Estratégia

A aplicação é executada em container Docker e o ZAP roda em um container separado, compartilhando a mesma rede Docker Compose para comunicação.

### Fluxo

1. **Sobe a aplicação** com `docker compose up -d`
2. **Aguarda** a aplicação ficar disponível em `http://localhost:5000/login`
3. **Obtém dinamicamente** o nome da rede Docker Compose do container `app`
4. **Executa o ZAP Baseline Scan** em modo headless, conectado à mesma rede, apontando para `http://app:5000`
5. **Gera relatórios** (JSON + HTML) no diretório `/zap/wrk` do container, montado em `zap_report/` local
6. **Faz upload** dos relatórios como artefato do pipeline

> **Nota**: O ZAP exige que o diretório `/zap/wrk` esteja montado como volume quando opções de arquivo (`-J`, `-r`) são usadas. Montamos `zap_report/` local nesse diretório, definimos `--workdir /zap/wrk` e usamos nomes relativos para os relatórios.

### Arquivo de regras (`.zap/rules.tsv`)

Alertas esperados em ambiente HTTP sem HTTPS são ignorados:

| ID | Ação | Descrição |
| --- | --- | --- |
| `10011` | IGNORE | Cookie Without Secure Flag |
| `10015` | IGNORE | Incomplete or No Cache-control Header |
| `10017` | IGNORE | Cross-Domain JavaScript Source File Inclusion |
| `10049` | IGNORE | Non-Storable Content |
| `10054` | IGNORE | Cookie without SameSite Attribute |
| `10096` | IGNORE | Timestamp Disclosure |
| `90033` | IGNORE | Loosely Scoped Cookie |

### Job `dast` no pipeline

Adicionado em `.github/workflows/ci.yml`, executado após `sast`:

```yaml
dast:
    runs-on: ubuntu-latest
    timeout-minutes: 15
    needs: sast
    steps:
      - uses: actions/checkout@v4
      - name: Start app (Docker Compose)
        run: docker compose up -d
      - name: Wait for app to be ready
        run: |
          for i in $(seq 1 15); do
            if curl -s -o /dev/null http://localhost:5000/login; then
              echo "App is ready"; exit 0
            fi
            sleep 2
          done
          echo "App failed to start"; docker compose logs; exit 1
      - name: ZAP Baseline Scan
        run: |
          mkdir -p zap_report
          NETWORK=$(docker inspect "$(docker compose ps -q app)" \
            --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{"\n"}}{{end}}' | head -1)
          docker run --rm \
            --network "$NETWORK" \
            -v "$PWD/.zap/rules.tsv":/zap/rules.tsv:ro \
            -v "$PWD/zap_report":/zap/wrk \
            --workdir /zap/wrk \
            ghcr.io/zaproxy/zaproxy:stable \
            /zap/zap-baseline.py \
              -t http://app:5000 \
              -c /zap/rules.tsv \
              -J zap_report.json \
              -r zap_report.html \
              -I
      - name: Summarize ZAP findings
        if: always()
        run: |
          if [ -f zap_report/zap_report.json ]; then
            jq -r '.site[]?.alerts[]? | "  [\(.riskdesc)] \(.name) (x\(.count))"' zap_report/zap_report.json 2>/dev/null
            TOTAL=$(jq '[.site[]?.alerts[]?] | length' zap_report/zap_report.json 2>/dev/null || echo 0)
            echo "Total alerts: $TOTAL"
          fi
      - name: Upload ZAP report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: zap-report
          path: zap_report/
```

## Resultados

| Métrica | Valor |
| --- | --- |
| Alvos escaneados | 1 (`http://app:5000`) |
| Modo de varredura | Baseline (passivo + spider tradicional) |
| Duração | ~3 min |
| Total de alertas | 16 tipos |
| HIGH | 0 |
| MEDIUM | 3 |
| LOW | 7 |
| INFORMACIONAL | 6 |

### Alertas encontrados

| Risco | Alerta | ID | Ocorrências |
| --- | --- | --- | --- |
| **Médio** | Content Security Policy (CSP) Header Not Set | 10038 | 4 |
| **Médio** | Missing Anti-clickjacking Header | 10020 | 4 |
| **Médio** | Vulnerable JS Library | 10009 | 1 |
| **Baixo** | Cookie without SameSite Attribute | 10054 | 5 |
| **Baixo** | Cross-Origin-Embedder-Policy Header Missing or Invalid | 90004 | 4 |
| **Baixo** | Cross-Origin-Opener-Policy Header Missing or Invalid | 90005 | 4 |
| **Baixo** | Cross-Origin-Resource-Policy Header Missing or Invalid | 90006 | 5 |
| **Baixo** | Permissions Policy Header Not Set | 10063 | 5 |
| **Baixo** | Server Leaks Version Information via "Server" Header | 10036 | 5 |
| **Baixo** | X-Content-Type-Options Header Missing | 10021 | 5 |
| **Informativo** | Authentication Request Identified | 10111 | 1 |
| **Informativo** | Information Disclosure - Suspicious Comments | 10027 | 20 |
| **Informativo** | Non-Storable Content | 10049 | 5 |
| **Informativo** | Session Management Response Identified | 10112 | 7 |
| **Informativo** | Storable and Cacheable Content | 10094 | 5 |
| **Informativo** | User Controllable HTML Element Attribute (Potential XSS) | 10032 | 5 |

> **Observação**: Nenhum alerta de severidade HIGH foi encontrado. Os alertas MEDIUM são relacionados à falta de headers de segurança (CSP, anti-clickjacking) e biblioteca JS vulnerável (Bootstrap), enquanto a maioria dos alertas LOW/INFORMACIONAL são comportamentos esperados em ambiente HTTP de desenvolvimento sem HTTPS.

## Como executar localmente

```bash
# Sobe a aplicação
docker compose up -d

# Aguarda disponibilidade
curl -s -o /dev/null http://localhost:5000/login && echo "OK"

# Descobre a rede do Compose
NETWORK=$(docker inspect "$(docker compose ps -q app)" \
  --format '{{range $k, $v := .NetworkSettings.Networks}}{{$k}}{{"\n"}}{{end}}' | head -1)

# Cria diretório para relatórios
mkdir -p zap_report

# Executa o ZAP Baseline Scan (--workdir /zap/wrk essencial para reports)
docker run --rm \
  --network "$NETWORK" \
  -v "$PWD/.zap/rules.tsv":/zap/rules.tsv:ro \
  -v "$PWD/zap_report":/zap/wrk \
  --workdir /zap/wrk \
  ghcr.io/zaproxy/zaproxy:stable \
  /zap/zap-baseline.py \
    -t http://app:5000 \
    -c /zap/rules.tsv \
    -J zap_report.json \
    -r zap_report.html \
    -I

# Visualiza o relatório HTML
xdg-open zap_report/zap_report.html
```
