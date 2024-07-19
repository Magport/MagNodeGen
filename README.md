# magnet-node-generator
generate magnet parachain by config

Magnet Template Code Generator  process of downloading the Magnet repository from GitHub and generating template code for magnet files based on the `config.json` file.

## Prerequisites

Before you start, ensure you have the following installed:
- [Git](https://git-scm.com/)
- [Python 3](https://www.python.org/)
- [Jinja2](https://pypi.org/project/Jinja2/) (`pip install jinja2`)

## Steps

1. **Modify the `config.json` file**

   Modify `config.json` file with your specific configurations. Example content:

   ```json
   {
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
   }
   ```

2. **Run the Python script**

   Execute the Python script to generate the template code:

   ```sh
   python main.py
   ```
