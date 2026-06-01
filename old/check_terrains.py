import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

terrains = [c for c in cards if c.get('card_type') == 'Terrain']
sys.stdout.write(f"Terrain cards: {len(terrains)}\n")
for t in terrains:
    sys.stdout.write(f"  {t.get('display_name', t['name'])}: color={t.get('color')} rarity={t.get('rarity')} groups={t.get('groups',[])}\n")
sys.stdout.flush()
