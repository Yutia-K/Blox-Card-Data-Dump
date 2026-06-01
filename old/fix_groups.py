import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# Normalize groups: merge plural variants, remove non-groups
GROUP_ALIASES = {
    'Dwarves': 'Dwarf',
    'Chairs': 'Chair',
    'Kittens': 'Kitten',
    'Ninjas': 'Ninja',
    'Survivors': 'Survivor',
    'Federation': 'The Federation',
    'Playstyle': None,  # not a group
}

for card in cards:
    old_groups = card.get('groups', [])
    if not old_groups:
        continue
    new_groups = []
    for g in old_groups:
        if g in GROUP_ALIASES:
            mapped = GROUP_ALIASES[g]
            if mapped and mapped not in new_groups:
                new_groups.append(mapped)
        elif g not in new_groups:
            new_groups.append(g)
    card['groups'] = new_groups

# Also move playstyle data to proper field
for card in cards:
    if 'playstyle' in card and not card['playstyle']:
        del card['playstyle']

# Stats
from collections import Counter
all_groups = Counter()
for c in cards:
    for g in c.get('groups', []):
        all_groups[g] += 1

with_groups = sum(1 for c in cards if c.get('groups'))
sys.stdout.write(f"Cards with groups: {with_groups}\n")
sys.stdout.write(f"Unique groups: {len(all_groups)}\n\n")

for g, count in all_groups.most_common():
    sys.stdout.write(f"  {g}: {count}\n")

# Verify the dash card doesn't have groups
dash = next((c for c in cards if '___' in c['name']), None)
if dash:
    sys.stdout.write(f"\n___ card: groups={dash.get('groups')}\n")

with open('cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)
sys.stdout.write("\nSaved.\n")
sys.stdout.flush()
