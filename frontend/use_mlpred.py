import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\frontend\src\components\PhysicsTelemetryCharts.jsx"

with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_def = "export default function PhysicsTelemetryCharts({ physicsSummary }) {"
good_def = "export default function PhysicsTelemetryCharts({ physicsSummary, mlPrediction }) {"
text = text.replace(bad_def, good_def)

bad_calc = "const consistencyScore = Math.max(0, 100 - (Math.abs(mafRes) * 100) - (Math.abs(bankDelta) * 10) - (sfi));"
good_calc = "const consistencyScore = mlPrediction?.confidence ? (mlPrediction.confidence * 100) : 87;"
text = text.replace(bad_calc, good_calc)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

