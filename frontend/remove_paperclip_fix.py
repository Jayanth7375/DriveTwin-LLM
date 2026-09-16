import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
skip = False
for line in lines:
    if "<button" in line and "fileInputRef.current?.click()" in line:
        # We are at the start of the button
        skip = True
    elif skip and "<Paperclip" in line:
        pass
    elif skip and "</button>" in line:
        skip = False
    elif not skip:
        new_lines.append(line)

final_lines = []
skip2 = False
for line in new_lines:
    if '<input' in line and 'type="file"' in line and 'ref={fileInputRef}' in line:
        skip2 = True
    elif skip2 and '/>' in line:
        skip2 = False
    elif not skip2:
        final_lines.append(line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

