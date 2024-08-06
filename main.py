import json
import subprocess
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, jsonify, abort, send_file
import uuid
import hmac
import hashlib
import base64
import functools
import time
import os
import shutil

app = Flask(__name__)

API_KEYS_FILE = 'api_keys.json'

api_keys = {}
tasks = {}

def save_api_keys():
    with open(API_KEYS_FILE, 'w') as f:
        json.dump(api_keys, f)

def load_api_keys():
    global api_keys
    if os.path.exists(API_KEYS_FILE):
        with open(API_KEYS_FILE, 'r') as f:
            api_keys = json.load(f)
    else:
        api_keys = {}

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
    save_api_keys()
    return jsonify({"api_key": new_key, "secret": new_secret})

@app.route('/generate-code', methods=['POST'])
@authenticate
def generate_code_endpoint():
    data = request.json
    task_id = data.get('taskId')
    config = data.get('config')

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

    zip_file_path = shutil.make_archive(task_dir, 'zip', task_dir)

    tasks[task_id] = {'status': 'completed', 'path': zip_file_path}
    print(f'Task {task_id} completed, zip file path: {tasks[task_id]["path"]}')
    return jsonify({'status': 'Task started', 'taskId': task_id})

@app.route('/task-status/<task_id>', methods=['GET'])
@authenticate
def task_status(task_id):
    print(f'Checking status for task {task_id}')
    task = tasks.get(task_id)
    if not task:
        print(f'Task {task_id} not found in tasks')
        abort(404, description="Not Found: Invalid taskId")

    if task['status'] == 'completed':
        zip_file_path = task['path']
        print(f'Task {task_id} completed, zip file path: {zip_file_path}')
        if os.path.exists(zip_file_path):
            return send_file(zip_file_path, as_attachment=True)
        else:
            print(f'ZIP file {zip_file_path} not found')
            abort(500, description="Internal Server Error: ZIP file not found")

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
    load_api_keys()
    app.run(host='0.0.0.0', port=5000, debug=True)
