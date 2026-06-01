import json, sys, re, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'https://blox-cards.fandom.com/api.php'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def api_get(params):
    params['format'] = 'json'
    url = BASE + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))

# Fetch it with the actual unicode name
name = '\u2017 \u2017 \u2017 \u2017 \u2017 \u2017 \u2017 \u2017 \u2017 \u2017 (Card)'
d = api_get({'action': 'parse', 'page': name, 'prop': 'wikitext'})
wt = d['parse']['wikitext']['*']
sys.stdout.write(wt[:2000] + '\n')
sys.stdout.flush()
