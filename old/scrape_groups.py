import json, re, time, urllib.request, urllib.parse, sys
from concurrent.futures import ThreadPoolExecutor, as_completed

sys.stdout.reconfigure(encoding='utf-8')

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

def extract_groups(page_name):
    """Fetch card page and extract Group field from wikitext"""
    data = api_get({"action": "parse", "page": page_name, "prop": "wikitext"})
    if not data or "parse" not in data:
        return (page_name, [])
    wt = data["parse"]["wikitext"]["*"]
    
    groups = []
    # Match: |[[Groups|Group]]: [[GroupName (Group)|GroupName]]
    for m in re.finditer(r'\[\[Groups?\|Group\]\]:\s*(.+)', wt):
        line = m.group(1)
        # Extract group names from wiki links
        for gm in re.finditer(r'\[\[(\w+(?:\s+\w+)*)\s*\(Group\)\|([^\]]+)\]\]', line):
            groups.append(gm.group(2).strip())
        # Also handle plain text after the field
        if not groups:
            # Try: [[GroupName (Group)|GroupName]] or just [[GroupName]]
            for gm in re.finditer(r'\[\[([^\]]+?)(?:\s*\(Group\))?\|([^\]]+)\]\]', line):
                groups.append(gm.group(2).strip())
    
    # Also check for Playstyle field (not a group but useful)
    playstyle = []
    for m in re.finditer(r'\[\[Groups#[^\]]*\|Playstyle\]\]:\s*(.+)', wt):
        line = m.group(1)
        for pm in re.finditer(r'\[\[([^\]]+?)\s*\(Playstyle\)\|([^\]]+)\]\]', line):
            playstyle.append(pm.group(2).strip())
    
    return (page_name, groups, playstyle)

# Load current data
with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

card_names = [c['name'] for c in cards]
sys.stdout.write(f"Fetching group data for {len(card_names)} cards...\n")
sys.stdout.flush()

# Fetch in parallel
results = {}
completed = 0
with ThreadPoolExecutor(max_workers=20) as pool:
    futures = {pool.submit(extract_groups, name): name for name in card_names}
    for future in as_completed(futures):
        completed += 1
        try:
            name, groups, playstyle = future.result()
            results[name] = (groups, playstyle)
        except:
            name = futures[future]
            results[name] = ([], [])
        if completed % 500 == 0:
            sys.stdout.write(f"  {completed}/{len(card_names)}...\n")
            sys.stdout.flush()

# Apply to cards
with_groups = 0
for card in cards:
    name = card['name']
    if name in results:
        groups, playstyle = results[name]
        if groups:
            card['groups'] = groups
            with_groups += 1
        else:
            card['groups'] = []
        if playstyle:
            card['playstyle'] = playstyle

# Stats
sys.stdout.write(f"\nCards with actual groups: {with_groups}\n")

# Show group distribution
from collections import Counter
all_groups = Counter()
for c in cards:
    for g in c.get('groups', []):
        all_groups[g] += 1
sys.stdout.write(f"\nGroup distribution ({len(all_groups)} groups):\n")
for g, count in all_groups.most_common():
    sys.stdout.write(f"  {g}: {count}\n")

# Verify specific cards
for name in ['Korblox Archer', 'Police Officer', 'Basic Bee', 'Fluffle', '___', 'Termiteking9']:
    c = next((x for x in cards if x['name'] == name or name in x.get('display_name', '')), None)
    if c:
        sys.stdout.write(f"  {c.get('display_name', c['name'])}: groups={c.get('groups')} playstyle={c.get('playstyle')}\n")

with open('cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

sys.stdout.write(f"\nSaved.\n")
sys.stdout.flush()
