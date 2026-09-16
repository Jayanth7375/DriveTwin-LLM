import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\EngineSchematicI6.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Add the missing closing tags for the component wrapper
text += """
    </div>
  );
}
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

