import json, sys, re, urllib.request, urllib.parse, time

BASE = "https://blox-cards.fandom.com/api.php"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def api_get(params):
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))

targets = ['Queen Shedare II', 'Termiteking9', 'Alpha-O & Pier - Intergalactic Rivals']
pages = ["Blue_Cards", "Red_Cards", "Green_Cards", "Yellow_Cards", "Colourless_Cards",
         "Action_And_Terrain_Cards", "Gear_Cards", "Tokens"]

for t in targets:
    sys.stdout.write(f"\n=== Searching for '{t}' ===\n")
    for page in pages:
        data = api_get({"action": "parse", "page": page, "prop": "wikitext"})
        wt = data["parse"]["wikitext"]["*"]
        
        # Check if card appears in this page
        if t in wt:
            # Find which section it's in
            lines = wt.split('\n')
            current_section = 'top'
            for i, line in enumerate(lines):
                m = re.match(r'={2,3}\s*(.*?)\s*={2,3}', line)
                if m:
                    current_section = m.group(1)
                # Also check tabber headers
                tm = re.match(r'-\|(.+)=', line)
                if tm:
                    current_section = 'tab:' + tm.group(1)
                if t in line:
                    sys.stdout.write(f"  Found in {page} section=[{current_section}] line {i}\n")
        time.sleep(0.3)
    sys.stdout.flush()
