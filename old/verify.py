import json, sys
from collections import Counter

with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)

# Check the 3 problem cards
targets = ['Queen Shedare II', 'Termiteking9', 'Alpha-O & Pier - Intergalactic Rivals']
for t in targets:
    c = next((c for c in cards if c['name'] == t), None)
    if c:
        sys.stdout.write(f"{c['name']}: type={c.get('card_type')} rarity={c.get('rarity')} color={c.get('color')}\n")

sys.stdout.write(f"\n--- Type distribution ---\n")
types = Counter(c.get('card_type','?') for c in cards)
for k,v in types.most_common():
    sys.stdout.write(f"  {k}: {v}\n")

# Spot check: sample some Actions to see if they make sense
sys.stdout.write(f"\n--- Sample Actions ---\n")
actions = [c for c in cards if c.get('card_type') == 'Action']
for c in actions[:10]:
    hp = c.get('health','-')
    pw = c.get('power','-')
    sys.stdout.write(f"  {c['name']}: hp={hp} pow={pw} effect={str(c.get('effect',''))[:80]}\n")

# Spot check: sample some Gears
sys.stdout.write(f"\n--- Sample Gears ---\n")
gears = [c for c in cards if c.get('card_type') == 'Gear']
for c in gears[:10]:
    hp = c.get('health','-')
    pw = c.get('power','-')
    sys.stdout.write(f"  {c['name']}: hp={hp} pow={pw} effect={str(c.get('effect',''))[:80]}\n")

# Spot check: sample Fighters
sys.stdout.write(f"\n--- Sample Fighters ---\n")
fighters = [c for c in cards if c.get('card_type') == 'Fighter']
for c in fighters[:5]:
    hp = c.get('health','-')
    pw = c.get('power','-')
    sys.stdout.write(f"  {c['name']}: hp={hp} pow={pw}\n")

sys.stdout.flush()
