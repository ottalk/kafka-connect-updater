import requests
import glob

config_dir="./configs"

if __name__ == '__main__':
    config_file_list=glob.glob(config_dir+"/*.json")
    config_files=[eval(f'("config_files", open("{file}", "rb"))') for file in config_file_list ]
    print(config_files)
    update_response = requests.post("http://updater-server-entrypoint:8077/create_update_connectors",files=config_files)
    print("update_response="+update_response.text)