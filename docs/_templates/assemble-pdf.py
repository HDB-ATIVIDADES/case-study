import re
import sys
import urllib.request


def fetch_ci_yml():
    url = 'https://raw.githubusercontent.com/HDB-ATIVIDADES/Task-Manager-using-Flask/main/.github/workflows/ci.yml'
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            return resp.read().decode()
    except Exception as e:
        return f'# (erro ao buscar ci.yml: {e})'


def read_todo_pending():
    items = []
    try:
        with open('todo.md') as f:
            for line in f:
                line = line.rstrip()
                if line.startswith('- [ ] '):
                    text = re.sub(r'^- \[.\] ', '', line)
                    parts = text.split(' — ', 1)
                    items.append(parts)
    except FileNotFoundError:
        pass
    return items


def gen_pending_table(items):
    rows = [
        '| Item | Impacto | Ação Recomendada |',
        '| --- | --- | --- |',
    ]
    for item in items:
        if len(item) == 2:
            rows.append(f'| {item[0]} | — | {item[1]} |')
        else:
            rows.append(f'| {item[0]} | — | Ver todo.md |')
    return '\n'.join(rows) + '\n'


def main():
    skeleton = sys.stdin.readlines()
    todo_pending = read_todo_pending()
    ci_yml = fetch_ci_yml()
    etapa_count = 0

    out = []
    for line in skeleton:
        m = re.match(r'^## Etapa (\d+)', line)
        if m:
            etapa_count += 1
            if etapa_count > 1:
                out.append('\\newpage\n')
            out.append(line)
            continue

        if re.match(r'^## Pipeline CI/CD Final', line):
            out.append('\\newpage\n')
            out.append(line)
            continue

        if '{{CI_YML}}' in line:
            out.append('```yaml\n')
            out.append(ci_yml)
            out.append('\n```\n')
            continue

        if '<!-- PENDENCIAS -->' in line:
            out.append(gen_pending_table(todo_pending))
            continue

        out.append(line)

    sys.stdout.write(''.join(out))


if __name__ == '__main__':
    main()
