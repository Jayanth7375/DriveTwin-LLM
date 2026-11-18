import os

filepath = r"C:\Users\Jayanth\Downloads\DRIVE-TWIN\Drive-Twin\backend\app\api\routes_analyze.py"
with open(filepath, 'r', encoding='utf-8') as f:
    text = f.read()

bad_upload = """        content = await file.read()
        filename = file.filename.lower()
        
        if filename.endswith(".csv"):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(io.BytesIO(content))"""

good_upload = """        filename = file.filename.lower()
        
        # Safe loading for massive files (like 1GB)
        if filename.endswith(".csv"):
            df = pd.read_csv(file.file, nrows=5000)
        elif filename.endswith(".xlsx") or filename.endswith(".xls"):
            df = pd.read_excel(file.file, nrows=5000)"""

text = text.replace(bad_upload, good_upload)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(text)

