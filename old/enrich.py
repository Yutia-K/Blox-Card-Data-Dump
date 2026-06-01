import json, re, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# Known groups from the wiki (extracted from group pages and effect text)
KNOWN_GROUPS = {
    'Overseer', 'Babylon', 'Doge', 'Toy', 'Morphic', 'Police', 'Korblox',
    'Stagnation', 'Shedarian', 'Ninja', 'CRP', 'Vagabond', 'Nightmare',
    'Celestial', 'Arkhive', 'Blacksite', 'Bee', 'Bargetown', 'NeFoCo',
    'Grinder', 'World of Wood', 'Dwarf', 'Stars', 'Orinthian', 'Chair',
    'Zombie', 'Dwarvern', 'Paraselene', 'Glaciem', 'Korblox', 'Enzymic',
    'Necroforensic', 'Nethercreep', 'Soul-Star', 'Federation', 'Immortal',
    'Zeitgeist', 'Acolyte', 'Case', 'Xylem', 'Foroth', 'Shedarian',
    'Havaluvian', 'Cthrite', 'Cothrite', 'Void', 'Lunar', 'Morphic',
    'Razikai', 'Nightmare', 'Necrosyndicate', 'Goo', 'Fluffle',
    'Justice', 'Apocrypha', 'Dimensionia', 'Doomspire', 'Innovative',
    'Hallow', 'Beckoned Masters', 'UGC', 'Offers',
}

# Build name set for group detection in effects
all_names = {c['name'] for c in cards}

def clean_name(name):
    """Remove wiki artifact underscores from display names"""
    # Only replace underscores that look like wiki artifacts (not intentional)
    # If the name has spaces AND underscores, underscores are probably artifacts
    if '_' in name and ' ' in name:
        return name.replace('_', ' ')
    # If name is ONLY underscores and spaces, it's intentional (like the dash card)
    return name

def detect_groups(effect, name):
    """Extract group/archetype references from effect text"""
    if not effect:
        return []
    groups = set()
    # Look for "a/an [Group] card" or "[Group] fighters" patterns
    for group in KNOWN_GROUPS:
        if re.search(r'\b' + re.escape(group) + r'\b', effect, re.IGNORECASE):
            groups.add(group)
    # Look for "Give yourself a/an [X] card" pattern
    for m in re.finditer(r'(?:Give yourself|search your deck for|add)\s+(?:an?\s+)?(\w+(?:\s+\w+)?)\s+card', effect, re.IGNORECASE):
        candidate = m.group(1).strip()
        if candidate[0].isupper() and candidate not in ('this', 'that', 'target', 'any', 'each', 'a', 'an', 'the'):
            groups.add(candidate)
    # Look for "[Group] (Group)" wiki-style references
    for m in re.finditer(r'(\w+)\s*\(Group\)', effect):
        groups.add(m.group(1))
    return sorted(groups)

def detect_type_from_effect(effect, name, current_type):
    """Use effect text to better determine card type"""
    if not effect:
        return current_type
    # Gear indicators
    gear_patterns = [
        r'Attach to a target fighter',
        r'Attach \w+ to a target fighter',
        r'attached to a fighter',
        r'gear on all fighters',
        r'Give yourself \d+ gears?',
    ]
    for pat in gear_patterns:
        if re.search(pat, effect, re.IGNORECASE):
            return 'Gear'
    return current_type

def fix_card_type_by_hp(card):
    """Cards with health/power are fighters (or tokens that are fighters)"""
    if card.get('health') is not None and card.get('power') is not None:
        if card['health'] > 0 or card['power'] > 0:
            # Has stats → it's a fighter (unless it's clearly a gear)
            effect = card.get('effect', '')
            if not re.search(r'Attach to a target fighter', effect, re.IGNORECASE):
                return 'Fighter'
    return card.get('card_type', 'Fighter')

# Enrichment pass
enriched = 0
groups_added = 0
type_fixed = 0
name_cleaned = 0

for card in cards:
    old_name = card['name']
    new_name = clean_name(old_name)
    if new_name != old_name:
        card['display_name'] = new_name
        name_cleaned += 1

    # Fix types based on health/power
    effect = card.get('effect', '')
    new_type = fix_card_type_by_hp(card)
    if new_type != card.get('card_type'):
        card['card_type'] = new_type
        type_fixed += 1

    # Extract groups
    groups = detect_groups(effect, card['name'])
    if groups:
        card['groups'] = groups
        groups_added += 1

# Stats
from collections import Counter
types = Counter(c.get('card_type', '?') for c in cards)
groups_count = sum(1 for c in cards if c.get('groups'))

sys.stdout.write(f"Enrichment complete:\n")
sys.stdout.write(f"  Names cleaned: {name_cleaned}\n")
sys.stdout.write(f"  Types fixed: {type_fixed}\n")
sys.stdout.write(f"  Cards with groups: {groups_count}\n")
sys.stdout.write(f"  Types: {dict(types)}\n")

# Verify the dash card
dash = next((c for c in cards if '___' in c['name'] or '\u2017' in c['name']), None)
if dash:
    sys.stdout.write(f"\nDash card: {dash['name']}\n")
    sys.stdout.write(f"  display_name: {dash.get('display_name')}\n")
    sys.stdout.write(f"  groups: {dash.get('groups')}\n")
    sys.stdout.write(f"  type: {dash.get('card_type')}\n")

# Sample cards with groups
sys.stdout.write(f"\n--- Sample cards with groups ---\n")
for c in cards:
    if c.get('groups') and len(c['groups']) >= 2:
        sys.stdout.write(f"  {c['name']}: groups={c['groups']}\n")
        if sum(1 for _ in []) > 5: break

# Check type fixes
sys.stdout.write(f"\n--- Cards that changed type ---\n")
for c in cards:
    rt = c.get('rarity_text', '')
    if c.get('card_type') == 'Fighter' and ('Action' in rt or 'Terrain' in rt or 'Gear' in rt):
        sys.stdout.write(f"  SUSPICIOUS: {c['name']} type=Fighter but rt={rt}\n")

with open('cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

sys.stdout.write(f"\nSaved enriched data.\n")
sys.stdout.flush()
