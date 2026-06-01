with open('build_html.py', 'r', encoding='utf-8') as f:
    text = f.read()

# Find and show the makePattern lines
lines = text.split('\n')
for i, line in enumerate(lines):
    if 'makePattern' in line or 'const pre' in line or 'const suf' in line:
        print(f"Line {i}: {line}")
