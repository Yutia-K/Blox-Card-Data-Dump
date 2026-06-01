import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

# Find cards that were previously terrain (from old fix_data.py results)
# Check rarity_text patterns
rt_patterns = set()
for c in cards:
    rt = c.get('rarity_text', '')
    if 'Terrain' in rt or 'terrain' in rt.lower():
        rt_patterns.add(rt)

sys.stdout.write("Rarity texts containing 'Terrain':\n")
for p in sorted(rt_patterns):
    sys.stdout.write(f"  [{p}]\n")

# Check what the listing pages tagged as Terrain
# The type_map from fix_data.py should have terrain tags
# But we overwrote them. Let me check cards that are in the old Terrain category
sys.stdout.write("\n--- Cards from Action/Terrain listing that should be terrains ---\n")
for c in cards:
    name = c['name']
    rt = c.get('rarity_text', '')
    # Check if this card was in a terrain section based on effect patterns
    effect = c.get('effect', '')
    if effect and ('terrain' in effect.lower()[:100] or 'remain' in effect.lower()[:100]):
        if c.get('card_type') != 'Terrain':
            sys.stdout.write(f"  {name}: type={c.get('card_type')} effect={effect[:80]}\n")

# Also check: how many cards have no hp/pw AND no effect?
no_data = [c for c in cards if c.get('health') is None and c.get('power') is None and not c.get('effect')]
sys.stdout.write(f"\nCards with no hp/pw/effect: {len(no_data)}\n")
for c in no_data[:5]:
    sys.stdout.write(f"  {c['name']}: rt={c.get('rarity_text','')}\n")
sys.stdout.flush()
