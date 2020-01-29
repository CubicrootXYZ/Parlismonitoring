import requests, json


payload = {'searchstring': 'Migration'}
r = requests.get('http://127.0.0.1:8080/searchfiles', params=payload)

print(r.text)