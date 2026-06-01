with open('build_html.py','r',encoding='utf-8') as f:
    text = f.read()

with open('search.txt','w',encoding='utf-8') as out:
    out.write(f"filterByGroup count: {text.count('filterByGroup')}\n")
    out.write(f"group-tag count: {text.count('group-tag')}\n")
    out.write(f"group-link count: {text.count('group-link')}\n\n")
    
    i = text.find('filterByGroup')
    out.write(f"filterByGroup at char {i}:\n")
    out.write(text[i:i+300] + '\n\n')
    
    j = text.find('group-tag')
    out.write(f"group-tag at char {j}:\n")
    out.write(text[j:j+300] + '\n\n')
    
    k = text.find('group-link')
    out.write(f"group-link at char {k}:\n")
    out.write(text[k:k+300] + '\n')
