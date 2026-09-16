import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the current light mode background
old_bg = "bg-[linear-gradient(135deg,#ff0000_0%,#00008b_50%,#3264ad_100%)] text-white"
new_bg = "bg-[linear-gradient(135deg,#3264AD_0%,darkblue_50%,red_100%)] text-white"

text = text.replace(old_bg, new_bg)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

