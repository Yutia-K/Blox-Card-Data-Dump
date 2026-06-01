import json
with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)
# Cards with & or < > in names
special = [c['name'] for c in cards if '&' in c['name'] or '<' in c['name'] or '>' in c['name'] or '"' in c['name']]
print(f"Cards with special chars: {len(special)}")
for s in special[:20]:
    print(f"  {s}")
