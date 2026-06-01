import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# Check what happened to terrains
terrains = [c for c in cards if c.get('rarity_text','') and 'Terrain' in c.get('rarity_text','')]
sys.stdout.write(f"Cards with Terrain in rarity_text: {len(terrains)}\n")
for t in terrains[:5]:
    sys.stdout.write(f"  {t['name']}: type={t['card_type']} rt={t.get('rarity_text')}\n")

# Check a specific card
c = next((x for x in cards if 'Queen Shedare' in x['name']), None)
if c:
    sys.stdout.write(f"\nQueen Shedare II:\n")
    sys.stdout.write(f"  effect: {c.get('effect','')[:300]}\n")
    sys.stdout.write(f"  groups: {c.get('groups')}\n")

# Cards that lost Fighter status
from collections import Counter
sys.stdout.write(f"\nType dist: {dict(Counter(c.get('card_type') for c in cards))}\n")

# Check actions that have hp/pw
actions_with_stats = [c for c in cards if c.get('card_type')=='Action' and c.get('health')]
sys.stdout.write(f"\nActions with health: {len(actions_with_stats)}\n")
for a in actions_with_stats[:5]:
    sys.stdout.write(f"  {a['name']}: hp={a.get('health')} pow={a.get('power')} rt={a.get('rarity_text','')[:60]}\n")
sys.stdout.flush()
