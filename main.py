import json
import subprocess
from jinja2 import Environment, FileSystemLoader

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
    repo_url = 'https://github.com/Magport/Magnet.git'
    branch = 'main-develop'
    dest_dir = 'Magnet'

    clone_repo(repo_url, branch, dest_dir)

    generate_code('config.json', 'template/runtime_lib.template', 'Magnet/runtime/src/lib.rs')
    generate_code('config.json', 'template/chain_spec.template', 'Magnet/node/src/chain_spec.rs')
    generate_code('config.json', 'template/rpc_mod.template', 'Magnet/node/src/rpc/mod.rs')
