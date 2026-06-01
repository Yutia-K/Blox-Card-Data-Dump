import json, re, urllib.request, urllib.parse, sys

BASE = 'https://blox-cards.fandom.com/api.php'
HEADERS = {'User-Agent': 'Mozilla/5.0'}
params = {'action':'parse','page':'1nicopatty','format':'json','prop':'wikitext'}
url = BASE + '?' + urllib.parse.urlencode(params)
req = urllib.request.Request(url, headers=HEADERS)
with urllib.request.urlopen(req, timeout=30) as resp:
    data = json.loads(resp.read().decode('utf-8'))
wt = data['parse']['wikitext']['*']
sys.stdout.write(repr(wt[:300]) + '\n')
sys.stdout.flush()

m = re.search(r'Effect:\s*(.*?)(?=\n\|-|\n\|[\}])', wt, re.DOTALL)
if m:
    sys.stdout.write('EFFECT: ' + m.group(1).strip()[:200] + '\n')
else:
    sys.stdout.write('NO EFFECT FOUND\n')
sys.stdout.flush()

m2 = re.search(r'Health/Power:\s*(\d+)\s*/\s*(\d+)', wt)
if m2:
    sys.stdout.write(f'HP: {m2.group(1)}, Power: {m2.group(2)}\n')
sys.stdout.flush()
