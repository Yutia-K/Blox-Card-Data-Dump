with open('blox_cards.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find makePattern function
i = html.find('function makePattern')
chunk = html[i:i+400]
with open('out.txt', 'w', encoding='utf-8') as f:
    f.write("=== makePattern ===\n")
    f.write(chunk + "\n\n")
    
    # Test what regex "Star" would produce
    j = html.find('const COMBINED_RE')
    f.write("=== COMBINED_RE ===\n")
    f.write(html[j:j+200] + "\n\n")
    
    # Check the escapeRe function
    k = html.find('function escapeRe')
    f.write("=== escapeRe ===\n")
    f.write(html[k:k+200] + "\n")
