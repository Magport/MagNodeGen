import requests
import json
import time
import hmac
import hashlib
import base64

config_file = 'config.json'
api_keys_file = 'api_keys.json'

with open(api_keys_file, 'r') as f:
    api_keys = json.load(f)
    api_key = list(api_keys.keys())[0]
    secret = api_keys[api_key]['secret']

task_id = '8f401dc7b755d4c7150e01be835d3848'
url = 'http://43.133.40.159:5001/generate-code'

with open(config_file, 'r') as f:
    config = json.load(f)

request_data = {
    'taskId': task_id,
    'config': config['config']
}
body = json.dumps(request_data)
method = 'POST'
path = '/generate-code'
timestamp = str(int(time.time()))

def create_signature(secret, method, path, timestamp, body):
    message = f'{method}{path}{timestamp}{body}'
    return base64.urlsafe_b64encode(hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()).decode('utf-8')

signature = create_signature(secret, method, path, timestamp, body)

headers = {
    'x-api-key': api_key,
    'x-signature': signature,
    'x-timestamp': timestamp,
    'Content-Type': 'application/json'
}

response = requests.post(url, headers=headers, data=body)

try:
    response_data = response.json()
except ValueError:
    response_data = response.text

print('Response:', response_data)
