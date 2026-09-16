import os
import re

input_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\old_LiveTelemetrySheet.jsx"
output_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\LiveTelemetrySheet.jsx"

with open(input_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Round corners
content = content.replace('rounded-none', 'rounded-2xl')

# 2. Outer wrapper
content = content.replace(
    'bg-white dark:bg-[#161b22] border border-gray-200 dark:border-[#30363d] rounded-2xl p-6 shadow-sm',
    'bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-3xl p-6 shadow-2xl shadow-black/5 dark:shadow-black/40 ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300'
)

# 3. Inner grid cards
content = content.replace(
    'bg-gray-50 dark:bg-[#0d1117] border',
    'bg-white/40 dark:bg-[#0d1117]/40 backdrop-blur-md border border-gray-200/50 dark:border-white/5 hover:border-gray-300/50 dark:hover:border-white/10 transition-colors duration-300'
)

content = content.replace(
    'border-gray-200 dark:border-[#30363d]',
    'border-gray-200/50 dark:border-white/10'
)

# 4. Headers
content = content.replace(
    'text-base font-semibold text-gray-900 dark:text-white',
    'text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400'
)
content = content.replace(
    'text-sm font-bold text-gray-900 dark:text-white',
    'text-sm font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400'
)

# 5. Buttons
content = content.replace(
    'bg-cyan-600 hover:bg-cyan-500 text-white shadow',
    'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 shadow-lg hover:shadow-cyan-500/25 hover:-translate-y-0.5 text-white'
)

# The old play/pause button: 
# bg-cyan-600 hover:bg-cyan-500 text-white font-bold flex items-center gap-1.5 transition-colors border border-cyan-400 rounded-none shadow
content = content.replace(
    'bg-cyan-600 hover:bg-cyan-500',
    'bg-gradient-to-r from-emerald-500 to-emerald-600 hover:from-emerald-400 hover:to-emerald-500 shadow-lg hover:shadow-emerald-500/25 hover:-translate-y-0.5 border-transparent'
)


with open(output_path, 'w', encoding='utf-8') as f:
    f.write(content)

