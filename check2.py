import json
with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)

# Check uncommon
for c in cards:
    rt = c.get('rarity_text','')
    if 'uncommon' in rt.lower() and c.get('rarity') != 'Uncommon':
        print(f"UNCOMMON MISS: {c['name']} -> rarity_text='{rt}' rarity={c.get('rarity')}")
        break

# Check what rarity_text looks like for various types
print("\n--- Sample action cards ---")
for c in cards:
    if 'Action' in c.get('rarity_text','') or 'action' in c.get('name','').lower():
        print(f"  {c['name']}: rt='{c.get('rarity_text','')}'")
        if sum(1 for _ in []) > 3: break

# Check a few with unknown type
print("\n--- Cards from gear page ---")
gear_names = {"Auteurs Easel","Sharp Shark Sword","Staff of Gloomy Grip","Elixir of Dreams","Prep for Survival"}
for c in cards:
    if c['name'] in gear_names:
        print(f"  {c['name']}: rt='{c.get('rarity_text','')}' type={c.get('card_type')}")
