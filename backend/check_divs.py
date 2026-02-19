
import re

def check_divs(filename):
    with open(filename, 'r') as f:
        content = f.read()

    lines = content.split('\n')
    div_balance = 0
    header_balance = 0
    
    # Regex for div
    div_open = re.compile(r'<div\b')
    div_close = re.compile(r'</div>')
    header_open = re.compile(r'<header\b')
    header_close = re.compile(r'</header>')

    for i, line in enumerate(lines):
        # Count divs
        opens = len(div_open.findall(line))
        closes = len(div_close.findall(line))
        div_balance += (opens - closes)
        
        # Check header
        if header_open.search(line):
            header_balance += 1
            print(f"Header opens at line {i+1}")
        if header_close.search(line):
            header_balance -= 1
            print(f"Header closes at line {i+1}")

    print(f"Final Div Balance: {div_balance}")
    print(f"Final Header Balance: {header_balance}")

check_divs('/home/npe-tech/Projets/MyLife/backend/templates/base.html')
