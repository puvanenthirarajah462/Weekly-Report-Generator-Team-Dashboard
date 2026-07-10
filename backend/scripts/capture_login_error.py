import json, urllib.request, urllib.error
login_url = 'http://127.0.0.1:8000/api/auth/login/'
creds = {'username':'admin','password':'admin123'}
req = urllib.request.Request(login_url, data=json.dumps(creds).encode(), headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        print('OK', r.read().decode())
except urllib.error.HTTPError as e:
    body = e.read()
    try:
        print('HTTPError', e.code, body.decode())
    except Exception:
        print('HTTPError', e.code, body)
except Exception as e:
    print('Error', e)
