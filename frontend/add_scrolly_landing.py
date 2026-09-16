import os
import re

# 1. Update App.jsx
filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Import the new component
text = text.replace("import DigitalTwinView from './components/DigitalTwinView';", 
                    "import DigitalTwinView from './components/DigitalTwinView';\nimport ScrollyLanding from './components/ScrollyLanding';")

# Change default tab
text = text.replace("const [activeTab, setActiveTab] = useState('overview');",
                    "const [activeTab, setActiveTab] = useState('landing');")

# Add the title for landing
text = text.replace("{activeTab === 'overview' && '1. Diagnostics & Telemetry Ingestion'}",
                    "{activeTab === 'landing' && 'Scroll Animation Landing Page'}\n              {activeTab === 'overview' && '1. Diagnostics & Telemetry Ingestion'}")

# Add the render block for landing
text = text.replace("{activeTab === 'overview' && (",
                    "{activeTab === 'landing' && (\n            <ScrollyLanding />\n          )}\n\n          {activeTab === 'overview' && (")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

# 2. Update Sidebar.jsx
sidebar_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\Sidebar.jsx"

with open(sidebar_path, 'r', encoding='utf-8') as f:
    sidebar_text = f.read()

# Add a nav item for landing at the top
sidebar_text = sidebar_text.replace(
    "const navItems = [\n    { id: 'overview'",
    "const navItems = [\n    { id: 'landing', label: 'Landing Animation', icon: <Sparkles className=\"class-for-icon\" /> },\n    { id: 'overview'"
)

with open(sidebar_path, 'w', encoding='utf-8') as f:
    f.write(sidebar_text)

