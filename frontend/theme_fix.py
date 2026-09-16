import os
import re

files_to_patch = [
    'src/components/TelemetryUploader.jsx',
    'src/components/DiagnosticCard.jsx',
    'src/components/LiveTelemetrySheet.jsx'
]

replacements = {
    'bg-[#161b22]': 'bg-white dark:bg-[#161b22]',
    'bg-[#0d1117]': 'bg-gray-50 dark:bg-[#0d1117]',
    'border-[#30363d]': 'border-gray-200 dark:border-[#30363d]',
    'text-gray-400': 'text-gray-500 dark:text-gray-400',
    'text-gray-300': 'text-gray-600 dark:text-gray-300',
    # We must be careful with text-white. Let's do a regex that replaces text-white if it's NOT near bg-cyan, bg-emerald, bg-red
}

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    for old, new in replacements.items():
        content = content.replace(old, new)
        
    # Replace text-white cautiously: 
    # find className="..." strings and replace text-white only if they don't contain bg-cyan, bg-emerald, bg-red
    def repl_classname(m):
        cls_str = m.group(1)
        if 'bg-cyan' not in cls_str and 'bg-emerald' not in cls_str and 'bg-red' not in cls_str and 'bg-blue' not in cls_str:
            cls_str = cls_str.replace('text-white', 'text-gray-900 dark:text-white')
        return f'className="{cls_str}"'
    
    content = re.sub(r'className="([^"]+)"', repl_classname, content)
    
    # same for template literals className={`...`}
    def repl_classname_tmpl(m):
        cls_str = m.group(1)
        if 'bg-cyan' not in cls_str and 'bg-emerald' not in cls_str and 'bg-red' not in cls_str and 'bg-blue' not in cls_str:
            cls_str = cls_str.replace('text-white', 'text-gray-900 dark:text-white')
        return f'className={{`{cls_str}`}}'
        
    content = re.sub(r'className=\{`([^`]+)`\}', repl_classname_tmpl, content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for f in files_to_patch:
    process_file(f)
    print(f"Patched {f}")

