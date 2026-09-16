import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\TelemetryUploader.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_code = """      {/* LEFT: HERO TEXT */}
      <div className="flex-1 space-y-6">
        <div className="flex items-center gap-4">
          <div className="h-0.5 w-10 bg-cyan-500 rounded-full"></div>
          <span className="text-xs font-mono font-semibold tracking-widest text-gray-500 dark:text-gray-400 uppercase">
            Real-Time Engine Intelligence
          </span>
        </div>
        
        <h1 className="text-5xl lg:text-6xl font-black text-gray-900 dark:text-white leading-[1.1] tracking-tight">
          Keep Your Engine <br />
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-emerald-400 to-cyan-500">
            One Step Ahead
          </span>
        </h1>
        
        <p className="text-gray-600 dark:text-gray-400 max-w-lg text-lg">
          Connect, monitor and analyze your engine with AI-powered diagnostics.
        </p>
        
        {/* Badges */}
        <div className="flex flex-wrap gap-6 pt-4">
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-emerald-500/10 flex items-center justify-center border border-emerald-500/20 shadow-[0_0_15px_rgba(16,185,129,0.15)]">
              <ShieldCheck className="w-6 h-6 text-emerald-500" />
            </div>
            <div>
              <p className="text-sm font-bold text-gray-900 dark:text-white">Detect</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">Faults Early</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-blue-500/10 flex items-center justify-center border border-blue-500/20 shadow-[0_0_15px_rgba(59,130,246,0.15)]">
              <LineChart className="w-6 h-6 text-blue-500" />
            </div>
            <div>
              <p className="text-sm font-bold text-gray-900 dark:text-white">Monitor</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">In Real-Time</p>
            </div>
          </div>
          
          <div className="flex items-center gap-3">
            <div className="w-12 h-12 rounded-full bg-cyan-500/10 flex items-center justify-center border border-cyan-500/20 shadow-[0_0_15px_rgba(34,211,238,0.15)]">
              <Sparkles className="w-6 h-6 text-cyan-400" />
            </div>
            <div>
              <p className="text-sm font-bold text-gray-900 dark:text-white">Predict</p>
              <p className="text-xs text-gray-500 dark:text-gray-400">With AI</p>
            </div>
          </div>
        </div>
      </div>"""

good_code = """      {/* LEFT: HERO TEXT */}
      <div className="flex-1 space-y-8">
        <div className="flex items-center gap-4">
          <div className="h-0.5 w-12 bg-cyan-600 rounded-full"></div>
          <span className="text-xs font-mono font-bold tracking-[0.2em] text-gray-500 dark:text-gray-400 uppercase">
            Real-Time Engine Intelligence
          </span>
        </div>
        
        <h1 className="text-[4.5rem] lg:text-[5.5rem] font-black text-gray-900 dark:text-white leading-[0.95] tracking-tighter">
          Keep Your<br />
          Engine<br />
          <span className="text-transparent bg-clip-text bg-gradient-to-b from-[#81e6b3] via-[#71d3d6] to-[#60b6e9]">
            One Step<br />
            Ahead
          </span>
        </h1>
        
        <p className="text-gray-600 dark:text-gray-300 max-w-md text-lg leading-relaxed pt-2">
          Connect, monitor and analyze your engine with AI-powered diagnostics.
        </p>
        
        {/* Badges */}
        <div className="flex flex-wrap gap-8 pt-4">
          <div className="flex items-center gap-4">
            <div className="w-[52px] h-[52px] rounded border bg-emerald-500/5 border-emerald-500/30 flex items-center justify-center">
              <ShieldCheck className="w-6 h-6 text-emerald-400" />
            </div>
            <div>
              <p className="text-[15px] font-bold text-gray-900 dark:text-white leading-tight">Detect</p>
              <p className="text-[13px] text-gray-500 dark:text-gray-400 leading-tight">Faults Early</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="w-[52px] h-[52px] rounded border bg-blue-500/5 border-blue-500/30 flex items-center justify-center">
              <LineChart className="w-6 h-6 text-blue-400" />
            </div>
            <div>
              <p className="text-[15px] font-bold text-gray-900 dark:text-white leading-tight">Monitor</p>
              <p className="text-[13px] text-gray-500 dark:text-gray-400 leading-tight">In Real-Time</p>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="w-[52px] h-[52px] rounded border bg-cyan-500/5 border-cyan-500/30 flex items-center justify-center">
              <Sparkles className="w-6 h-6 text-cyan-400" />
            </div>
            <div>
              <p className="text-[15px] font-bold text-gray-900 dark:text-white leading-tight">Predict</p>
              <p className="text-[13px] text-gray-500 dark:text-gray-400 leading-tight">With AI</p>
            </div>
          </div>
        </div>
      </div>"""

if bad_code in text:
    text = text.replace(bad_code, good_code)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    print("Replaced successfully")
else:
    print("Could not find bad code block")

