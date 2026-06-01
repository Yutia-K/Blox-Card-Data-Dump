import json, sys
with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)
c = next((c for c in cards if 'isaak' in c['name'].lower()), None)
if c:
    sys.stdout.write(json.dumps(c, indent=2, ensure_ascii=False)[:600] + '\n')
else:
    partials = [c['name'] for c in cards if 'brodsky' in c['name'].lower() or 'isaak' in c['name'].lower()]
    sys.stdout.write('Not found. Partials: ' + json.dumps(partials) + '\n')
sys.stdout.flush()
