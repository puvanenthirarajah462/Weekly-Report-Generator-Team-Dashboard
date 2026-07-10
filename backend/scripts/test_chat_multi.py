import json, urllib.request, urllib.error
login_url = 'http://127.0.0.1:8000/api/auth/login/'
chat_url = 'http://127.0.0.1:8000/api/ai/chat/'
creds = {'username':'admin','password':'admin123'}

msgs = [
    'hello',
    'hi',
    'how are you',
    'What blockers came up this week?',
    'Show hours this week',
    'who has blockers?',
    'summarize'
]

# get token
req = urllib.request.Request(login_url, data=json.dumps(creds).encode(), headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        login_resp = json.loads(r.read())
    access = login_resp.get('access')
    if not access:
        print('Login failed:', login_resp)
        raise SystemExit(1)
except Exception as e:
    print('Login error', e)
    raise SystemExit(1)

for m in msgs:
    payload = json.dumps({'message': m}).encode()
    req = urllib.request.Request(chat_url, data=payload, headers={'Content-Type':'application/json','Authorization':f'Bearer {access}'})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            resp = r.read().decode()
        print('\nMessage:', m)
        print('Response:', resp)
    except urllib.error.HTTPError as e:
        print('\nMessage:', m)
        print('HTTPError', e.code, e.read().decode())
    except Exception as e:
        print('\nMessage:', m)
        print('Error', e)
