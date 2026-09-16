import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_block = """      {/* Quick Prompt Suggestions */}
      <div className="flex items-center gap-2 py-2 overflow-x-auto text-[11px] no-scrollbar border-t border-gray-200 dark:border-[#30363d]/50">
        <span className="text-gray-500 shrink-0 font-medium">Quick Prompts:</span>
        <button
          type="button"
          onClick={() => setInput("What are the exact torque specs for spark plugs and cylinder head bolts?")}
          className="bg-[#0d1117] hover:bg-cyan-500/20 hover:text-cyan-300 text-gray-500 dark:text-gray-400 border border-gray-200 dark:border-[#30363d] px-2.5 py-1 rounded-lg shrink-0 transition-colors"
        >
          🔩 Torque Specs
        </button>
        <button
          type="button"
          onClick={() => setInput("How do I perform a compression test and component swap test for cylinder 3 misfire?")}
          className="bg-[#0d1117] hover:bg-cyan-500/20 hover:text-cyan-300 text-gray-500 dark:text-gray-400 border border-gray-200 dark:border-[#30363d] px-2.5 py-1 rounded-lg shrink-0 transition-colors"
        >
          🧪 Cylinder 3 Repair
        </button>
        <button
          type="button"
          onClick={() => setInput("Explain the 120 degree firing order and Cylinder Power Index (CPI) formula.")}
          className="bg-[#0d1117] hover:bg-cyan-500/20 hover:text-cyan-300 text-gray-500 dark:text-gray-400 border border-gray-200 dark:border-[#30363d] px-2.5 py-1 rounded-lg shrink-0 transition-colors"
        >
          📐 I6 Physics & Firing Order
        </button>
        <button
          type="button"
          onClick={() => setInput("What causes P0299 boost leak and P0101 MAF drift?")}
          className="bg-[#0d1117] hover:bg-cyan-500/20 hover:text-cyan-300 text-gray-500 dark:text-gray-400 border border-gray-200 dark:border-[#30363d] px-2.5 py-1 rounded-lg shrink-0 transition-colors"
        >
          💨 P0299 & P0101 Faults
        </button>
      </div>"""

# Remove the bad block
text = text.replace(bad_block, "")

# Find the end of the form
form_end = """        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="p-2.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-2xl disabled:opacity-50 transition-colors shadow shrink-0"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        accept=".csv,.log,.txt"
        className="hidden"
      />"""

good_block = """        <button
          type="submit"
          disabled={!input.trim() || loading}
          className="p-2.5 bg-cyan-600 hover:bg-cyan-500 text-white rounded-2xl disabled:opacity-50 transition-colors shadow shrink-0"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        accept=".csv,.log,.txt"
        className="hidden"
      />
      
      {/* Quick Prompt Suggestions (Bottom Aligned Pills) */}
      <div className="flex items-center justify-center gap-3 pt-4 pb-1 overflow-x-auto text-[11px] no-scrollbar">
        <button
          type="button"
          onClick={() => setInput("What are the exact torque specs for spark plugs and cylinder head bolts?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <span>🔩</span> Torque Specs
        </button>
        <button
          type="button"
          onClick={() => setInput("How do I perform a compression test and component swap test for cylinder 3 misfire?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <span>🧪</span> Cylinder 3 Repair
        </button>
        <button
          type="button"
          onClick={() => setInput("Explain the 120 degree firing order and Cylinder Power Index (CPI) formula.")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <span>📐</span> I6 Physics & Firing Order
        </button>
        <button
          type="button"
          onClick={() => setInput("What causes P0299 boost leak and P0101 MAF drift?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <span>💨</span> P0299 & P0101 Faults
        </button>
      </div>"""

if form_end in text:
    text = text.replace(form_end, good_block)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Success")
else:
    print("Failed to find form end.")

