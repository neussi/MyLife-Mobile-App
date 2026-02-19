
import re

def check_template(filename):
    with open(filename, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    stack = []
    
    # Regex for tags
    tag_re = re.compile(r'{%\s*(\w+).*?%}')

    for i, line in enumerate(lines):
        for match in tag_re.finditer(line):
            tag_name = match.group(1)
            full_tag = match.group(0)
            
            if tag_name in ['if', 'for', 'block', 'with']:
                stack.append((tag_name, i + 1, full_tag))
            elif tag_name in ['endif', 'endfor', 'endblock', 'endwith']:
                if not stack:
                    print(f"Error: Unexpected {{% {tag_name} %}} at line {i+1}")
                    return
                
                last_tag, last_line, _ = stack[-1]
                expected_end = 'end' + last_tag
                
                if tag_name == expected_end:
                    stack.pop()
                else:
                    # Ignore mismatches if it's just elif/else (handled inside)
                    # But wait, elif/else don't close.
                    pass

    if stack:
        print("Unclosed tags found:")
        for tag, line, content in stack:
            print(f"Line {line}: {content}")
    else:
        print("Template is balanced.")

check_template('/home/npe-tech/Projets/MyLife/backend/templates/base.html')
