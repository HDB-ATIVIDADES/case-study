# AGENTS.md

This is an academic case study (SDLC / DevOps / DevSecOps) in **Portuguese**. The repo is a starting point — most work happens externally.

## Repo structure

- `README.md` — Case study instructions (8 stages). This is the primary spec.
- `opencode.json` — Configures `gitbook-chat` MCP server at `http://localhost:8000/sse`. Use `gitbook-chat_get_welcome` and `gitbook-chat_query_gitbook` to query case study documentation.

## App code

The base application is a **Flask task manager** cloned from an external repo:

```bash
git clone https://github.com/AdityaBagad/Task-Manager-using-Flask.git
cd Task-Manager-using-Flask
pip3 install -r requirements.txt
python run.py
```

All development, Dockerization, and pipeline work targets this cloned repo, not this repo.

## Pipeline (Stage 3+)

- If machine has ≤8GB RAM, use **GitHub Actions** instead of GitLab CI.
- Pipeline stages expected: build/interpret → tests → SAST (Bandit) → dependency checks (Safety/pip-audit) → DAST (OWASP ZAP) → CD (review/deploy) → monitoring (Prometheus+Grafana / Wazuh / ELK).
- Delivery artifact: PDF report with pipeline YAML inlined, **not** the `.yml` file separately.

## Key requirements

- Auth required before any action; app must log via syslog (auth success/failure).
- SAST: Bandit. Dependency check: Safety or pip-audit.
- DAST: OWASP ZAP (Docker image, headless baseline scan for CI).
- Monitoring: Prometheus+Grafana, Wazuh, or ELK Stack for log analysis and anomaly alerts.
