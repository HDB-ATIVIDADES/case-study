import re
import sys
import glob
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


def bump_heading(line):
    return re.sub(r'^(#+)', r'\1##', line)


def main():
    skeleton = sys.stdin.readlines()
    todo_pending = read_todo_pending()
    ci_yml = fetch_ci_yml()

    etapa_dirs = {}
    for n in range(1, 8):
        etapa_dirs[n] = sorted(glob.glob(f"docs/etapa-{n}/*.md"))

    out = []
    inside_etapa = False

    for line in skeleton:
        m = re.match(r'^## Etapa (\d+)', line)
        if m:
            inside_etapa = True
            num = int(m.group(1))
            if num > 1:
                out.append('\\newpage\n')
            out.append(line)
            for fname in etapa_dirs.get(num, []):
                with open(fname) as f:
                    for fline in f:
                        out.append(bump_heading(fline))
                out.append('\n')
            continue

        if inside_etapa and line.strip() == '':
            out.append(line)
            continue

        if inside_etapa and line.startswith('## '):
            inside_etapa = False

        if '{{CI_YML}}' in line:
            ci_yml_block = '```yaml\n' + ci_yml + '\n```\n'
            out.append(ci_yml_block)
            continue

        if '<!-- PENDENCIAS -->' in line:
            out.append(gen_pending_table(todo_pending))
            continue

        out.append(line)

    sys.stdout.write(''.join(out))


if __name__ == '__main__':
    main()
