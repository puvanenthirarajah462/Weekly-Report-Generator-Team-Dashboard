import json, urllib.request, urllib.error
login_url = 'http://127.0.0.1:8000/api/auth/login/'
creds = {'username':'admin','password':'admin123'}
req = urllib.request.Request(login_url, data=json.dumps(creds).encode(), headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        login_resp = json.loads(r.read())
    access = login_resp.get('access')
    print('Got access token:', bool(access))
    print('Login response:', login_resp)
except urllib.error.HTTPError as e:
    print('Login HTTPError:', e.code, e.read().decode())
except Exception as e:
    print('Login error:', e)
