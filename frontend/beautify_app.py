import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Change the main background to have a subtle radial gradient so the glass cards look better
text = text.replace(
    "bg-[#0d1117] text-gray-100",
    "bg-slate-950 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(34,211,238,0.1),rgba(255,255,255,0))] text-gray-100"
)

text = text.replace(
    "bg-gray-50 text-gray-900",
    "bg-gray-50 bg-[radial-gradient(ellipse_80%_80%_at_50%_-20%,rgba(34,211,238,0.15),rgba(255,255,255,0))] text-gray-900"
)

# Header glassmorphism
text = text.replace(
    "bg-[#161b22] border-[#30363d]",
    "bg-[#161b22]/80 backdrop-blur-xl border-white/10"
)
text = text.replace(
    "bg-white border-gray-200",
    "bg-white/80 backdrop-blur-xl border-gray-200/50"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

