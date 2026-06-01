import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

names = {c['name'] for c in cards}
display_names = {c.get('display_name', c['name']) for c in cards}

# Check Terminal Calculation
sys.stdout.write("=== 'Terminal Calculation' ===\n")
tc = [n for n in names if 'terminal' in n.lower() or 'calculation' in n.lower()]
for n in tc:
    sys.stdout.write(f"  [{n}]\n")

# Check what names would match in Termiteking9's effect
c = next((x for x in cards if x['name'] == 'Termiteking9'), None)
if c:
    sys.stdout.write(f"\nTermiteking9 effect: {c.get('effect','')}\n")
    for n in sorted(names, key=len, reverse=True):
        if len(n) >= 4 and n not in {'Has','K','Stud','Studs'}:
            if re.search(r'\b' + re.escape(n) + r'\b', c.get('effect',''), re.IGNORECASE):
                sys.stdout.write(f"  MATCH: [{n}]\n")

# Check Imperial Indoctrination
sys.stdout.write("\n=== 'Imperial Indoctrination' ===\n")
ii = [n for n in names if 'imperial' in n.lower() or 'indoctrination' in n.lower()]
for n in ii:
    sys.stdout.write(f"  [{n}]\n")

# Check how many effects have NO links at all (might be too aggressive blacklist)
linked = 0
unlinked = 0
for c in cards:
    eff = c.get('effect', '')
    if not eff: continue
    has_link = False
    for n in sorted(display_names, key=len, reverse=True):
        if len(n) >= 4 and n not in {'Has','Stud','Studs'}:
            if re.search(r'\b' + re.escape(n) + r'\b', eff, re.IGNORECASE):
                has_link = True
                break
    if has_link: linked += 1
    else: unlinked += 1
sys.stdout.write(f"\nEffects with links: {linked}\n")
sys.stdout.write(f"Effects without links: {unlinked}\n")
sys.stdout.flush()
