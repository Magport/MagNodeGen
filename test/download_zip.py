import json
import time
import hmac
import hashlib
import base64
import requests

api_keys_file = 'api_keys.json'
task_id = '8f401dc7b755d4c7150e01be835d3847'
url = f'http://127.0.0.1:5000/task-status/{task_id}'

with open(api_keys_file, 'r') as f:
    api_keys = json.load(f)
    api_key = list(api_keys.keys())[0]
    secret = api_keys[api_key]['secret']

timestamp = str(int(time.time()))
method = 'GET'
path = f'/task-status/{task_id}'
body = ''

def create_signature(secret, method, path, timestamp, body):
    message = f'{method}{path}{timestamp}{body}'
    return base64.urlsafe_b64encode(hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()).decode('utf-8')

signature = create_signature(secret, method, path, timestamp, body)

headers = {
    'x-api-key': api_key,
    'x-signature': signature,
    'x-timestamp': timestamp
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    with open('task.zip', 'wb') as f:
        f.write(response.content)
    print('ZIP file downloaded successfully as task.zip')
else:
    print(f'Failed to download ZIP file: {response.status_code}')
    print(response.text)
