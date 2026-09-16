import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace("import ScrollyLanding from './components/ScrollyLanding';", "import VideoLanding from './components/VideoLanding';")
text = text.replace("<ScrollyLanding onEnter={() => setShowLanding(false)} />", "<VideoLanding onEnter={() => setShowLanding(false)} />")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

