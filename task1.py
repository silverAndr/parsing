#!/usr/bin/env python
# coding: utf-8
import requests
import json
user_name = 'silverAndr'
print('Заголовки: \n',  req.headers)
print('Ответ: \n',  req.text)
data = json.loads(req.text)
with open('data.json', 'w') as fp:
    json.dump(data, fp)
print('Список репозиториев:\n')
for repo in data:
    print(repo['full_name'] + ' [' + str(repo['id']) + ']')
