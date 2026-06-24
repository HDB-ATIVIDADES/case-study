# Etapa 4: Análise Estática de Segurança (SAST)

## Ferramentas

| Ferramenta | Finalidade | Instalação |
| --- | --- | --- |
| **Bandit** | Análise estática de segurança no código Python | `pip install bandit` |
| **pip-audit** | Varredura de vulnerabilidades em dependências | `pip install pip-audit` |

## Integração no Pipeline

Adicionado job `sast` em `.github/workflows/ci.yml`, que roda após `build` (paralelo ao `test`).

### Fluxo do job `sast`

1. **Setup**: checkout + Python 3.9 + cache pip
2. **Instala dependências + ferramentas**: `pip install -r requirements.txt bandit pip-audit`
3. **Bandit scan**: gera JSON completo com `--exit-zero` (nunca falha nesta etapa)
4. **Bandit — fail on HIGH**: script Python que verifica se há achados `issue_severity == 'HIGH'`; se sim, o pipeline falha
5. **pip-audit scan**: gera JSON com descrições, nunca falha (apenas reporta)
6. **Upload de artefatos**: `bandit-report.json` e `pip-audit-report.json` salvos mesmo em caso de falha

### Job `sast` no pipeline

```yaml
  sast:
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
      - name: Install dependencies + tools
        run: |
          pip install --no-cache-dir -r requirements.txt
          pip install bandit pip-audit
      - name: Bandit scan
        run: |
          cd todo_project
          bandit -r . -f json -o ../bandit-report.json --exit-zero
      - name: Bandit — fail on HIGH
        run: |
          python -c "
          import json
          with open('bandit-report.json') as f:
              data = json.load(f)
          high = [r for r in data.get('results', [])
                  if r['issue_severity'] == 'HIGH']
          if high:
              for r in high:
                  print(f'FAIL: {r[\"test_id\"]} {r[\"filename\"]}:{r[\"line_number\"]}')
              exit(1)
          print('No HIGH severity issues found')
          "
      - name: pip-audit scan
        run: |
          pip-audit -r requirements.txt -f json --desc | tee pip-audit-report.json
      - name: Upload Bandit report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: bandit-report
          path: bandit-report.json
      - name: Upload pip-audit report
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: pip-audit-report
          path: pip-audit-report.json
```

## Resultados

### Bandit

| Métrica | Valor |
| --- | --- |
| Total de achados | 90 |
| **HIGH** | **0** ✅ (pipeline passa) |
| MEDIUM | 1 |
| LOW | 89 |

#### Achados por tipo

| Test ID | Severidade | Descrição | Ocorrências |
| --- | --- | --- | --- |
| `B101` | LOW | `assert` usado em testes (esperado) | 81 |
| `B104` | MEDIUM | Possível senha hardcoded (SECRET_KEY) | 1 |
| `B105` | LOW | Possível senha hardcoded | 1 |
| `B106` | LOW | Possível senha hardcoded | 7 |

**Threshold**: o pipeline falha apenas em `HIGH`. Como não há nenhum, o job `sast` passa.

### pip-audit

| Métrica | Valor |
| --- | --- |
| Total de vulnerabilidades | 16 |
| Pacotes afetados | 4 |

| Pacote | Versão | Vulns | Fixação |
| --- | --- | --- | --- |
| Flask | 1.1.4 | 2 | 2.2.5+ |
| Jinja2 | 2.11.3 | 4 | 3.1.3+ |
| Werkzeug | 1.0.1 | 7 | 2.2.3+ |
| pytest | 7.4.4 | 1 | 9.0.3 |

> **Nota**: Todas as vulnerabilidades estão em versões fixadas por compatibilidade com Flask 1.1.4. A atualização desses pacotes quebraria a aplicação. O risco é aceito e documentado para o relatório final (Etapa 8).

## Como executar localmente

```bash
# Bandit
docker compose exec -w /app/todo_project app bandit -r . -f json -o /tmp/bandit-report.json

# pip-audit
docker compose exec -w /app/todo_project app pip-audit -r /app/requirements.txt -f json --desc

# Simular a validação HIGH do pipeline
docker compose exec -w /app/todo_project app sh -c 'bandit -r . -f json -o /tmp/br.json --exit-zero && python3 -c "
import json
with open(\"/tmp/br.json\") as f:
    d = json.load(f)
high = [r for r in d.get(\"results\", []) if r[\"issue_severity\"] == \"HIGH\"]
print(f\"HIGH={len(high)}\")
exit(1 if high else 0)
"'
```
