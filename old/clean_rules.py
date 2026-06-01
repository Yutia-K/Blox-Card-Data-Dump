import re

with open('rules.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# Clean up wiki markup remnants
text = re.sub(r"''(.*?)''", r'\1', text)  # italic
text = re.sub(r"'''(.*?)'''", r'\1', text)  # bold
text = re.sub(r'^Category:.*$', '', text, flags=re.MULTILINE)
text = re.sub(r'\n{3,}', '\n\n', text)
text = text.strip() + '\n'

with open('rules.txt', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"Cleaned: {len(text)} chars")
