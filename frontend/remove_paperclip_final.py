import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_chunk = """        <form onSubmit={handleSend} className="flex items-center gap-2 pt-2">
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

good_chunk = """        <form onSubmit={handleSend} className="flex items-center gap-2 pt-2">"""

text = text.replace(bad_chunk, good_chunk)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

