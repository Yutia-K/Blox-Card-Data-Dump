import json, sys, re, urllib.request, urllib.parse, time

BASE = 'https://blox-cards.fandom.com/api.php'
HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_wikitext(page):
    params = {'action': 'parse', 'page': page, 'format': 'json', 'prop': 'wikitext'}
    url = BASE + '?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as r:
        d = json.loads(r.read().decode('utf-8'))
    return d['parse']['wikitext']['*']

def clean_wikitext(wt):
    wt = re.sub(r'\[\[File:[^\]]*\]\]', '', wt)
    wt = re.sub(r'\[\[([^\]|]*?)\]\]', r'\1', wt)
    wt = re.sub(r'\[\[[^\]]*?\|([^\]]*?)\]\]', r'\1', wt)
    wt = re.sub(r'\{\{[^}]*\}\}', '', wt)
    wt = re.sub(r'<[^>]+>', '', wt)
    wt = re.sub(r'\n{3,}', '\n\n', wt)
    return wt.strip()

pages = ['How_to_Play', 'Battle', 'Effect_Powers', 'Passives', 'Lock', 'Baseplate_(Game_Mechanic)']
all_text = 'BLOX CARDS - RULES REFERENCE\n' + '=' * 50 + '\n\n'

for page in pages:
    sys.stdout.write(f'Fetching {page}...\n')
    sys.stdout.flush()
    try:
        wt = get_wikitext(page)
        cleaned = clean_wikitext(wt)
        title = page.replace('_', ' ')
        all_text += f'## {title}\n\n{cleaned}\n\n\n'
    except Exception as e:
        sys.stdout.write(f'  Failed: {e}\n')
    time.sleep(0.3)

with open('rules.txt', 'w', encoding='utf-8') as f:
    f.write(all_text)
sys.stdout.write(f'Done: {len(all_text)} chars written to rules.txt\n')
sys.stdout.flush()
