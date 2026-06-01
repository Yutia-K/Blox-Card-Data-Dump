import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)

# Find cards with dashes or special chars
for c in cards:
    name = c['name']
    # Check for dash-like characters
    if any(ch in name for ch in ['\u2015', '\u2014', '\u2500', '\u2013', '___', '---']):
        sys.stdout.write(f"FOUND: [{name}]\n")
        sys.stdout.write(f"  type={c.get('card_type')} rarity={c.get('rarity')} color={c.get('color')}\n")
        sys.stdout.write(f"  effect={str(c.get('effect',''))[:200]}\n\n")

# Also find cards with unusual names (single char, symbols, etc)
sys.stdout.write("\n--- Cards with unusual names ---\n")
for c in cards:
    name = c['name']
    if len(name) <= 2 or name.startswith('_') or name.startswith('-'):
        sys.stdout.write(f"  [{name}] type={c.get('card_type')} rarity={c.get('rarity')}\n")
sys.stdout.flush()
