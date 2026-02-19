
import re

def trace_tags(filename):
    with open(filename, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    stack = []
    
    tag_re = re.compile(r'{%\s*(\w+).*?%}')

    print("--- Tag Trace ---")
    for i, line in enumerate(lines):
        for match in tag_re.finditer(line):
            tag_name = match.group(1)
            full_tag = match.group(0)
            
            if tag_name in ['if', 'for', 'block', 'with']:
                stack.append((tag_name, i + 1, full_tag))
                print(f"Push: {tag_name} at line {i+1} (Stack depth: {len(stack)})")
            elif tag_name in ['endif', 'endfor', 'endblock', 'endwith']:
                if not stack:
                    print(f"Error: Unexpected {{% {tag_name} %}} at line {i+1}")
                    return
                
                last_tag, last_line, _ = stack[-1]
                expected_end = 'end' + last_tag
                
                if tag_name == expected_end:
                    stack.pop()
                    print(f"Pop: {tag_name} at line {i+1} matches {last_tag} from {last_line} (Stack depth: {len(stack)})")
                else:
                    pass

    if stack:
        print("Unclosed tags found:")
        for tag, line, content in stack:
            print(f"Line {line}: {content}")

trace_tags('/home/npe-tech/Projets/MyLife/backend/templates/base.html')
