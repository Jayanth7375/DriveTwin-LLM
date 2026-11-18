import re

with open('frontend/src/App.jsx', 'r', encoding='utf-8') as f:
    content = f.read()

# The conflict string
conflict_regex = re.compile(r"<<<<<<< HEAD\n\n        <footer.*?</footer>\n=======\n>>>>>>> [a-f0-9]+\n", re.DOTALL)
match = conflict_regex.search(content)

if match:
    # Keep the footer
    replacement = """
        <footer className={`border-t py-3.5 text-center text-xs mt-auto transition-colors duration-300 ${isDarkMode ? 'bg-[#161b22]/80 backdrop-blur-xl border-white/10 text-gray-500' : 'bg-white/80 backdrop-blur-xl border-gray-200/50 text-gray-400'}`}>
          Diesel Inline-6 Engine LLM Diagnostic Suite  PyTorch PINN & NVIDIA GPU CUDA Active
        </footer>
"""
    new_content = content[:match.start()] + replacement + content[match.end():]
    with open('frontend/src/App.jsx', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Resolved conflict in App.jsx")
else:
    print("Conflict markers not found. Did something change?")
