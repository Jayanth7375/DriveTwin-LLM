import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Round corners
content = content.replace('rounded-none', 'rounded-2xl')
content = content.replace('rounded-xl', 'rounded-2xl')

# 2. Outer wrapper
content = content.replace(
    'bg-[#161b22] border border-[#30363d] rounded-2xl p-5 shadow-xl',
    'bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl shadow-black/5 dark:shadow-black/40 ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300'
)

# 3. Inner inputs / boxes
content = content.replace(
    'bg-[#0d1117] border border-[#30363d]',
    'bg-white dark:bg-[#0d1117] border border-gray-200 dark:border-[#30363d]'
)
content = content.replace(
    'bg-[#161b22] text-cyan-400 border-b border-[#30363d]',
    'bg-gray-100 dark:bg-[#161b22] text-blue-600 dark:text-cyan-400 border-b border-gray-200 dark:border-[#30363d]'
)

# text colors
content = content.replace(
    'text-white',
    'text-gray-900 dark:text-white'
)
content = content.replace(
    'text-gray-200',
    'text-gray-700 dark:text-gray-200'
)
content = content.replace(
    'text-gray-300',
    'text-gray-600 dark:text-gray-300'
)
content = content.replace(
    'text-gray-400',
    'text-gray-500 dark:text-gray-400'
)

# Border colors
content = content.replace(
    'border-[#30363d]',
    'border-gray-200 dark:border-[#30363d]'
)
content = content.replace(
    'border-b border-[#30363d]',
    'border-b border-gray-200 dark:border-[#30363d]'
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

