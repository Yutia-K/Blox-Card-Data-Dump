with open('blox_cards.html', 'rb') as f:
    html = f.read()

# Find "makePattern" in raw bytes
idx = html.find(b'makePattern')
# Get 400 bytes around it
chunk = html[idx:idx+400]
with open('raw.txt', 'wb') as f:
    f.write(chunk)
