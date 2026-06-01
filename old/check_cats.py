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

# Check categories for known group members
test_cards = ['Zombie King', 'Korblox Archer', 'Police Officer', 'Basic Bee', 'Fluffle']
for name in test_cards:
    try:
        d = api_get({'action': 'query', 'titles': name, 'prop': 'categories', 'cllimit': '50'})
        pages = d['query']['pages']
        for pid, page in pages.items():
            cats = [c['title'] for c in page.get('categories', [])]
            sys.stdout.write(f"{name}: {cats}\n")
    except Exception as e:
        sys.stdout.write(f"{name}: ERROR {e}\n")
    time.sleep(0.3)

sys.stdout.flush()
