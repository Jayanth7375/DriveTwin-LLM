import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\LiveTelemetrySheet.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace hardcoded dark mode with the beautiful glassmorphism that supports light/dark
content = content.replace(
    'bg-[#161b22] border border-[#30363d] rounded-2xl p-5 shadow-sm space-y-5',
    'bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl shadow-black/5 dark:shadow-black/40 ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300 space-y-5'
)

content = content.replace(
    'border-b border-[#30363d]',
    'border-b border-gray-200/50 dark:border-white/10'
)

# Replace inner cards
content = content.replace(
    'bg-[#0d1117] border',
    'bg-white/40 dark:bg-[#0d1117]/40 backdrop-blur-md border border-gray-200/50 dark:border-white/5 hover:border-gray-300/50 dark:hover:border-white/10 transition-colors duration-300'
)

content = content.replace(
    'border-[#30363d]',
    'border-gray-200/50 dark:border-white/10'
)

# Text headers
content = content.replace(
    'text-sm font-bold text-white',
    'text-sm font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400'
)
content = content.replace(
    'text-gray-400',
    'text-gray-500 dark:text-gray-400'
)
content = content.replace(
    'text-gray-200',
    'text-gray-700 dark:text-gray-200'
)
content = content.replace(
    'text-gray-300',
    'text-gray-600 dark:text-gray-300'
)

# Play button
content = content.replace(
    'bg-cyan-600 hover:bg-cyan-500 text-white font-bold flex items-center gap-1.5 transition-colors border border-cyan-400 rounded-none shadow',
    'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-bold flex items-center gap-1.5 transition-all duration-300 border border-transparent rounded-2xl shadow-lg hover:shadow-cyan-500/25 hover:-translate-y-0.5'
)


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

