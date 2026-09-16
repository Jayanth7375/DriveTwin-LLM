import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Remove the button with the Paperclip
text = re.sub(
    r'<button[^>]*onClick=\{[^}]*fileInputRef\.current\?\.click\(\)[^}]*\}[^>]*>[\s\S]*?<Paperclip[^>]*/>[\s\S]*?</button>', 
    '', 
    text
)

# Remove the hidden input
text = re.sub(
    r'<input\s+type="file"\s+ref=\{fileInputRef\}[\s\S]*?/>',
    '',
    text
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

