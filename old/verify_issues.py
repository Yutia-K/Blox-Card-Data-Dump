import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

names = {c['name'] for c in cards}
display_names = {c.get('display_name', c['name']): c['name'] for c in cards}

# 1. Check if "Doge" is a card name
sys.stdout.write("=== 'Doge' as card name ===\n")
for n in names:
    if n.lower() == 'doge':
        sys.stdout.write(f"  EXACT: {n}\n")
    elif 'doge' in n.lower():
        sys.stdout.write(f"  PARTIAL: {n}\n")

# 2. Check "2Hex" effect
sys.stdout.write("\n=== 2Hex ===\n")
c = next((x for x in cards if x['name'] == '2Hex'), None)
if c:
    sys.stdout.write(f"  effect: [{c.get('effect','')}]\n")
    sys.stdout.write(f"  rarity_text: [{c.get('rarity_text','')}]\n")

# 3. Find cards with very short names that could cause false positives
sys.stdout.write("\n=== Short card names (<=3 chars) ===\n")
short = sorted([n for n in names if len(n) <= 3], key=len)
for n in short:
    sys.stdout.write(f"  [{n}]\n")

# 4. Find card names that are common English words
common_words = {'has', 'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'her', 'was', 'one', 'our', 'out', 'has', 'his', 'how', 'man', 'new', 'now', 'old', 'see', 'way', 'who', 'did', 'get', 'let', 'say', 'she', 'too', 'use', 'a', 'i'}
sys.stdout.write("\n=== Card names that are common words ===\n")
for n in names:
    if n.lower() in common_words:
        sys.stdout.write(f"  [{n}]\n")

# 5. Check what "Has" matches
sys.stdout.write("\n=== Checking 'Has' in ESC_MAP ===\n")
# Simulate what ESC_MAP would look like
for c in cards:
    en = c['name']  # In JS, esc() is called
    if en.lower() == 'has' or ' has ' in f' {en.lower()} ':
        sys.stdout.write(f"  MATCH: [{c['name']}]\n")

# 6. Check the dash card effect for group vs card linking
sys.stdout.write("\n=== Dash card effect ===\n")
dash = next((x for x in cards if '___' in x['name'] or '\u2017' in x.get('display_name','')), None)
if dash:
    sys.stdout.write(f"  name: {dash['name']}\n")
    sys.stdout.write(f"  effect: {dash.get('effect','')}\n")
    # Check which words in the effect would match card names
    effect = dash.get('effect', '')
    for word in re.findall(r'\b[A-Z]\w+\b', effect):
        if word in names:
            sys.stdout.write(f"    -> '{word}' IS a card name\n")

# 7. Find all card names that appear as substrings in other card names
sys.stdout.write("\n=== Card names that are substrings of other names (potential false matches) ===\n")
name_list = sorted(names, key=len, reverse=True)
problematic = []
for i, n in enumerate(name_list[:200]):  # check top 200 longest
    for m in name_list[i+1:]:
        if m.lower() in n.lower() and len(m) >= 3:
            problematic.append((m, n))
for short_name, long_name in problematic[:20]:
    sys.stdout.write(f"  '{short_name}' found inside '{long_name}'\n")

sys.stdout.flush()
