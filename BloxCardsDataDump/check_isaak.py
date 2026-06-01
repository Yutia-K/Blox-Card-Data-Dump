import json, sys

with open('cards_data.json','r',encoding='utf-8') as f:
    cards = json.load(f)

c = next((c for c in cards if 'isaak' in c['name'].lower()), None)
if c:
    sys.stdout.write(f"name: {c['name']}\n")
    sys.stdout.write(f"card_type: {c.get('card_type')}\n")
    sys.stdout.write(f"rarity_text: {c.get('rarity_text')}\n")
    sys.stdout.write(f"color: {c.get('color')}\n")
    sys.stdout.write(f"rarity: {c.get('rarity')}\n")
    sys.stdout.write(f"health: {c.get('health')}\n")
    sys.stdout.write(f"power: {c.get('power')}\n")
    sys.stdout.write(f"cost: {c.get('cost_text')}\n")
    sys.stdout.write(f"effect: {c.get('effect','')[:300]}\n")
else:
    # Try partial
    partials = [c for c in cards if 'brodsky' in c['name'].lower() or 'isaak' in c['name'].lower()]
    sys.stdout.write(f"Not found. Partials: {[p['name'] for p in partials]}\n")
sys.stdout.flush()
