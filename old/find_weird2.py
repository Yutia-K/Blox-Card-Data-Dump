import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)

# Check for various dash/line chars
target_chars = set('\u2017\u2015\u2014\u2500\u2013\u2581\u2584\u005F\u203E\u00AF')
for c in cards:
    name = c['name']
    if any(ch in target_chars for ch in name):
        sys.stdout.write(f"FOUND: [{name}] type={c.get('card_type')} rarity={c.get('rarity')}\n")

# Also just search for (Card) suffix
sys.stdout.write("\n--- Cards ending with (Card) or (something) ---\n")
for c in cards:
    if '(' in c['name'] and ')' in c['name']:
        sys.stdout.write(f"  [{c['name']}] type={c.get('card_type')} color={c.get('color')}\n")
sys.stdout.flush()
