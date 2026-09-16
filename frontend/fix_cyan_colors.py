import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix text colors
text = text.replace('text-cyan-200', 'text-cyan-800 dark:text-cyan-200')
text = text.replace('text-cyan-300', 'text-cyan-700 dark:text-cyan-300')
text = text.replace('text-cyan-400', 'text-cyan-600 dark:text-cyan-400')

# Fix background colors
text = text.replace('bg-cyan-500/10', 'bg-cyan-50 dark:bg-cyan-500/10')
text = text.replace('bg-cyan-950/80', 'bg-gray-100 dark:bg-cyan-950/80')

# Fix border colors
text = text.replace('border-cyan-500/20', 'border-cyan-200 dark:border-cyan-500/20')
text = text.replace('border-cyan-500/30', 'border-cyan-300 dark:border-cyan-500/30')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

