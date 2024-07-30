import json
import subprocess
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, jsonify, abort
import uuid
import hmac
import hashlib
import base64
import functools
import time
import os
import shutil

app = Flask(__name__)

api_keys = {}
tasks = {}

def generate_api_key():
    return str(uuid.uuid4())

def generate_secret():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).rstrip(b'=').decode('utf-8')

def create_signature(secret, method, path, timestamp, body):
    message = f'{method}{path}{timestamp}{body}'
    return base64.urlsafe_b64encode(hmac.new(secret.encode(), message.encode(), hashlib.sha256).digest()).decode('utf-8')

def authenticate(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.headers.get('x-api-key')
        signature = request.headers.get('x-signature')
        timestamp = request.headers.get('x-timestamp')

        if not api_key or not signature or not timestamp:
            abort(401, description="Unauthorized: Missing API key, signature, or timestamp")

        if api_key not in api_keys:
            abort(401, description="Unauthorized: Invalid API key")

        secret = api_keys[api_key]['secret']
        method = request.method
        path = request.path
        body = request.get_data(as_text=True)
        expected_signature = create_signature(secret, method, path, timestamp, body)

        if not hmac.compare_digest(expected_signature, signature):
            abort(401, description="Unauthorized: Invalid signature")

        return func(*args, **kwargs)
    return wrapper

@app.route('/generate-key', methods=['POST'])
def generate_key():
    new_key = generate_api_key()
    new_secret = generate_secret()
    username = request.json.get('username')
    if not username:
        abort(400, description="Bad Request: Missing username")
    api_keys[new_key] = {'username': username, 'secret': new_secret}
    return jsonify({"api_key": new_key, "secret": new_secret})

@app.route('/test', methods=['GET'])
@authenticate
def secure_data():
    return jsonify({"data": "This is a test."})

@app.route('/generate-code', methods=['POST'])
@authenticate
def generate_code_endpoint():
    data = request.json
    config = data.get('config')
    task_id = data.get('taskId')

    if not config or not task_id:
        abort(400, description="Bad Request: Missing config or taskId")

    task_dir = os.path.join('tasks', task_id)
    os.makedirs(task_dir, exist_ok=True)

    config_path = os.path.join(task_dir, 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f)

    repo_url = 'https://github.com/Magport/Magnet.git'
    branch = 'features/genTemplate'
    dest_dir = os.path.join(task_dir, 'Magnet')

    clone_repo(repo_url, branch, dest_dir)
    generate_code(config_path, 'template/runtime_lib.template', os.path.join(dest_dir, 'runtime/src/lib.rs'))
    generate_code(config_path, 'template/chain_spec.template', os.path.join(dest_dir, 'node/src/chain_spec.rs'))
    generate_code(config_path, 'template/rpc_mod.template', os.path.join(dest_dir, 'node/src/rpc/mod.rs'))

    shutil.make_archive(task_dir, 'zip', task_dir)

    tasks[task_id] = {'status': 'completed', 'path': f'{task_dir}.zip'}
    return jsonify({'status': 'Task started', 'taskId': task_id})

@app.route('/task-status/<task_id>', methods=['GET'])
@authenticate
def task_status(task_id):
    task = tasks.get(task_id)
    if not task:
        abort(404, description="Not Found: Invalid taskId")
    return jsonify(task)

def clone_repo(repo_url, branch, dest_dir):
    try:
        subprocess.run(['git', 'clone', '-b', branch, repo_url, dest_dir], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")
        raise

def generate_code(json_file, template_file, output_file):
    with open(json_file, 'r') as f:
        config = json.load(f)

    env = Environment(loader=FileSystemLoader('./'))
    template = env.get_template(template_file)

    with open(output_file, 'w') as f:
        f.write(template.render(config=config))

if __name__ == "__main__":
    app.run(debug=True)

    #repo_url = 'https://github.com/Magport/Magnet.git'
    #branch = 'features/genTemplate'
    #dest_dir = 'Magnet'

    #clone_repo(repo_url, branch, dest_dir)

    #generate_code('config.json', 'template/runtime_lib.template', 'Magnet/runtime/src/lib.rs')
    #generate_code('config.json', 'template/chain_spec.template', 'Magnet/node/src/chain_spec.rs')
    #generate_code('config.json', 'template/rpc_mod.template', 'Magnet/node/src/rpc/mod.rs')
