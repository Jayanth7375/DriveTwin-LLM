import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\App.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

text = text.replace(
    "<PhysicsTelemetryCharts physicsSummary={physicsSummary} />",
    "<PhysicsTelemetryCharts physicsSummary={physicsSummary} mlPrediction={mlPred} />"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

