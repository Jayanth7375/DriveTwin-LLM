import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# The current text has:
# 'bg-[#0d1117] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(34,211,238,0.1),rgba(255,255,255,0))] text-gray-100'
# We will remove the radial-gradient for dark mode.
text = text.replace(
    "bg-[#0d1117] bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(34,211,238,0.1),rgba(255,255,255,0))] text-gray-100",
    "bg-[#0d1117] text-gray-100"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

