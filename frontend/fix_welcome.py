import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Replace any emoji before "Welcome"
text = re.sub(r'### [^\w]*Welcome', '### Welcome', text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

