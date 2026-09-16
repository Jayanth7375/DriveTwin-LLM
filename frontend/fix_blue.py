import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("bg-slate-950", "bg-[#0d1117]")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

