import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Remove the old quick prompts block completely
# It starts with {/* Quick Prompt Suggestions */} and ends before {/* Input Form with File Attachment Button */}

pattern = re.compile(r'\{\/\* Quick Prompt Suggestions \*\/\}.*?(?=\{\/\* Input Form)', re.DOTALL)
text = pattern.sub('', text)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

