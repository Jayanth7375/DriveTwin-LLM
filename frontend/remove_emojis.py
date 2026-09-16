import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\InteractiveChat.jsx"

with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
    text = f.read()

# Fix the Welcome Message
# Note: since the file might have weird bytes, let's use a regex or just simple replace for the "Welcome" line
text = text.replace("### 🤖 Welcome to the Inline-6 RAG AI Diagnostic Assistant!", "### Welcome to the Inline-6 RAG AI Diagnostic Assistant!")
text = text.replace("### dY - Welcome to the Inline-6 RAG AI Diagnostic Assistant!", "### Welcome to the Inline-6 RAG AI Diagnostic Assistant!")
text = text.replace("### ðŸ¤– Welcome", "### Welcome")

# Replace Quick Prompts with Lucide Icons
bad_prompts = """      {/* Quick Prompt Suggestions (Bottom Aligned Pills) */}
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

good_prompts = """      {/* Quick Prompt Suggestions (Bottom Aligned Pills) */}
      <div className="flex items-center justify-center gap-3 pt-4 pb-1 overflow-x-auto text-[11px] no-scrollbar">
        <button
          type="button"
          onClick={() => setInput("What are the exact torque specs for spark plugs and cylinder head bolts?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <Wrench className="w-3.5 h-3.5 text-gray-500" /> Torque Specs
        </button>
        <button
          type="button"
          onClick={() => setInput("How do I perform a compression test and component swap test for cylinder 3 misfire?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <Activity className="w-3.5 h-3.5 text-gray-500" /> Cylinder 3 Repair
        </button>
        <button
          type="button"
          onClick={() => setInput("Explain the 120 degree firing order and Cylinder Power Index (CPI) formula.")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <BarChart3 className="w-3.5 h-3.5 text-gray-500" /> I6 Physics & Firing Order
        </button>
        <button
          type="button"
          onClick={() => setInput("What causes P0299 boost leak and P0101 MAF drift?")}
          className="bg-transparent hover:bg-gray-100 dark:hover:bg-[#21262d] text-gray-600 dark:text-gray-300 border border-gray-200 dark:border-[#30363d] px-3.5 py-1.5 rounded-full shrink-0 transition-colors flex items-center gap-2"
        >
          <AlertTriangle className="w-3.5 h-3.5 text-gray-500" /> P0299 & P0101 Faults
        </button>
      </div>"""

if bad_prompts in text:
    text = text.replace(bad_prompts, good_prompts)
else:
    print("Could not find bad prompts to replace")

# Add the new imports to lucide-react if they don't exist
import_line = "import { MessageSquare, Send, Bot, User, Sparkles, Paperclip, FileSpreadsheet, ShieldAlert, CheckCircle2 } from 'lucide-react';"
new_import_line = "import { MessageSquare, Send, Bot, User, Sparkles, Paperclip, FileSpreadsheet, ShieldAlert, CheckCircle2, Wrench, Activity, BarChart3, AlertTriangle } from 'lucide-react';"

if import_line in text:
    text = text.replace(import_line, new_import_line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

