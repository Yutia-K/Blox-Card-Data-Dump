import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

names = {c['name'] for c in cards}
dn_map = {c.get('display_name', c['name']): c for c in cards}

# Check terrarian card names from the wiki page
terrarians = [
    'Crossroads', 'Bargetown Backrooms', 'Zenith Cube', 'Lunar Impact (Card)',
    'Mac Iris', 'Polluted Vitality Wellspring', "Alpha Brick's Presence",
    "Host Farm of Svakarataja", 'Empty Office', "Eisenhower's Laboratory",
    'Scorched Earth', 'Foroth', 'Rocket Arena', 'Lumber Tycoon',
    'Ultimate Build', 'Catalog Heaven', 'Disaster Survival', "Mo's Dungeon"
]

sys.stdout.write("=== Checking terrarian cards ===\n")
for t in terrarians:
    in_names = t in names
    in_dn = t in dn_map
    sys.stdout.write(f"  {t}: in_names={in_names} in_display={in_dn}\n")
    if in_dn:
        c = dn_map[t]
        sys.stdout.write(f"    type={c.get('card_type')} rarity={c.get('rarity')} token={c.get('rarity')=='Token'}\n")

# Also check: how many Token-type cards do we have?
tokens = [c for c in cards if c.get('rarity') == 'Token']
sys.stdout.write(f"\nTotal Token cards: {len(tokens)}\n")

# Check if any tokens are terrarians
sys.stdout.write(f"\n=== Token cards that might be terrarians ===\n")
for c in tokens:
    eff = c.get('effect', '')
    if 'terrain' in eff.lower()[:100] or 'animate' in eff.lower()[:100]:
        sys.stdout.write(f"  {c.get('display_name', c['name'])}: effect={eff[:80]}\n")

sys.stdout.flush()
