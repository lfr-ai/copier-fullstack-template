import re
import glob

pattern_args = re.compile(r'^\s+(Args|Returns?|Raises|Yields):\s*$')
pattern_param_no_type = re.compile(r'^\s{8,12}(\w+):\s+(?!\()')
pattern_param_with_type = re.compile(r'^\s{8,12}(\w+)\s*\(')

files_with_issues = {}
for ext in ['**/*.py', '**/*.py.jinja']:
    for filepath in glob.glob(f'template/backend/{ext}', recursive=True):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
        except Exception:
            continue
        in_args = False
        section_name = ''
        issues = []
        for i, line in enumerate(lines):
            m = pattern_args.match(line)
            if m:
                in_args = True
                section_name = m.group(1)
                continue
            if in_args:
                stripped = line.strip()
                if not stripped or (not line.startswith(' ' * 8) and stripped and not stripped.startswith('#')):
                    in_args = False
                    continue
                if pattern_param_no_type.match(line) and not pattern_param_with_type.match(line):
                    issues.append((i+1, section_name, line.rstrip()))
        if issues:
            files_with_issues[filepath] = issues

print(f'Files with docstring params missing typehints: {len(files_with_issues)}')
total = sum(len(v) for v in files_with_issues.values())
print(f'Total params missing typehints: {total}')
print()
for f, issues in sorted(files_with_issues.items()):
    short = f.replace('template/backend/', '')
    print(f'{short} ({len(issues)} issues):')
    for line_no, section, line in issues[:5]:
        print(f'  L{line_no} [{section}]: {line}')
    if len(issues) > 5:
        print(f'  ... and {len(issues)-5} more')
    print()
