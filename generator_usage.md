# 客户端使用教程

## 1. 生成apiKey和secret

通过 HTTP POST请求:

```shell
curl -X POST http://127.0.0.1:5000/generate-key -H "Content-Type: application/json" -d '{"username": "testuser"}'
```

响应数据:

```shell
{
    "api_key": "generated-api-key",
    "secret": "generated-secret"
}
```

## 2. 使用apiKey和secret签名请求并发送请求

使用`HMAC`算法进行签名， nodejs实例：

```javascript
const crypto = require('crypto');
const axios = require('axios');

// 生成签名
function createSignature(secret, method, path, timestamp, body) {
    const message = `${method}${path}${timestamp}${body}`;
    return crypto.createHmac('sha256', secret).update(message).digest('base64url');
}

const apiKey = 'your_api_key';
const secret = 'your_secret';
const method = 'POST';
const path = '/generate-code';
const timestamp = Math.floor(Date.now() / 1000).toString();

const config =    {
    "pallet_frame_system": {
        "index": 0,
        "optional": false,
        "parameter": {
            "RuntimeVersion": {
                "spec_name": "magnet-parachain",
                "impl_name": "magnet-parachain",
                "authoring_version": 1,
                "spec_version": 1,
                "impl_version": 0,
                "apis": "RUNTIME_API_VERSIONS",
                "transaction_version": 1,
                "state_version": 1
            },
            "RuntimeBlockLength": "5 * 1024 * 1024",
            "SS58Prefix": 42
        },
        "chain_spec": {},
        "rpc_mod": {}
    },
    ...
};

const body = JSON.stringify({ config, taskId: 'your_task_id' });
const signature = createSignature(secret, method, path, timestamp, body);

axios.post('http://127.0.0.1:5000/generate-code', body, {
    headers: {
        'x-api-key': apiKey,
        'x-signature': signature,
        'x-timestamp': timestamp,
        'Content-Type': 'application/json'
    }
})
    .then(response => {
        console.log('Response:', response.data);
    })
    .catch(error => {
        console.error('Error:', error.response ? error.response.data : error.message);
    });
```

## 3. 使用taskId请求任务进度并下载

发送HTTP GET请求下载生成的模板压缩文件:
```shell
curl -H "x-api-key: your_api_key_here" \
     -H "x-signature: your_signature_here" \
     -H "x-timestamp: your_timestamp_here" \
     http://127.0.0.1:5000/task-status/your_task_id --output task.zip
```
