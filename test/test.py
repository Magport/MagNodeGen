import requests
import json
import time
import hmac
import hashlib
import base64

# 配置
config_file = 'config.json'
api_keys_file = 'api_keys.json'

# 从文件读取 API key 和 secret
with open(api_keys_file, 'r') as f:
    api_keys = json.load(f)
    api_key = list(api_keys.keys())[0]
    secret = api_keys[api_key]['secret']

task_id = '8f401dc7b755d4c7150e01be835d3847'
url = 'http://127.0.0.1:8080/generate-code'

# 从文件读取配置数据
with open(config_file, 'r') as f:
    config = json.load(f)

# 构造请求数据
request_data = {
    'taskId': task_id,
    'config': config['config']
}
body = json.dumps(request_data)
method = 'POST'
path = '/generate-code'
timestamp = str(int(time.time()))

# 生成签名
def create_signature(secret, method, path, timestamp, body):
    message = f'{method}{path}{timestamp}{body}'
    return base64.urlsafe_b64encode(hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()).decode('utf-8')

signature = create_signature(secret, method, path, timestamp, body)

# 发送请求
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
