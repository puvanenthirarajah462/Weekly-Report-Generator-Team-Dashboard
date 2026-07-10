import json, urllib.request
login_url = 'http://127.0.0.1:8000/api/auth/login/'
chat_url = 'http://127.0.0.1:8000/api/ai/chat/'
creds = {'username':'admin','password':'admin123'}

msgs = ['hello','hi','how are you','What blockers came up this week?','Show hours this week','who has blockers?','summarize']

req = urllib.request.Request(login_url, data=json.dumps(creds).encode(), headers={'Content-Type':'application/json'})
with urllib.request.urlopen(req, timeout=10) as r:
    access = json.loads(r.read()).get('access')

for m in msgs:
    payload = json.dumps({'message': m}).encode()
    req = urllib.request.Request(chat_url, data=payload, headers={'Content-Type':'application/json','Authorization':f'Bearer {access}'})
    with urllib.request.urlopen(req, timeout=10) as r:
        resp = json.loads(r.read())
    ans = resp.get('answer','')
    one_line = ' '.join(ans.splitlines())
    print(f"{m!r} -> {one_line}")
