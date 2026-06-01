import json, sys

with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)

targets = ['Queen Shedare II', 'Termiteking9', 'Alpha-O & Pier - Intergalactic Rivals']
for t in targets:
    found = [c for c in cards if c['name'].lower() == t.lower()]
    if found:
        c = found[0]
        sys.stdout.write(f"=== {c['name']} ===\n")
        sys.stdout.write(f"  card_type: {c.get('card_type')}\n")
        sys.stdout.write(f"  rarity_text: {c.get('rarity_text')}\n")
        sys.stdout.write(f"  color: {c.get('color')}\n")
        sys.stdout.write(f"  rarity: {c.get('rarity')}\n")
        sys.stdout.write(f"  health: {c.get('health')}\n")
        sys.stdout.write(f"  power: {c.get('power')}\n")
        sys.stdout.write(f"  cost: {c.get('cost_text')}\n")
        sys.stdout.write(f"  effect: {c.get('effect','')[:200]}\n")
    else:
        # Try partial match
        partial = [c for c in cards if t.lower() in c['name'].lower() or c['name'].lower() in t.lower()]
        sys.stdout.write(f"=== {t} === NOT FOUND EXACT\n")
        if partial:
            for p in partial[:3]:
                sys.stdout.write(f"  partial: {p['name']} type={p.get('card_type')}\n")
    sys.stdout.write("\n")
    sys.stdout.flush()
