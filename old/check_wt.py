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

def get_wt(page):
    d = api_get({'action': 'parse', 'page': page, 'prop': 'wikitext'})
    return d['parse']['wikitext']['*']

# Check full wikitext for group/archetype info
for name in ['Zombie King', 'Korblox Archer', 'Police Officer', 'Basic Bee', 'Fluffle', 'Eisenhower']:
    wt = get_wt(name)
    sys.stdout.write(f"\n=== {name} ===\n")
    # Look for archetype, group, faction fields
    for line in wt.split('\n'):
        line_lower = line.lower()
        if any(kw in line_lower for kw in ['archetype', 'group', 'faction', 'tribe', 'zombie', 'korblox', 'police', 'bee', 'fluffle', 'morphic']):
            sys.stdout.write(f"  {line[:150]}\n")
    # Also show the table structure
    sys.stdout.write(f"  --- raw first 500 chars ---\n")
    sys.stdout.write(f"  {wt[:500]}\n")
    time.sleep(0.3)

sys.stdout.flush()
