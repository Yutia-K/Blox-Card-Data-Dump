import json, re, time, urllib.request, urllib.parse, sys

BASE = "https://blox-cards.fandom.com/api.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def api_get(params):
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except:
            time.sleep(1)
    return None

print("Building card-type map from listing pages...", flush=True)
color_pages = ["Blue_Cards", "Red_Cards", "Green_Cards", "Yellow_Cards", "Colourless_Cards",
               "Action_And_Terrain_Cards", "Gear_Cards", "Tokens"]

type_map = {}  # card_name -> card_type

for page in color_pages:
    data = api_get({"action": "parse", "page": page, "prop": "wikitext"})
    if not data or "parse" not in data:
        continue
    wt = data["parse"]["wikitext"]["*"]

    current_type = "Fighter"
    for line in wt.split('\n'):
        m = re.match(r'={2,3}\s*.*?(Fighter|Action|Terrain|Gear)s?\s*={2,3}', line, re.IGNORECASE)
        if m:
            current_type = m.group(1).capitalize()
            if current_type == "Fighters": current_type = "Fighter"
            elif current_type == "Actions": current_type = "Action"
            elif current_type == "Terrains": current_type = "Terrain"
            elif current_type == "Gears": current_type = "Gear"

        for nm in re.findall(r'\[\[File:[^\]]*\|link=([^\]|]+)', line):
            nm = nm.strip()
            if nm and not nm.startswith("Category:"):
                # Fighter always wins over Gear/Action/Terrain
                # Cards often appear in token/gear sections for their created tokens
                if nm not in type_map or current_type == "Fighter":
                    type_map[nm] = current_type

    time.sleep(0.3)

print(f"Type map: {len(type_map)} entries", flush=True)

# Load and fix card data
with open("cards_data.json", "r", encoding="utf-8") as f:
    cards = json.load(f)

def detect_rarity(rt):
    rt_lower = rt.lower()
    for r in ["Legendary", "Epic", "Uncommon", "Common", "Rare", "Token", "Legacy"]:
        if r.lower() in rt_lower:
            return r
    return None

fixed = 0
for card in cards:
    rt = card.get("rarity_text", "")
    new_rarity = detect_rarity(rt)
    if new_rarity and new_rarity != card.get("rarity"):
        card["rarity"] = new_rarity
        fixed += 1

    name = card["name"]
    if name in type_map:
        card["card_type"] = type_map[name]

print(f"Fixed {fixed} rarity values", flush=True)

from collections import Counter
types = Counter(c.get('card_type','Unknown') for c in cards)
print(f"Types: {dict(types)}", flush=True)
rarities = Counter(c.get('rarity','Unknown') for c in cards)
print(f"Rarities: {dict(rarities)}", flush=True)

# Verify specific cards
for target in ['Queen Shedare II', 'Termiteking9', 'Alpha-O & Pier - Intergalactic Rivals', 'Isaak Brodsky']:
    c = next((c for c in cards if c['name'] == target), None)
    if c:
        print(f"  {c['name']}: {c.get('card_type')}", flush=True)

with open("cards_data.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print("Saved!", flush=True)
