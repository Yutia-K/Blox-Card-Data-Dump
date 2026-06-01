import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

names = {c['name'] for c in cards}
dn_set = {c.get('display_name', c['name']) for c in cards}

# Check Terminal Calculation
sys.stdout.write("Terminal Calculation in names: " + str('Terminal Calculation' in names) + "\n")
sys.stdout.write("Terminal Calculation in display_names: " + str('Terminal Calculation' in dn_set) + "\n")

# List all names containing "Terminal"
for n in sorted(names):
    if 'terminal' in n.lower():
        sys.stdout.write(f"  [{n}]\n")

# List all names containing "Imperial"
for n in sorted(names):
    if 'imperial' in n.lower():
        sys.stdout.write(f"  [{n}]\n")

# Check Termiteking9 effect
c = next((x for x in cards if x['name'] == 'Termiteking9'), None)
if c:
    sys.stdout.write(f"\nTermiteking9 effect: {c.get('effect','')}\n")

# Check which blacklisted names are actually problematic
blacklist_names = {'Has','K','Stud','Studs','Doge','Toy','Overseer','Babylon','Zombie','Bee','Chair','Police','Ninja','Stars','Dwarf','Goo','Nightmare','Void','Justice','Baseplate','Hal','Ice','Rad','Cow','Oz','Mag','Bob','Rage','Pier'}

# How many effects reference a blacklisted name?
bl_ref = 0
for c in cards:
    eff = c.get('effect', '')
    for bl in blacklist_names:
        if bl.lower() in eff.lower():
            bl_ref += 1
            break
sys.stdout.write(f"\nEffects referencing blacklisted names: {bl_ref}\n")

# How many linkable names exist (4+ chars, not blacklisted)?
linkable = [n for n in dn_set if len(n) >= 4 and n not in blacklist_names]
sys.stdout.write(f"Linkable names (4+ chars, not blacklisted): {len(linkable)}\n")
sys.stdout.flush()
