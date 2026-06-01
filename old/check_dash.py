import json, sys, re, urllib.request, urllib.parse

BASE = 'https://blox-cards.fandom.com/api.php'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_wikitext(page):
    params = {'action': 'parse', 'page': page, 'format': 'json', 'prop': 'wikitext'}
    url = BASE + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d['parse']['wikitext']['*']

# Check the dash card
wt = get_wikitext('\u2015 \u2015 \u2015 \u2015 \u2015 \u2015 \u2015 \u2015 \u2015 \u2015 (Card)')
sys.stdout.write('=== DASH CARD ===\n')
sys.stdout.write(wt[:2000] + '\n')
sys.stdout.flush()
