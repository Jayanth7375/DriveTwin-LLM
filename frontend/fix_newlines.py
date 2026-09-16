import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Replace the broken string literals with fixed ones using backticks or \\n
text = text.replace('title: "Diagnose\na Fault"', 'title: "Diagnose\\na Fault"')
text = text.replace('title: "Explain\na Code"', 'title: "Explain\\na Code"')
text = text.replace('title: "Analyze\nSensor Data"', 'title: "Analyze\\nSensor Data"')
text = text.replace('title: "Show in\n3D Model"', 'title: "Show in\\n3D Model"')

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

