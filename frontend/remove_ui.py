import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\EngineSchematicI6.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Remove 2D/3D toggle
text = text.replace("""            <div className="flex bg-slate-100 dark:bg-black/20 rounded-full p-1 border border-slate-200 dark:border-white/5 text-xs font-bold">
              <button className="px-4 py-1.5 rounded-full text-slate-500 hover:text-slate-700">2D</button>
              <button className="px-4 py-1.5 rounded-full bg-slate-800 text-white shadow-sm">3D</button>
            </div>""", "")

# 2. Remove CPI buttons
text = text.replace("""          <div className="hidden md:flex bg-slate-50 dark:bg-[#0d1117] rounded-full p-1 border border-slate-100 dark:border-white/5 text-xs font-medium text-slate-500">
            <button className="px-4 py-1.5 rounded-full bg-blue-500 text-white shadow-sm">Power Index</button>
            <button className="px-4 py-1.5 rounded-full hover:text-slate-700">Compression</button>
            <button className="px-4 py-1.5 rounded-full hover:text-slate-700">Combustion</button>
            <button className="px-4 py-1.5 rounded-full hover:text-slate-700">Temperature</button>
          </div>""", "")

# 3. Remove the entire bottom row (Quick Actions, Health, Alerts)
bottom_row_start = text.find("{/* BOTTOM ROW: Health, Alerts, Actions */}")
if bottom_row_start != -1:
    # We find the end of this div. The div has grid grid-cols-1 md:grid-cols-3
    text = text[:bottom_row_start] + "      "

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

