with open('blox_cards.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find ESC_RE assignment and get surrounding context
i = html.find('const ESC_RE = new RegExp(')
# Get 500 chars from that point
chunk = html[i:i+800]
with open('debug2.txt', 'w', encoding='utf-8') as out:
    out.write(chunk)
