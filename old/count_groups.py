with open('build_html.py','r',encoding='utf-8') as f:
    text = f.read()

# Count remaining group-tag onclick without title
import re
matches = re.findall(r'group-tag" onclick', text)
print(f'group-tag onclick without title: {len(matches)}')

matches2 = re.findall(r'group-tag" title', text)
print(f'group-tag with title: {len(matches2)}')

# Find remaining ones
for i, m in enumerate(re.finditer(r'group-tag" onclick', text)):
    start = max(0, m.start()-20)
    end = min(len(text), m.end()+100)
    print(f'\nOccurrence {i+1}:')
    print(text[start:end])
