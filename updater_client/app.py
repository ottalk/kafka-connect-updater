from flask import Flask,request,jsonify
import requests
import glob
import json

config_dir="./configs"

app = Flask(__name__)

@app.route('/')
def default():
    r=requests.get('http://localhost:8083')
    route_details="""
FUNCTIONS:


"""
    return route_details

@app.route('/get_connectors')
def get_connectors():
    r=requests.get('http://localhost:8088/connectors')
    return r.text

@app.route('/get_connector_config/<string:connector>')
def get_connector_details(connector):
    r=requests.get('http://localhost:8088/connectors/'+connector)
    return r.text

@app.route('/create_update_connectors', methods=['GET','POST'])
def create_update_connectors():
    config_file_list=glob.glob(config_dir+"/*.json")
    config_files=[eval(f'("config_files", open("{file}", "rb"))') for file in config_file_list ]
    print(config_files)
    response = requests.post("http://localhost:8088/create_update_connectors",files=config_files)
    return response.text

if __name__ == '__main__':
    app.run(debug=True,port=8077)