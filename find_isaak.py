import json, sys, re, urllib.request, urllib.parse, time

BASE = "https://blox-cards.fandom.com/api.php"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def api_get(params):
    params["format"] = "json"
    url = BASE + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=20) as resp:
        return json.loads(resp.read().decode("utf-8"))

target = "Isaak Brodsky"
pages = ["Blue_Cards", "Red_Cards", "Green_Cards", "Yellow_Cards", "Colourless_Cards",
         "Action_And_Terrain_Cards", "Gear_Cards", "Tokens"]

for page in pages:
    data = api_get({"action": "parse", "page": page, "prop": "wikitext"})
    wt = data["parse"]["wikitext"]["*"]
    if target in wt:
        lines = wt.split('\n')
        current_section = 'top'
        for i, line in enumerate(lines):
            m = re.match(r'={2,3}\s*(.*?)\s*={2,3}', line)
            if m:
                current_section = m.group(1)
            if target in line:
                sys.stdout.write(f"  {page} section=[{current_section}] line {i}\n")
    time.sleep(0.3)
sys.stdout.flush()
