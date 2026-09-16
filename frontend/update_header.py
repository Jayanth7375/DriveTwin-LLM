import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_header = "{activeTab === 'schematic' && '4. Inline-6 Visual HUD & Cylinder Map'}"
good_header = "{activeTab === 'schematic' && 'Real-Time Engine Monitoring'}"

text = text.replace(bad_header, good_header)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

