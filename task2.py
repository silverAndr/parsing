#!/usr/bin/env python
# coding: utf-8
import requests
import json
api_key = 'd65a6b79349acbfdd33e86ca5b130d78937b917b'
inn = '7707083893'
res_company = requests.post('https://suggestions.dadata.ru/suggestions/api/4_1/rs/findById/party',
            data=json.dumps({'query': inn}),
             headers={
                 'Content-Type': 'application/json',
                 'Accept': 'application/json',
                 'Authorization': f"Token {api_key}"
             })
res_company
data = json.loads(res_company.text)
with open('dadata.json', 'w') as fp:
    json.dump(data, fp)
