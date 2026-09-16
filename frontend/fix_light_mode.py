import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the current light mode background
old_bg = "bg-gray-50 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(34,211,238,0.15),rgba(255,255,255,0))] text-gray-900"
new_bg = "bg-[linear-gradient(135deg,#ff0000_0%,#00008b_50%,#3264ad_100%)] text-white"

text = text.replace(old_bg, new_bg)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

