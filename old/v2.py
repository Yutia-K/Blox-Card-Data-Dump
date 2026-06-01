with open('blox_cards.html', 'r', encoding='utf-8') as f:
    html = f.read()

i = html.find('function makePattern')
with open('verify.txt', 'w', encoding='utf-8') as f:
    f.write(html[i:i+300])
