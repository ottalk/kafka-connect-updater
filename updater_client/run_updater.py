import requests
import glob
import json

config_dir="./configs"

if __name__ == '__main__':
    with open('./connectors_to_update.json') as f:
        connectors_to_update_json=f.read()
    config_file_list=glob.glob(config_dir+"/*.json")
    config_files=[eval(f'("config_files", open("{file}", "rb"))') for file in config_file_list ]
    print("connectors_to_update_file=",connectors_to_update_json)
    print("config_files",config_files)
    update_response = requests.post("http://updater-server-entrypoint:8077/create_update_connectors",data=json.loads(connectors_to_update_json),files=config_files)
    print("update_response="+update_response.text)