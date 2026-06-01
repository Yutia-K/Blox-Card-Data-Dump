import json, sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# Build the linking data and test it
names = {c['name']: i for i, c in enumerate(cards)}
display_names = {}
for i, c in enumerate(cards):
    dn = c.get('display_name', c['name'])
    display_names[dn] = i

# Blacklist: card names that are too common or cause issues
BLACKLIST = {
    'Has',   # verb - appears in almost every effect
    'K',     # single letter
    'Stud',  # game currency
    'Studs', # game currency
}

# Group names that are also card names - don't link in "a/an X card" context
GROUP_COLLISION = {
    'Doge', 'Toy', 'Overseer', 'Babylon', 'Zombie', 'Bee', 'Chair',
    'Police', 'Ninja', 'Stars', 'Dwarf', 'Goo', 'Nightmare',
}

def esc(s):
    """HTML escape"""
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

# Build ESC_MAP excluding blacklisted names
esc_map = {}
for i, c in enumerate(cards):
    dn = c.get('display_name', c['name'])
    if dn not in BLACKLIST:
        esc_map[esc(dn)] = i

# Sort by length descending for longest-first matching
sorted_names = sorted(esc_map.keys(), key=len, reverse=True)

# Build regex with word boundaries
# For names with spaces or special chars, use \b at start and end
def make_pattern(name):
    escaped = re.escape(name)
    # Add word boundary at start (if starts with word char)
    # Add word boundary at end (if ends with word char)
    prefix = r'\b' if re.match(r'\w', name) else ''
    suffix = r'\b' if re.match(r'.*\w$', name) else ''
    return prefix + escaped + suffix

pattern = '|'.join(make_pattern(n) for n in sorted_names)
regex = re.compile(pattern, re.IGNORECASE)

# Test the regex on some effects
test_cases = [
    ('Haste. | Defender.', '2Hex'),
    ('When this card is cast, if you have 800 or more life: You lose 750 Life. Give yourself an Overseer card, a Babylon card, a Doge card, and a Toy card.', 'Dash card'),
    ('Has Haste.', 'Has test'),
    ('Give yourself 3 Titanic Stud cards.', 'Stud test'),
    ('Attach Terminal Calculation to all allied fighters.', 'Terminal test'),
]

for text, label in test_cases:
    matches = regex.findall(text)
    sys.stdout.write(f"\n{label}: [{text[:80]}]\n")
    sys.stdout.write(f"  Matches: {matches}\n")

# Also check: which card names contain "Has" as a substring?
sys.stdout.write("\n=== Names containing 'Has' ===\n")
for n in names:
    if 'Has' in n and n != 'Has':
        sys.stdout.write(f"  [{n}]\n")

# Count how many effects would be affected by "Has" linking
has_count = sum(1 for c in cards if c.get('effect') and 'Has' in c.get('effect', ''))
sys.stdout.write(f"\nEffects containing 'Has': {has_count}\n")

# Check what the word-boundary regex does for "Haste"
haste_test = regex.findall('Haste')
sys.stdout.write(f"\n'Haste' matches: {haste_test}\n")

has_test = regex.findall('Has ')
sys.stdout.write(f"'Has ' matches: {has_test}\n")

sys.stdout.flush()
