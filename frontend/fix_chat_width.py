import os

# 1. Fix App.jsx
app_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"
with open(app_path, 'r', encoding='utf-8') as f:
    app_text = f.read()

bad_app = """          {activeTab === 'chat' && (
            <div className="max-w-5xl mx-auto">
              <InteractiveChat diagnosticContext={fullDiagnosticContext} />
            </div>
          )}"""

good_app = """          {activeTab === 'chat' && (
            <div className="w-full">
              <InteractiveChat diagnosticContext={fullDiagnosticContext} />
            </div>
          )}"""

app_text = app_text.replace(bad_app, good_app)

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_text)


# 2. Fix InteractiveChat.jsx
chat_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"
with open(chat_path, 'r', encoding='utf-8') as f:
    chat_text = f.read()

# Remove max-w-5xl mx-auto from main wrapper, and adjust h-[78vh] to h-[85vh] for full height
chat_text = chat_text.replace(
    'duration-300 flex flex-col h-[78vh] max-w-5xl mx-auto',
    'duration-300 flex flex-col h-[85vh] w-full'
)

# Fix bot bubble background color in light mode
chat_text = chat_text.replace(
    "'bg-[#0d1117] text-gray-700 dark:text-gray-200 border border-gray-200 dark:border-[#30363d] rounded-tl-none'",
    "'bg-gray-50 dark:bg-[#0d1117] text-gray-800 dark:text-gray-200 border border-gray-200 dark:border-[#30363d] rounded-tl-none'"
)

# Make the chat bubbles wider if needed, or leave max-w-[85%] but because the container is full width, it will look much bigger.
chat_text = chat_text.replace(
    'max-w-[85%]',
    'max-w-[95%]'
)

with open(chat_path, 'w', encoding='utf-8') as f:
    f.write(chat_text)

