import json, urllib.request, urllib.error, time
login_url = 'http://127.0.0.1:8000/api/auth/login/'
creds = {'username':'admin','password':'admin123'}
for i in range(1,11):
    try:
        req = urllib.request.Request(login_url, data=json.dumps(creds).encode(), headers={'Content-Type':'application/json'})
        with urllib.request.urlopen(req, timeout=10) as r:
            print(i, 'OK', r.read().decode()[:120].replace('\n',' '))
    except urllib.error.HTTPError as e:
        body = e.read()
        try:
            print(i, 'HTTPError', e.code, body.decode()[:1000])
        except Exception:
            print(i, 'HTTPError', e.code, body)
    except Exception as e:
        print(i, 'Error', e)
    time.sleep(0.2)
