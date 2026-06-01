import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

VERIFIED_GROUPS = {
    'Overseer', 'Babylon', 'Doge', 'Toy', 'Morphic', 'Police', 'Korblox',
    'Stagnation', 'Shedarian', 'Ninja', 'CRP', 'Vagabond', 'Nightmare',
    'Celestial', 'Arkhive', 'Blacksite', 'Bee', 'Bargetown', 'NeFoCo',
    'Grinder', 'World of Wood', 'Dwarf', 'Stars', 'Orinthian', 'Chair',
    'Zombie', 'Dwarvern', 'Paraselene', 'Glaciem', 'Enzymic',
    'Necroforensic', 'Nethercreep', 'Soul-Star', 'Federation', 'Immortal',
    'Zeitgeist', 'Acolyte', 'Xylem', 'Foroth', 'Havaluvian', 'Cothrite',
    'Razikai', 'Necrosyndicate', 'Goo', 'Fluffle', 'Justice', 'Apocrypha',
    'Dimensionia', 'Doomspire', 'Innovative', 'Beckoned Masters', 'Void',
    'Lunar', 'Smiley', 'Dreamer', 'Nightmare Knights', 'Redcliff',
    'Baseplate', 'Station', 'Zombified',
}

def clean_name(name):
    if '_' in name and ' ' in name:
        return name.replace('_', ' ')
    return name

def detect_groups(effect):
    if not effect:
        return []
    groups = set()
    for group in VERIFIED_GROUPS:
        if re.search(r'\b' + re.escape(group) + r'\b', effect, re.IGNORECASE):
            groups.add(group)
    return sorted(groups)

# Enrich: display_name + groups only, DON'T touch card_type
for card in cards:
    card['display_name'] = clean_name(card['name'])
    card['groups'] = detect_groups(card.get('effect', ''))

from collections import Counter
types = Counter(c.get('card_type', '?') for c in cards)
groups_count = sum(1 for c in cards if c.get('groups'))

sys.stdout.write(f"Types: {dict(types)}\n")
sys.stdout.write(f"Cards with groups: {groups_count}\n")

# Show all unique groups
all_groups = set()
for c in cards:
    all_groups.update(c.get('groups', []))
sys.stdout.write(f"Groups ({len(all_groups)}): {sorted(all_groups)}\n")

# Verify
for name in ['Queen Shedare II', 'Termiteking9', 'Isaak Brodsky', 'Duddedud',
             'Elixir of Dreams', 'Ambition\'s Grasp', 'Collapsing Laboratory']:
    c = next((x for x in cards if x['name'] == name), None)
    if c:
        sys.stdout.write(f"  {c.get('display_name')}: type={c['card_type']} groups={c.get('groups',[])}\n")

# Count by type + groups
for t in ['Fighter', 'Action', 'Terrain', 'Gear']:
    subset = [c for c in cards if c.get('card_type') == t]
    with_groups = sum(1 for c in subset if c.get('groups'))
    sys.stdout.write(f"  {t}: {len(subset)} total, {with_groups} with groups\n")

with open('cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

sys.stdout.write("Saved.\n")
sys.stdout.flush()
