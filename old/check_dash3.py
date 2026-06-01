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

# Fetch the dash card
page_name = '___(Card)'
# Try URL-encoded version
try:
    d = api_get({'action': 'parse', 'page': '___(Card)', 'prop': 'wikitext'})
    wt = d['parse']['wikitext']['*']
    sys.stdout.write(f"Found ___(Card):\n{wt[:1500]}\n")
except Exception as e:
    sys.stdout.write(f"___(Card) not found: {e}\n")

# Search for it
sys.stdout.write("\nSearching...\n")
r = api_get({'action': 'query', 'list': 'search', 'srsearch': '"___" card green uncommon', 'srlimit': '5'})
for hit in r['query']['search']:
    sys.stdout.write(f"  {hit['title']}\n")

# Try searching by the actual unicode char
r2 = api_get({'action': 'query', 'list': 'search', 'srsearch': '\u2017 card', 'srlimit': '5'})
for hit in r2['query']['search']:
    sys.stdout.write(f"  {hit['title']}\n")

sys.stdout.flush()
