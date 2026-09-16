import os
import re

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

# Fix Schematic wrapper
bad_schematic = """          {activeTab === 'schematic' && (
            <div className="space-y-6 max-w-7xl mx-auto">
              <div className={`p-4 rounded-xl flex items-center justify-between border ${isDarkMode ? 'bg-[#161b22]/80 backdrop-blur-xl border-white/10' : 'bg-white/80 backdrop-blur-xl border-gray-200/50'}`}>
                <div>
                  <h3 className={`text-sm font-bold flex items-center gap-2 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                    Inline-6 Diesel Engine Real-Time Visual Schematic
                  </h3>
                  <p className={`text-xs mt-0.5 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    Visual mechanical diagram showing Cylinders 1-6 power indices, Common Rail fuel lines, VGT turbo, and EGR valves.
                  </p>
                </div>
              </div>
              <EngineSchematicI6 mlPrediction={mlPred} physicsSummary={physicsSummary} />
            </div>
          )}"""

good_schematic = """          {activeTab === 'schematic' && (
            <div className="max-w-7xl mx-auto">
              <EngineSchematicI6 mlPrediction={mlPred} physicsSummary={physicsSummary} />
            </div>
          )}"""

# Fix Physics wrapper
bad_physics = """          {activeTab === 'physics' && (
            <div className="space-y-6 max-w-7xl mx-auto">
              <div className={`p-4 rounded-xl flex items-center justify-between border ${isDarkMode ? 'bg-[#161b22]/80 backdrop-blur-xl border-white/10' : 'bg-white/80 backdrop-blur-xl border-gray-200/50'}`}>
                <div>
                  <h3 className={`text-sm font-bold flex items-center gap-2 ${isDarkMode ? 'text-white' : 'text-gray-800'}`}>
                    Physics Telemetry Residuals & PyTorch PINN Transformer Output
                  </h3>
                  <p className={`text-xs mt-0.5 ${isDarkMode ? 'text-gray-400' : 'text-gray-500'}`}>
                    Analytical ideal gas airflow residuals, lean lambda bank variance, dynamic crank acceleration balance (CPI 1 to 6).
                  </p>
                </div>
              </div>
              <PhysicsTelemetryCharts physicsSummary={physicsSummary} />
            </div>
          )}"""

good_physics = """          {activeTab === 'physics' && (
            <div className="max-w-7xl mx-auto">
              <PhysicsTelemetryCharts physicsSummary={physicsSummary} />
            </div>
          )}"""

text = text.replace(bad_schematic, good_schematic)
text = text.replace(bad_physics, good_physics)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

