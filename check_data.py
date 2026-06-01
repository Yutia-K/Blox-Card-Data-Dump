import json, sys
from collections import Counter

with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)

print(f'Total cards: {len(cards)}', flush=True)

fields = ['rarity_text','cost_text','cost','health','power','effect','bio','color','card_type','rarity']
for field in fields:
    count = sum(1 for c in cards if field in c and c[field])
    print(f'  {field}: {count}/{len(cards)}', flush=True)

colors = Counter(c.get('color','Unknown') for c in cards)
print(f'\nColors: {dict(colors)}', flush=True)

types = Counter(c.get('card_type','Unknown') for c in cards)
print(f'Types: {dict(types)}', flush=True)

rarities = Counter(c.get('rarity','Unknown') for c in cards)
print(f'Rarities: {dict(rarities)}', flush=True)

print(f'\nSample:', flush=True)
print(json.dumps(cards[5], indent=2, ensure_ascii=False)[:600], flush=True)
