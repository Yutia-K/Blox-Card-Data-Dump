import json, sys, re, urllib.request, urllib.parse

BASE = 'https://blox-cards.fandom.com/api.php'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def api_get(params):
    params['format'] = 'json'
    url = BASE + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))

# Search for the dash card
r = api_get({'action': 'query', 'list': 'search', 'srsearch': 'dash (Card)', 'srlimit': '10'})
for hit in r['query']['search']:
    sys.stdout.write(f"  {hit['title']}\n")

# Also try exact page with the unicode dashes
sys.stdout.write('\n')
for name in ['\u2015 \u2015 \u2015 \u2015 \u2015 \u2015 \u2015 \u2015 \u2015 \u2015 (Card)',
             '___(Card)', '\u2014 \u2014 \u2014 \u2014 \u2014 \u2014 \u2014 \u2014 \u2014 \u2014 (Card)']:
    try:
        d = api_get({'action': 'parse', 'page': name, 'prop': 'wikitext'})
        wt = d['parse']['wikitext']['*']
        sys.stdout.write(f"Found: {name}\n{wt[:500]}\n")
    except:
        sys.stdout.write(f"Not found: {name}\n")
sys.stdout.flush()
