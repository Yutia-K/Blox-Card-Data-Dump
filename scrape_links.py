import re

with open('wiki_main.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find all wiki links
links = re.findall(r'href="(/wiki/[^"]+)"', html)
unique = sorted(set(links))
for link in unique[:100]:
    print(link)
print(f"\n--- Total unique links: {len(unique)} ---")
