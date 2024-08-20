import json
import subprocess
from jinja2 import Environment, FileSystemLoader
from flask import Flask, request, jsonify, send_file
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
TASKS_FILE = 'tasks.json'
TASK_RETENTION_SECONDS = 7 * 24 * 60 * 60

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

def save_tasks():
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f)

def load_tasks():
    global tasks
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            tasks = json.load(f)
    else:
        tasks = {}

def clean_old_tasks():
    current_time = time.time()
    expired_tasks = []
    for task_id, task_info in tasks.items():
        if current_time - task_info['timestamp'] > TASK_RETENTION_SECONDS:
            expired_tasks.append(task_id)
            shutil.rmtree(os.path.dirname(task_info['path']), ignore_errors=True)

    for task_id in expired_tasks:
        del tasks[task_id]

    save_tasks()

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
            return jsonify({"success": False, "taskId": None, "message": "Unauthorized: Missing API key, signature, or timestamp"}), 401

        if api_key not in api_keys:
            return jsonify({"success": False, "taskId": None, "message": "Unauthorized: Invalid API key"}), 401

        secret = api_keys[api_key]['secret']
        method = request.method
        path = request.path
        body = request.get_data(as_text=True)
        expected_signature = create_signature(secret, method, path, timestamp, body)

        if not hmac.compare_digest(expected_signature, signature):
            return jsonify({"success": False, "taskId": None, "message": "Unauthorized: Invalid signature"}), 401

        return func(*args, **kwargs)
    return wrapper

@app.route('/generate-key', methods=['POST'])
def generate_key():
    new_key = generate_api_key()
    new_secret = generate_secret()
    username = request.json.get('username')
    if not username:
        return jsonify({"success": False, "taskId": None, "message": "Bad Request: Missing username"}), 400
    api_keys[new_key] = {'username': username, 'secret': new_secret}
    save_api_keys()
    return jsonify({"success": True, "taskId": None, "message": "", "data": {"api_key": new_key, "secret": new_secret}})

@app.route('/generate-code', methods=['POST'])
@authenticate
def generate_code_endpoint():
    data = request.json
    task_id = data.get('taskId')
    config = data.get('config')

    if not config or not task_id:
        return jsonify({"success": False, "taskId": None, "message": "Bad Request: Missing config or taskId"}), 400

    task_dir = os.path.join('tasks', task_id)
    os.makedirs(task_dir, exist_ok=True)

    config_path = os.path.join(task_dir, 'config.json')
    with open(config_path, 'w') as f:
        json.dump(config, f)

    repo_url = 'https://github.com/Magport/Magnet.git'
    branch = 'features/genTemplate'
    dest_dir = os.path.join(task_dir, 'Magnet')

    try:
        clone_repo(repo_url, branch, dest_dir)
        generate_code(config_path, 'template/runtime_lib.template', os.path.join(dest_dir, 'runtime/src/lib.rs'))
        generate_code(config_path, 'template/chain_spec.template', os.path.join(dest_dir, 'node/src/chain_spec.rs'))
        generate_code(config_path, 'template/rpc_mod.template', os.path.join(dest_dir, 'node/src/rpc/mod.rs'))

        subprocess.run(['cargo', '+stable', 'fmt', '--all'], cwd=dest_dir, check=True)

        zip_file_path = shutil.make_archive(task_dir, 'zip', task_dir)
        print(f'zip file path: {zip_file_path}')

        md5_hash = hashlib.md5()
        with open(zip_file_path, 'rb') as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                md5_hash.update(byte_block)
        zip_md5 = md5_hash.hexdigest()

        tasks[task_id] = {'status': 'completed', 'path': zip_file_path, 'timestamp': time.time(), 'md5': zip_md5}
        save_tasks()

        return jsonify({"success": True, "taskId": task_id, "message": "", "md5": zip_md5})
    except Exception as e:
        return jsonify({"success": False, "taskId": task_id, "message": str(e)}), 500

@app.route('/task-status/<task_id>', methods=['GET'])
@authenticate
def task_status(task_id):
    print(f'Checking status for task {task_id}')
    task = tasks.get(task_id)
    if not task:
        print(f'Task {task_id} not found in tasks')
        return jsonify({"success": False, "taskId": task_id, "message": "Not Found: Invalid taskId"}), 404

    if task['status'] == 'completed':
        zip_file_path = task['path']
        print(f'Task {task_id} completed, zip file path: {zip_file_path}')
        if os.path.exists(zip_file_path):
            return send_file(zip_file_path, as_attachment=True)
        else:
            print(f'ZIP file {zip_file_path} not found')
            return jsonify({"success": False, "taskId": task_id, "message": "Internal Server Error: ZIP file not found"}), 500

    return jsonify({"success": True, "taskId": task_id, "message": "Task is still in progress"})

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
    load_tasks()
    clean_old_tasks()
    app.run(host='0.0.0.0', port=5000, debug=True)
