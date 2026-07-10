import json, urllib.request, urllib.error
login_url = 'http://127.0.0.1:8000/api/auth/login/'
chat_url = 'http://127.0.0.1:8000/api/ai/chat/'
creds = {'username':'admin','password':'admin123'}
req = urllib.request.Request(login_url, data=json.dumps(creds).encode(), headers={'Content-Type':'application/json'})
try:
    with urllib.request.urlopen(req, timeout=10) as r:
        login_resp = json.loads(r.read())
    access = login_resp.get('access')
    if not access:
        print('No access token')
    else:
        chat_payload = json.dumps({'message':'What blockers came up this week?'}).encode()
        chat_req = urllib.request.Request(chat_url, data=chat_payload, headers={'Content-Type':'application/json','Authorization':f'Bearer {access}'})
        try:
            with urllib.request.urlopen(chat_req, timeout=10) as cr:
                print('Chat response:', cr.read().decode())
        except urllib.error.HTTPError as he:
            print('Chat HTTPError:', he.code, he.read().decode())
        except Exception as e:
            print('Chat error:', e)
except Exception as e:
    print('Login error', e)
