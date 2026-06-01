import json
import re
import time
import urllib.request
import urllib.parse
import sys

BASE = "https://blox-cards.fandom.com/api.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}

def api_get(params):
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            print(f"  Retry {attempt+1} for {url[:80]}: {e}", file=sys.stderr)
            time.sleep(2 * (attempt + 1))
    return None

def get_card_names_from_page(page_title):
    data = api_get({"action": "parse", "page": page_title, "prop": "wikitext"})
    if not data or "parse" not in data:
        print(f"  Failed to fetch {page_title}", file=sys.stderr)
        return []
    wikitext = data["parse"]["wikitext"]["*"]
    names = re.findall(r'\[\[File:[^\]]*\|link=([^\]|]+)', wikitext)
    seen = set()
    unique = []
    for n in names:
        n = n.strip()
        if n and n not in seen and not n.startswith("Category:") and not n.startswith("File:"):
            seen.add(n)
            unique.append(n)
    return unique

def parse_cost(cost_str):
    cost = {}
    color_map = {
        'C': 'Colorless', 'B': 'Blue', 'R': 'Red', 'G': 'Green',
        'Y': 'Yellow', 'W': 'White'
    }
    parts = cost_str.strip().split()
    for part in parts:
        m = re.match(r'(\d+)([A-Z])', part.strip())
        if m:
            color_name = color_map.get(m.group(2), m.group(2))
            cost[color_name] = int(m.group(1))
    return cost

def parse_card_page(page_title):
    data = api_get({"action": "parse", "page": page_title, "prop": "wikitext"})
    if not data or "parse" not in data:
        return None
    wikitext = data["parse"]["wikitext"]["*"]
    
    card = {"name": page_title}
    
    # Rarity
    m = re.search(r'\[\[Rarity\]\]:\s*(.+)', wikitext)
    if m:
        card["rarity_text"] = m.group(1).strip()
    
    # Cost
    m = re.search(r'Cost:\s*(.+)', wikitext)
    if m:
        cost_str = m.group(1).strip()
        card["cost_text"] = cost_str
        card["cost"] = parse_cost(cost_str)
    
    # Health/Power
    m = re.search(r'Health/Power:\s*(\d+)\s*/\s*(\d+)', wikitext)
    if m:
        card["health"] = int(m.group(1))
        card["power"] = int(m.group(2))
    
    # Effect - use a simpler pattern
    m = re.search(r'Effect:\s*(.*?)(?=\n\|-|\n\|[\}])', wikitext, re.DOTALL)
    if m:
        effect = m.group(1).strip()
        effect = re.sub(r'<br\s*/?>', ' | ', effect)
        effect = re.sub(r'<[^>]+>', '', effect)
        effect = re.sub(r'\[\[[^\]]*\|([^\]]*)\]\]', r'\1', effect)
        effect = re.sub(r'\[\[([^\]]*)\]\]', r'\1', effect)
        card["effect"] = effect.strip()
    
    # Bio
    m = re.search(r'Bio:\s*(.*?)(?=\n\|-|\n\|[\}])', wikitext, re.DOTALL)
    if m:
        card["bio"] = m.group(1).strip()
    
    # Color
    rarity_text = card.get("rarity_text", "")
    for color in ["Blue", "Red", "Green", "Yellow", "White", "Colourless"]:
        if color.lower() in rarity_text.lower():
            card["color"] = color
            break
    
    # Card type
    if "Action" in rarity_text:
        card["card_type"] = "Action"
    elif "Terrain" in rarity_text:
        card["card_type"] = "Terrain"
    elif "Gear" in rarity_text:
        card["card_type"] = "Gear"
    else:
        card["card_type"] = "Fighter"
    
    # Rarity tier
    for rarity in ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Token", "Legacy"]:
        if rarity.lower() in rarity_text.lower():
            card["rarity"] = rarity
            break
    
    return card

print("=== Step 1: Collecting card names ===")
color_pages = ["Blue_Cards", "Red_Cards", "Green_Cards", "Yellow_Cards", "Colourless_Cards",
               "Action_And_Terrain_Cards", "Gear_Cards", "Tokens"]

all_card_names = set()
for page in color_pages:
    print(f"Fetching {page}...")
    names = get_card_names_from_page(page)
    print(f"  Found {len(names)} cards")
    all_card_names.update(names)
    time.sleep(0.5)

print(f"\nTotal unique card names: {len(all_card_names)}")

print(f"\n=== Step 2: Fetching {len(all_card_names)} card pages ===")
cards = []
failed = []
sorted_names = sorted(all_card_names)
for i, name in enumerate(sorted_names):
    if i % 100 == 0:
        print(f"Progress: {i}/{len(all_card_names)}...")
        sys.stdout.flush()
    card = parse_card_page(name)
    if card:
        cards.append(card)
    else:
        failed.append(name)
    if i % 5 == 0:
        time.sleep(0.2)

print(f"\nParsed: {len(cards)}, Failed: {len(failed)}")

with open("cards_data.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Saved to cards_data.json")
