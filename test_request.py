import requests
'''
auth_token='UhuiYI9VMw2hgNLTsDkxdJ3A8555syg4AGn8g5jvROo'
hed = {'Authorization': 'Bearer ' + auth_token}
data = {}

url = 'https://go.teachbase.ru/endpoint/v1/courses'
response = requests.get(url, json=data, headers=hed)
#print(response)
#print(response.json())
'''
from requests_oauthlib import OAuth1
url = 'https://go.teachbase.ru/endpoint/v1/courses'
auth = OAuth1('YOUR_APP_KEY', '8bdf8070ca5eb1ee7565aa4722e9772a60612310f62f0a04ba4774e7527c836b',
              'USER_OAUTH_TOKEN', 'c2c76197cc8de37d0d04a9cc4127ef7bb5c0961d4f96eeec6fff403e30b304dd')
print(auth)
response = requests.get(url, auth=auth)
print(response)
print(response.json())