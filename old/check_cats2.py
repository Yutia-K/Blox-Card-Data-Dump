import json, sys, re, urllib.request, urllib.parse, time
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'https://blox-cards.fandom.com/api.php'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def api_get(params):
    params['format'] = 'json'
    url = BASE + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))

# Check wikitext for group info
test_cards = ['Zombie King', 'Korblox Archer', 'Police Officer', 'Basic Bee', 'Fluffle']
for name in test_cards:
    try:
        d = api_get({'action': 'query', 'titles': name, 'prop': 'categories', 'cllimit': '50'})
        pages = d['query']['pages']
        for pid, page in pages.items():
            cats = [c['title'] for c in page.get('categories', [])]
            # Look for group-like categories
            group_cats = [c for c in cats if 'Card' in c or 'Group' in c or any(g.lower() in c.lower() for g in ['zombie','korblox','police','bee','fluffle','morphic','ninja'])]
            sys.stdout.write(f"{name}:\n")
            sys.stdout.write(f"  all cats: {cats}\n")
            sys.stdout.write(f"  group cats: {group_cats}\n")
    except Exception as e:
        sys.stdout.write(f"{name}: ERROR {e}\n")
    time.sleep(0.3)

# Also search for Category:Zombie Cards etc
sys.stdout.write("\n=== Searching for group categories ===\n")
for group in ['Zombie', 'Korblox', 'Police', 'Bee', 'Morphic', 'Ninja', 'Doge']:
    try:
        r = api_get({'action': 'query', 'list': 'categorymembers', 'cmtitle': f'Category:{group} Cards', 'cmlimit': '5'})
        members = r['query']['categorymembers']
        sys.stdout.write(f"Category:{group} Cards: {len(members)} members\n")
        for m in members[:3]:
            sys.stdout.write(f"  {m['title']}\n")
    except:
        try:
            r = api_get({'action': 'query', 'list': 'categorymembers', 'cmtitle': f'Category:{group}s', 'cmlimit': '5'})
            members = r['query']['categorymembers']
            sys.stdout.write(f"Category:{group}s: {len(members)} members\n")
        except:
            sys.stdout.write(f"Category:{group} Cards: NOT FOUND\n")
    time.sleep(0.3)

sys.stdout.flush()
