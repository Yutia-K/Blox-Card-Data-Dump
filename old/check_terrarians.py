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

d = api_get({'action': 'parse', 'page': 'Terrarians (Playstyle)', 'prop': 'wikitext'})
wt = d['parse']['wikitext']['*']
sys.stdout.write(wt[:3000] + '\n')
sys.stdout.flush()
