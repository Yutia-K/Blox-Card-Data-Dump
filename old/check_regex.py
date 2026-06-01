with open('blox_cards.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the ESC_RE line
i = html.find('const ESC_RE')
j = html.find(';', i)
with open('debug_regex.txt', 'w', encoding='utf-8') as out:
    out.write(html[i:j+1] + '\n\n')

    # Find linkEffect function
    k = html.find('function linkEffect')
    l = html.find('}', html.find('}', k) + 1) + 1
    out.write(html[k:l+1] + '\n\n')

    # Find BLACKLIST
    m = html.find('const BLACKLIST')
    n = html.find(';', m)
    out.write(html[m:n+1] + '\n')
