import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

from .phrases import YES, NO, GENERIC

LIB = {'is_arxiv', 'is_arxiv_post_2007', 'is_arxiv_pre_2007'}

def normalize(text):
    return ' '.join(text.lower().replace("n't", ' not').replace('-', ' ').split())

def matches(text, phrases):
    found = []
    for phrase in sorted(phrases, key=lambda x: (-len(x), x)):
        pattern = r'(?<!\w)' + re.escape(phrase) + r'(?!\w)'
        if re.search(pattern, text):
            found.append(phrase)
            text = re.sub(pattern, lambda m: ' ' * len(m.group()), text)
    return found, text

def claims(text):
    negative, remainder = matches(normalize(text), NO)
    positive, _ = matches(remainder, YES)
    return bool(positive), bool(negative)

def prose(text):
    output = []
    fence = None
    for line in text.splitlines():
        m = re.match(r'^ {0,3}(`{3,}|~{3,})', line)
        if fence:
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= len(fence) and not line[m.end():].strip():
                fence = None
            continue
        if m:
            fence = m.group(1)
            output.append('')
        else:
            output.append(line)
    return '\n'.join(output)

def evidence(text):
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError):
        return False
    imports = {}
    bound = set()
    definitions = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            definitions.add(node.name)
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name == 'idutils':
                    imports[alias.asname or 'idutils'] = 'idutils'
                else:
                    imports[alias.asname or alias.name.split('.')[0]] = alias.name
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            for alias in node.names:
                if alias.name != '*':
                    imports[alias.asname or alias.name] = node.module + '.' + alias.name
        elif isinstance(node, (ast.Assign, ast.AnnAssign, ast.NamedExpr)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for target in targets:
                bound.update(n.id for n in ast.walk(target) if isinstance(n, ast.Name))
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                if item.optional_vars:
                    bound.update(n.id for n in ast.walk(item.optional_vars) if isinstance(n, ast.Name))
    shadows = bound | definitions
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        f = node.func
        if isinstance(f, ast.Name) and f.id not in shadows:
            route = imports.get(f.id, '')
            name = route.rsplit('.', 1)[-1]
            if name not in definitions and (name in GENERIC or route in {'idutils.' + x for x in LIB}):
                return True
        if isinstance(f, ast.Attribute) and f.attr not in definitions:
            base = f.value
            while isinstance(base, ast.Attribute):
                base = base.value
            if isinstance(base, ast.Name) and base.id in imports and base.id in shadows:
                continue
            if f.attr in GENERIC:
                return True
            if f.attr in LIB and isinstance(f.value, ast.Name) and imports.get(f.value.id) == 'idutils' and f.value.id not in shadows:
                return True
    return False

def audit(root, ignore=()):
    root = Path(root)
    if root.is_symlink() or not root.is_dir() or not os.access(str(root), os.R_OK | os.X_OK):
        raise OSError('invalid or unreadable directory: ' + str(root))
    positive = negative = prod = test = False
    docs = []
    sources = []
    for directory, dirs, files in os.walk(str(root), followlinks=False, onerror=lambda e: (_ for _ in ()).throw(e)):
        base = Path(directory)
        dirs[:] = sorted(d for d in dirs if not (base / d).is_symlink() and not any(((base / d).relative_to(root).as_posix()).startswith(x) for x in ignore))
        for name in sorted(files):
            path = base / name
            rel = path.relative_to(root).as_posix()
            if path.is_symlink() or any(rel.startswith(x) for x in ignore):
                continue
            parts = path.relative_to(root).parts
            if name == 'README.md' and len(parts) == 1 or name.endswith('.md') and 'docs' in parts[:-1]:
                docs.append(rel)
                text = prose(path.read_text(encoding='utf-8'))
                for para in re.split(r'\n\s*\n', text):
                    a, b = claims(para)
                    positive |= a
                    negative |= b
            elif name.endswith('.py'):
                sources.append(rel)
                is_test = 'tests' in parts[:-1] or name.startswith('test_') or name.endswith('_test.py')
                if not is_test and any(x in parts[:-1] for x in ('fixtures', 'docs', 'examples')):
                    continue
                found = evidence(path.read_text(encoding='utf-8'))
                if is_test:
                    test |= found
                else:
                    prod |= found
    findings = []
    if positive and not prod:
        findings.append({'id': 'documented-arxiv-validation-claim-false', 'severity': 'MEDIUM' if test else 'HIGH', 'message': 'Evidence occurs only in tests.' if test else 'No production evidence found.'})
    if negative and prod:
        findings.append({'id': 'documented-no-arxiv-validation-claim-false', 'severity': 'HIGH', 'message': 'Production evidence contradicts the negative claim.'})
    return {'findings': findings, 'production_evidence': prod, 'test_evidence': test, 'documents': docs, 'source_files': sources}

class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(1, self.prog + ': error: ' + message + '\n')

def main(argv=None):
    parser = Parser(prog='arxiv-validation-claim-audit')
    parser.add_argument('--version', action='version', version='0.1.0')
    sub = parser.add_subparsers(dest='command', required=True, parser_class=Parser)
    command = sub.add_parser('audit')
    command.add_argument('repo', nargs='?', default='.')
    command.add_argument('--json', action='store_true')
    command.add_argument('--verbose', action='store_true')
    command.add_argument('--ignore', action='append', default=[])
    command.add_argument('--fail-on', choices=['high', 'medium'], default='high')
    args = parser.parse_args(argv)
    try:
        result = audit(args.repo, args.ignore)
    except (OSError, UnicodeError) as exc:
        print('error: ' + str(exc), file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        for finding in result['findings']:
            print(finding['severity'] + ' ' + finding['id'] + ': ' + finding['message'])
        if not result['findings']:
            print('PASS')
        if args.verbose:
            print('Documents: ' + str(len(result['documents'])) + '; Python files: ' + str(len(result['source_files'])))
    return 2 if any(f['severity'] == 'HIGH' or args.fail_on == 'medium' for f in result['findings']) else 0
