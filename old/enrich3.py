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

def is_gear(effect, hp, pw):
    """Check if card is a Gear (not a Fighter that creates gears)"""
    if not effect:
        return False
    # Gears: primary purpose is to attach. Effect starts with "Attach" or
    # first line is "Attach to a target fighter"
    first_line = effect.split('|')[0].strip()
    # Direct gear patterns - the card itself attaches
    if re.match(r'^(?:Fading\.\s*)?Attach to a target fighter', first_line, re.IGNORECASE):
        return True
    if re.match(r'^(?:Fading\.\s*)?Attach [\w\s]+ to a target fighter', first_line, re.IGNORECASE):
        return True
    if re.match(r'^Attach to a target', effect.strip(), re.IGNORECASE):
        return True
    # If no health/power and starts with Attach
    if hp is None and pw is None:
        if re.search(r'^Attach', effect.strip(), re.IGNORECASE):
            return True
        # "Inert" + attach pattern
        if 'Inert' in effect and 'Attach' in effect:
            return True
    return False

def get_true_type(card):
    rt = card.get('rarity_text', '')
    effect = card.get('effect', '')
    hp = card.get('health')
    pw = card.get('power')

    # Explicit in rarity_text (wiki markup)
    if '[[Action' in rt or ']] Action' in rt or rt.rstrip().endswith('Action'):
        return 'Action'
    if '[[Terrain' in rt or ']] Terrain' in rt or rt.rstrip().endswith('Terrain'):
        return 'Terrain'

    # Gear detection from effect
    if is_gear(effect, hp, pw):
        return 'Gear'

    # Has health/power → Fighter (genuine stats, not zero/zero edge case)
    if hp is not None and hp > 0:
        return 'Fighter'
    if pw is not None and pw > 0:
        return 'Fighter'

    # No stats, no gear pattern → likely Action
    if hp is None and pw is None:
        return 'Action'

    return card.get('card_type', 'Fighter')

for card in cards:
    card['display_name'] = clean_name(card['name'])
    card['card_type'] = get_true_type(card)
    card['groups'] = detect_groups(card.get('effect', ''))

from collections import Counter
types = Counter(c.get('card_type', '?') for c in cards)
sys.stdout.write(f"Types: {dict(types)}\n")

# Verify specific
for name in ['0x2991; Dying Butterfly', 'Ambition\'s Grasp', 'Animites', 'Duddedud',
             'Elixir of Dreams', 'Fuse Bomb', 'Doombringer', '___',
             'Isaak Brodsky', 'Queen Shedare II', 'Termiteking9']:
    c = next((x for x in cards if x['name'] == name or name in x.get('display_name','')), None)
    if c:
        sys.stdout.write(f"  {c.get('display_name',c['name'])}: type={c['card_type']} groups={c.get('groups',[])}\n")

# Groups summary
groups_count = sum(1 for c in cards if c.get('groups'))
sys.stdout.write(f"\nCards with groups: {groups_count}\n")

with open('cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

sys.stdout.write("Saved.\n")
sys.stdout.flush()
