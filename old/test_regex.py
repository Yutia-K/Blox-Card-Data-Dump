with open('blox_cards.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find makePattern in the actual HTML output
i = html.find('function makePattern')
chunk = html[i:i+300]
with open('out.txt', 'w', encoding='utf-8') as f:
    f.write("=== In HTML output ===\n")
    f.write(chunk + "\n\n")
    
    # Test: what would makePattern produce for "Star"?
    # Simulate in Python
    import re
    name = "Star"
    e = re.sub(r'[.*+?^${}()|[\]\\]', r'\\&', name)
    pre = r'\b' if re.match(r'\w', name) else ''
    suf = r'\b' if re.match(r'.*\w$', name) else ''
    pattern = pre + e + suf
    f.write(f"Pattern for 'Star': {pattern}\n")
    
    # Test against "start"
    test_re = re.compile(pattern, re.IGNORECASE)
    match = test_re.search('start')
    f.write(f"'Star' in 'start': {match}\n")
    
    match2 = test_re.search('Star')
    f.write(f"'Star' in 'Star': {match2}\n")
    
    # Also test "Era" in "obliterated"
    name2 = "Era"
    e2 = re.sub(r'[.*+?^${}()|[\]\\]', r'\\&', name2)
    pre2 = r'\b' if re.match(r'\w', name2) else ''
    suf2 = r'\b' if re.match(r'.*\w$', name2) else ''
    pattern2 = pre2 + e2 + suf2
    f.write(f"\nPattern for 'Era': {pattern2}\n")
    test_re2 = re.compile(pattern2, re.IGNORECASE)
    match3 = test_re2.search('obliterated')
    f.write(f"'Era' in 'obliterated': {match3}\n")
