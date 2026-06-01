import json, sys, re, urllib.request, urllib.parse, time
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.stdout.reconfigure(encoding='utf-8')

BASE = 'https://blox-cards.fandom.com/api.php'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def api_get(params):
    params['format'] = 'json'
    url = BASE + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode('utf-8'))

# Fetch Terrarians page and extract card names
d = api_get({'action': 'parse', 'page': 'Terrarians (Playstyle)', 'prop': 'wikitext'})
wt = d['parse']['wikitext']['*']

# Extract card names from link= parameters
terrarian_names = set()
for m in re.finditer(r'\[\[File:[^\]]*\|link=([^\]|]+)', wt):
    name = m.group(1).strip()
    if name and not name.startswith('Category:'):
        terrarian_names.add(name)

sys.stdout.write(f"Terrarian card names from wiki: {len(terrarian_names)}\n")
for n in sorted(terrarian_names):
    sys.stdout.write(f"  {n}\n")

# Load cards and add Terrarian group
with open('cards_data.json', 'r', encoding='utf-8') as f:
    cards = json.load(f)

dn_map = {}
for c in cards:
    dn = c.get('display_name', c['name'])
    dn_map[dn] = c
    dn_map[c['name']] = c

added = 0
for tn in terrarian_names:
    c = dn_map.get(tn)
    if c:
        groups = c.get('groups', [])
        if 'Terrarian' not in groups:
            groups.append('Terrarian')
            c['groups'] = groups
            added += 1
    else:
        sys.stdout.write(f"  NOT FOUND: {tn}\n")

sys.stdout.write(f"\nAdded Terrarian group to {added} cards\n")

# Verify
terrarians = [c for c in cards if 'Terrarian' in c.get('groups', [])]
sys.stdout.write(f"Total Terrarian cards: {len(terrarians)}\n")
for t in terrarians[:5]:
    sys.stdout.write(f"  {t.get('display_name', t['name'])}: type={t.get('card_type')} groups={t.get('groups')}\n")

with open('cards_data.json', 'w', encoding='utf-8') as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)
sys.stdout.write("Saved.\n")
sys.stdout.flush()
