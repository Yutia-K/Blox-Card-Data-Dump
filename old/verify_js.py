with open('blox_cards.html', 'r', encoding='utf-8') as f:
    html = f.read()

i = html.find('const COMBINED_RE')
with open('debug.txt', 'w', encoding='utf-8') as out:
    out.write(html[i:i+600] + '\n\n')
    
    # Check linkEffect function
    j = html.find('function linkEffect')
    out.write(html[j:j+800])
