with open('blox_cards.html','r',encoding='utf-8') as f:
    html = f.read()
i = html.find('ESC_RE')
with open('debug.txt','w') as out:
    out.write(html[i:i+500])
