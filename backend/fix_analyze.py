import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\backend\app\api\routes_analyze.py"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace('except Exception as e:', 'except Exception as e:\n        import traceback\n        traceback.print_exc()\n')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

