# magnet-node-generator

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

For more details on parameter configuration usage, please refer to [config_usage.md](https://github.com/toints/magnet-node-generator/blob/main/config_usage.md).


2. **Run the Python script**

   Execute the Python script to start the generate template code service:

   ```sh
   python main.py
   ```

3. **Test**

The test directory contains test cases for generating code and downloading compressed files.

`gen_code.py` includes test cases for generating code using templates.

`download_zip.py` contains test cases for downloading the compressed file of the code generated in the previous step to your local machine.

Before using the test cases, please call `/generate-key` to generate the apiKey and secret, and then add the apiKey information to the test cases.

For more usage of code generator, please refer to [generator_usage.md](https://github.com/toints/magnet-node-generator/blob/main/generator_usage.md).
