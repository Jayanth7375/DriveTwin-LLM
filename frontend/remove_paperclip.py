import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_chunk = """        {/* Input Form with File Attachment Button */}
      <form onSubmit={handleSend} className="flex items-center gap-2 pt-2">
        <button
          type="button"
          onClick={() => fileInputRef.current?.click()}
          title="Upload ECU CSV/Excel file directly in chat"
          className="p-2.5 bg-[#0d1117] hover:bg-[#21262d] border border-gray-200 dark:border-[#30363d] hover:border-cyan-400 text-cyan-600 dark:text-cyan-400 rounded-2xl transition-colors shrink-0"
        >
          <Paperclip className="w-4 h-4" />
        </button>

        <input
          type="file"
          ref={fileInputRef}
          accept=".csv,.xlsx,.xls"
          onChange={handleFileUploadInChat}
          className="hidden"
        />"""

import re
# Use regex to strip it because of exact whitespace
text = re.sub(
    r'<button[^>]*>\s*<Paperclip[^>]*/>\s*</button>', 
    '', 
    text
)

text = re.sub(
    r'<input\s+type="file"\s+ref=\{fileInputRef\}[^>]*/>',
    '',
    text
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

