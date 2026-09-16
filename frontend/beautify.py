import os
import re

files_to_patch = [
    'src/components/TelemetryUploader.jsx',
    'src/components/DiagnosticCard.jsx',
    'src/components/LiveTelemetrySheet.jsx',
    'src/components/PhysicsTelemetryCharts.jsx'
]

def beautify_file(filepath):
    if not os.path.exists(filepath): return
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Round corners
    content = content.replace('rounded-none', 'rounded-2xl')

    # 2. Upgrade main outer wrappers
    # TelemetryUploader / DiagnosticCard main wrappers usually have:
    # "bg-white dark:bg-[#161b22] border border-gray-200 dark:border-[#30363d] rounded-2xl p-5 shadow-sm"
    # Wait, I just replaced rounded-none with rounded-2xl, so:
    content = re.sub(
        r'bg-white dark:bg-\[\#161b22\] border border-gray-200 dark:border-\[\#30363d\] rounded-2xl p-5 shadow-sm',
        r'bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-2xl p-6 shadow-2xl shadow-black/5 dark:shadow-black/40 ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300',
        content
    )
    
    # In DiagnosticCard, it doesn't have `space-y-5`, just `shadow-sm`
    content = re.sub(
        r'bg-white dark:bg-\[\#161b22\] border border-gray-200 dark:border-\[\#30363d\] rounded-2xl p-5\nshadow-sm',
        r'bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-2xl p-6 shadow-2xl shadow-black/5 dark:shadow-black/40 ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300',
        content
    )

    # LiveTelemetrySheet uses `p-6` maybe? Let's genericize:
    content = re.sub(
        r'bg-white dark:bg-\[\#161b22\] border border-gray-200 dark:border-\[\#30363d\] rounded-2xl p-([0-9]+) shadow-sm',
        r'bg-white/60 dark:bg-[#161b22]/60 backdrop-blur-xl border border-gray-200/50 dark:border-white/10 rounded-2xl p-\1 shadow-2xl shadow-black/5 dark:shadow-black/40 ring-1 ring-black/5 dark:ring-white/5 transition-all duration-300',
        content
    )

    # 3. Upgrade inner wrappers (bg-gray-50 / #0d1117)
    content = content.replace(
        'bg-gray-50 dark:bg-[#0d1117] border border-gray-200 dark:border-[#30363d]',
        'bg-gray-100/50 dark:bg-[#0d1117]/50 backdrop-blur-md border border-gray-200/50 dark:border-white/5 hover:border-gray-300/50 dark:hover:border-white/10 transition-colors duration-300'
    )
    
    content = content.replace(
        'border-gray-200 dark:border-[#30363d]',
        'border-gray-200/50 dark:border-white/10'
    )

    # 4. Beautify Header Text
    content = content.replace(
        'text-base font-semibold text-gray-900 dark:text-white',
        'text-lg font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400'
    )
    content = content.replace(
        'text-sm font-bold text-gray-900 dark:text-white',
        'text-sm font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-500 dark:from-white dark:to-gray-400'
    )

    # 5. Make buttons pop
    content = content.replace(
        'bg-cyan-600 hover:bg-cyan-500',
        'bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 shadow-lg hover:shadow-cyan-500/25 hover:-translate-y-0.5'
    )
    
    # 6. Make progress bars glow
    content = content.replace(
        'bg-cyan-400',
        'bg-gradient-to-r from-cyan-400 to-blue-500 shadow-[0_0_10px_rgba(34,211,238,0.5)]'
    )
    
    # 7. Badges enhancements
    content = content.replace(
        'bg-cyan-500/10 text-cyan-300',
        'bg-cyan-500/10 text-cyan-400 shadow-[0_0_10px_rgba(34,211,238,0.1)]'
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in files_to_patch:
    beautify_file(f)
    print(f"Beautified {f}")

