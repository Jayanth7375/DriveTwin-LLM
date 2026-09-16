import os

# 1. FIX SIDEBAR (Remove Landing Animation tab)
sidebar_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\Sidebar.jsx"
with open(sidebar_path, 'r', encoding='utf-8') as f:
    sidebar_text = f.read()

sidebar_text = sidebar_text.replace(
    "    { id: 'landing', label: 'Landing Animation', icon: <Sparkles className=\"class-for-icon\" /> },\n", 
    ""
)
with open(sidebar_path, 'w', encoding='utf-8') as f:
    f.write(sidebar_text)


# 2. FIX APP.JSX (Conditional full screen landing vs dashboard)
app_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"
with open(app_path, 'r', encoding='utf-8') as f:
    app_text = f.read()

# Make overview the default again and add showLanding state
app_text = app_text.replace(
    "const [activeTab, setActiveTab] = useState('landing');",
    "const [showLanding, setShowLanding] = useState(true);\n  const [activeTab, setActiveTab] = useState('overview');"
)

# Remove the landing tab conditions inside the dashboard
app_text = app_text.replace("{activeTab === 'landing' && 'Scroll Animation Landing Page'}\n              ", "")
app_text = app_text.replace("{activeTab === 'landing' && (\n            <ScrollyLanding />\n          )}\n\n          ", "")

# Wrap the main return in a condition
return_start = app_text.find("return (\n    <div className={`min-h-screen")
if return_start != -1:
    landing_return = """if (showLanding) {
    return <ScrollyLanding onEnter={() => setShowLanding(false)} />;
  }

  return (
    <div className={`min-h-screen"""
    app_text = app_text[:return_start] + landing_return + app_text[return_start + len("return (\n    <div className={`min-h-screen"):]

with open(app_path, 'w', encoding='utf-8') as f:
    f.write(app_text)


# 3. FIX SCROLLYLANDING.JSX (Add "Enter the Dashboard" button and absolute positioning)
scrolly_path = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\ScrollyLanding.jsx"
with open(scrolly_path, 'r', encoding='utf-8') as f:
    scrolly_text = f.read()

# Add onEnter prop
scrolly_text = scrolly_text.replace("export default function ScrollyLanding() {", "export default function ScrollyLanding({ onEnter }) {")

# We want the window itself to be the scroll container now because it's rendering standalone!
# We don't have .overflow-y-auto wrapper anymore.
scrolly_text = scrolly_text.replace(
    "const scrollContainer = containerRef.current?.closest('.overflow-y-auto') || window;",
    "const scrollContainer = window;"
)

# Replace the return block to span the full window, use fixed positioning for canvas, and add the button
return_block_old = """  return (
    <div ref={containerRef} style={{ height: '400vh' }} className="w-full relative">
      <div className="sticky top-0 w-full h-[calc(100vh-150px)] flex flex-col items-center justify-center overflow-hidden">
        {/* Render only the canvas, perfectly sized and centered without any text as requested */}
        <canvas 
          ref={canvasRef} 
          className="w-full h-full object-cover rounded-2xl shadow-2xl"
        />
      </div>
    </div>
  );"""

return_block_new = """  return (
    <div ref={containerRef} style={{ height: '400vh' }} className="w-full bg-[#0d1117] relative">
      <div className="fixed top-0 left-0 w-full h-screen flex flex-col items-center justify-center overflow-hidden">
        <canvas 
          ref={canvasRef} 
          className="w-full h-full object-cover"
        />
        
        {/* Enter Dashboard Button positioned absolutely over the canvas */}
        <div className="absolute bottom-12 left-0 right-0 flex justify-center z-50">
          <button 
            onClick={onEnter}
            className="px-8 py-4 bg-cyan-600 hover:bg-cyan-500 text-white font-bold rounded-full shadow-[0_0_20px_rgba(34,211,238,0.4)] hover:shadow-[0_0_30px_rgba(34,211,238,0.6)] transition-all uppercase tracking-widest"
          >
            Enter the Dashboard
          </button>
        </div>
      </div>
    </div>
  );"""

scrolly_text = scrolly_text.replace(return_block_old, return_block_new)

with open(scrolly_path, 'w', encoding='utf-8') as f:
    f.write(scrolly_text)

