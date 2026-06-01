import json, re, time, urllib.request, urllib.parse, sys, os
from concurrent.futures import ThreadPoolExecutor, as_completed

BASE = "https://blox-cards.fandom.com/api.php"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
PROGRESS_FILE = "cards_progress.json"
WORKERS = 20  # concurrent requests

def api_get(params):
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except Exception:
            time.sleep(1 + attempt)
    return None

def parse_card(name):
    data = api_get({"action": "parse", "page": name, "prop": "wikitext"})
    if not data or "parse" not in data:
        return None
    wt = data["parse"]["wikitext"]["*"]
    card = {"name": name}

    m = re.search(r'\[\[Rarity\]\]:\s*(.+)', wt)
    if m: card["rarity_text"] = m.group(1).strip()

    m = re.search(r'Cost:\s*(.+)', wt)
    if m:
        cs = m.group(1).strip()
        card["cost_text"] = cs
        cost = {}
        cm = {'C':'Colorless','B':'Blue','R':'Red','G':'Green','Y':'Yellow','W':'White'}
        for p in cs.split():
            pm = re.match(r'(\d+)([A-Z])', p.strip())
            if pm: cost[cm.get(pm.group(2), pm.group(2))] = int(pm.group(1))
        if cost: card["cost"] = cost

    m = re.search(r'Health/Power:\s*(\d+)\s*/\s*(\d+)', wt)
    if m:
        card["health"] = int(m.group(1))
        card["power"] = int(m.group(2))

    m = re.search(r'Effect:\s*(.*?)(?=\n\|-|\n\|\})', wt, re.DOTALL)
    if m:
        eff = m.group(1).strip()
        eff = re.sub(r'<br\s*/?>', ' | ', eff)
        eff = re.sub(r'<[^>]+>', '', eff)
        eff = re.sub(r'\[\[[^\]]*\|([^\]]*)\]\]', r'\1', eff)
        eff = re.sub(r'\[\[([^\]]*)\]\]', r'\1', eff)
        card["effect"] = eff.strip()

    m = re.search(r'Bio:\s*(.*?)(?=\n\|-|\n\|\})', wt, re.DOTALL)
    if m: card["bio"] = m.group(1).strip()

    rt = card.get("rarity_text", "")
    for c in ["Blue","Red","Green","Yellow","White","Colourless"]:
        if c.lower() in rt.lower(): card["color"] = c; break

    if "Action" in rt: card["card_type"] = "Action"
    elif "Terrain" in rt: card["card_type"] = "Terrain"
    elif "Gear" in rt: card["card_type"] = "Gear"
    else: card["card_type"] = "Fighter"

    for r in ["Common","Uncommon","Rare","Epic","Legendary","Token","Legacy"]:
        if r.lower() in rt.lower(): card["rarity"] = r; break

    return card

# Load card names
with open("card_names.json", "r") as f:
    all_names = json.load(f)

# Load progress
done_set = set()
cards = []
if os.path.exists(PROGRESS_FILE):
    with open(PROGRESS_FILE, "r", encoding="utf-8") as f:
        cards = json.load(f)
    done_set = {c["name"] for c in cards}

to_do = [n for n in all_names if n not in done_set]
print(f"Total: {len(all_names)}, Done: {len(done_set)}, Remaining: {len(to_do)}", flush=True)

if to_do:
    completed = 0
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(parse_card, name): name for name in to_do}
        for future in as_completed(futures):
            completed += 1
            result = future.result()
            if result:
                cards.append(result)
            if completed % 200 == 0:
                print(f"  {completed}/{len(to_do)} fetched ({len(cards)} total cards)...", flush=True)
                with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
                    json.dump(cards, f, ensure_ascii=False)

# Final save
with open("cards_data.json", "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"\nDone! {len(cards)} cards saved to cards_data.json", flush=True)
