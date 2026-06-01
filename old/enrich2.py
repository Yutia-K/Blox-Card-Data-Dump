import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# Verified groups from wiki (color pages + faction/group pages)
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
    'Lunar', 'Smiley', 'Vagabond', 'Dreamer', 'Nightmare Knights',
    'Brixzee', 'Redcliff', 'Overseer', 'Babylon', 'Toy', 'Doge',
    'Korblox', 'Shedarian', 'Stagnation', 'Orinthian', 'Bargetown',
    'Grinder', 'Dwarf', 'Paraselene', 'Ninja', 'Celestial',
}

# Also build a set of all card names that ARE groups (from (Group) pages)
GROUP_SUFFIXES = set()

def clean_name(name):
    if '_' in name and ' ' in name:
        return name.replace('_', ' ')
    return name

def detect_groups(effect):
    if not effect:
        return []
    groups = set()
    # Only match verified group names
    for group in VERIFIED_GROUPS:
        if re.search(r'\b' + re.escape(group) + r'\b', effect, re.IGNORECASE):
            groups.add(group)
    return sorted(groups)

def get_true_type(card):
    """Determine card type from multiple signals"""
    rt = card.get('rarity_text', '')
    effect = card.get('effect', '')
    hp = card.get('health')
    pw = card.get('power')

    # Explicit in rarity_text
    if '[[Action' in rt or 'Action]]' in rt:
        return 'Action'
    if '[[Terrain' in rt or 'Terrain]]' in rt:
        return 'Terrain'
    if '[[Gear' in rt or 'Gear]]' in rt:
        return 'Gear'

    # Effect-based gear detection
    if effect and re.search(r'Attach (?:to a target|[\w\s]+ to a target) fighter', effect, re.IGNORECASE):
        return 'Gear'

    # Has health/power → Fighter
    if hp is not None and pw is not None:
        if hp > 0 or pw > 0:
            return 'Fighter'

    return card.get('card_type', 'Fighter')

# Enrich
for card in cards:
    # Clean display name
    card['display_name'] = clean_name(card['name'])

    # Fix type
    card['card_type'] = get_true_type(card)

    # Extract groups
    card['groups'] = detect_groups(card.get('effect', ''))

# Report
from collections import Counter
types = Counter(c.get('card_type', '?') for c in cards)
groups_count = sum(1 for c in cards if c.get('groups'))

sys.stdout.write(f"Types: {dict(types)}\n")
sys.stdout.write(f"Cards with groups: {groups_count}\n")

# Verify specific cards
for target in ['Duddedud', '___', 'Dante']:
    c = next((x for x in cards if target in x['name']), None)
    if c:
        sys.stdout.write(f"  {c['name']}: type={c['card_type']} groups={c.get('groups')}\n")

# Show all unique groups found
all_groups = set()
for c in cards:
    all_groups.update(c.get('groups', []))
sys.stdout.write(f"\nAll groups found ({len(all_groups)}): {sorted(all_groups)}\n")

# Sample actions/terrains/gears
for t in ['Action', 'Terrain', 'Gear']:
    items = [c for c in cards if c.get('card_type') == t][:3]
    sys.stdout.write(f"\nSample {t}s:\n")
    for c in items:
        sys.stdout.write(f"  {c['name']}: hp={c.get('health')} pow={c.get('power')} effect={str(c.get('effect',''))[:80]}\n")

with open('cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

sys.stdout.write("\nSaved.\n")
sys.stdout.flush()
