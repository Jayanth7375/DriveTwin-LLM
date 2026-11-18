import requests

try:
    res = requests.get('http://127.0.0.1:8000/api/ecu-live/ports')
    print("Status:", res.status_code)
    print("Body:", res.text.encode('utf-8'))
except Exception as e:
    print(e)

