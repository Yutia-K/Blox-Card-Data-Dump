import json
import re
import time
import urllib.request
import urllib.parse
import sys
import os

BASE = "https://blox-cards.fandom.com/api.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
PROGRESS_FILE = "cards_progress.json"

def api_get(params):
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception as e:
            if attempt < 2:
                time.sleep(1)
    return None

def parse_card_page(page_title):
    data = api_get({"action": "parse", "page": page_title, "prop": "wikitext"})
    if not data or "parse" not in data:
        return None
    wikitext = data["parse"]["wikitext"]["*"]
    card = {"name": page_title}
    
    m = re.search(r'\[\[Rarity\]\]:\s*(.+)', wikitext)
    if m:
        card["rarity_text"] = m.group(1).strip()
    
    m = re.search(r'Cost:\s*(.+)', wikitext)
    if m:
        cost_str = m.group(1).strip()
        card["cost_text"] = cost_str
        cost = {}
        cm = {'C':'Colorless','B':'Blue','R':'Red','G':'Green','Y':'Yellow','W':'White'}
        for part in cost_str.split():
            pm = re.match(r'(\d+)([A-Z])', part.strip())
            if pm:
                cost[cm.get(pm.group(2), pm.group(2))] = int(pm.group(1))
        if cost:
            card["cost"] = cost
    
    m = re.search(r'Health/Power:\s*(\d+)\s*/\s*(\d+)', wikitext)
    if m:
        card["health"] = int(m.group(1))
        card["power"] = int(m.group(2))
    
    m = re.search(r'Effect:\s*(.*?)(?=\n\|-|\n\|\})', wikitext, re.DOTALL)
    if m:
        effect = m.group(1).strip()
        effect = re.sub(r'<br\s*/?>', ' | ', effect)
        effect = re.sub(r'<[^>]+>', '', effect)
        effect = re.sub(r'\[\[[^\]]*\|([^\]]*)\]\]', r'\1', effect)
        effect = re.sub(r'\[\[([^\]]*)\]\]', r'\1', effect)
        card["effect"] = effect.strip()
    
    m = re.search(r'Bio:\s*(.*?)(?=\n\|-|\n\|\})', wikitext, re.DOTALL)
    if m:
        card["bio"] = m.group(1).strip()
    
    rarity_text = card.get("rarity_text", "")
    for color in ["Blue", "Red", "Green", "Yellow", "White", "Colourless"]:
        if color.lower() in rarity_text.lower():
            card["color"] = color
            break
    
    if "Action" in rarity_text:
        card["card_type"] = "Action"
    elif "Terrain" in rarity_text:
        card["card_type"] = "Terrain"
    elif "Gear" in rarity_text:
        card["card_type"] = "Gear"
    else:
        card["card_type"] = "Fighter"
    
    for rarity in ["Common", "Uncommon", "Rare", "Epic", "Legendary", "Token", "Legacy"]:
        if rarity.lower() in rarity_text.lower():
            card["rarity"] = rarity
            break
    
    return card

# Load card names
with open("card_names.json", "r") as f:
    all_names = json.load(f)

# Load progress if exists
done = {}
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        for c in json.load(f):
            done[c["name"]] = c

print(f"Total: {len(all_names)}, Already done: {len(done)}", flush=True)

cards = list(done.values())
to_do = [n for n in all_names if n not in done]
print(f"Remaining: {len(to_do)}", flush=True)

for i, name in enumerate(to_do):
    if i % 100 == 0:
        print(f"Progress: {i}/{len(to_do)}...", flush=True)
        # Save progress
        with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
            json.dump(cards, f, ensure_ascii=False)
    card = parse_card_page(name)
    if card:
        cards.append(card)
    time.sleep(0.1)

# Final save
with open("cards_data.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"\nDone! {len(cards)} cards saved.", flush=True)
