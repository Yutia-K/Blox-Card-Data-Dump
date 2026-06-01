import json, sys, re

# Check Blue_Cards for Queen Shedare II
d = json.load(open('blue_api.json','r',encoding='utf-8'))
wt = d['parse']['wikitext']['*']

lines = wt.split('\n')
current_section = 'unknown'
for i, line in enumerate(lines):
    m = re.match(r'={2,3}\s*(.*?)\s*={2,3}', line)
    if m:
        current_section = m.group(1)
    if 'Queen Shedare' in line:
        sys.stdout.write(f'Blue Cards - Line {i}: section=[{current_section}] line={line[:150]}\n')

# Check Red_Cards for Termiteking9 and Alpha-O
d2 = json.load(open('cards_data.json','r',encoding='utf-8'))

# Let's also check what sections exist in Blue Cards
sys.stdout.write('\n--- Blue Cards sections ---\n')
for i, line in enumerate(lines):
    m = re.match(r'={2,3}\s*(.*?)\s*={2,3}', line)
    if m:
        sys.stdout.write(f'  Line {i}: {m.group(1)}\n')

sys.stdout.flush()
