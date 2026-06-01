with open('blox_cards.html','r',encoding='utf-8') as f:
    html = f.read()

i = html.find('NAME_REGEX')
with open('debug.txt','w') as out:
    out.write(html[i:i+500] + '\n\n')
    
    # Also check the regex replace part
    j = html.find('.replace(', i)
    out.write('Replace context:\n')
    out.write(html[j:j+200] + '\n')
