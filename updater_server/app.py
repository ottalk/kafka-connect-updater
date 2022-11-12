from flask import Flask,request,jsonify
import requests
import json

app = Flask(__name__)

@app.route('/')
def default():
    r=requests.get('http://localhost:8083')
    route_details="""CONNECT VERSION:"""+r.text+"""
FUNCTIONS:
/get_connectors  \t\t\t - list currently configured connectors
/get_connector_config/<connector>\t - print current configuration for supplied connector
/create_update_connectors\t\t - create/update connectors using configuration files

"""
    return route_details

@app.route('/get_connectors')
def get_connectors():
    r=requests.get('http://localhost:8083/connectors')
    return r.text

@app.route('/get_connector_config/<string:connector>')
def get_connector_details(connector):
    r=requests.get('http://localhost:8083/connectors/'+connector)
    return r.text

@app.route('/create_update_connectors', methods=['GET','POST'])
def create_update_connectors():
    # Get list of currently configured connectors
    connectors_list=requests.get('http://localhost:8083/connectors')
    print(connectors_list.text)
    #print(''.join(connectors_list))

    if request.method == "POST":
        config_files = request.files.getlist("config_files")
        print("#config_files="+str(len(config_files)))
        for config_file in config_files:
            print(config_file.filename)
            with open(config_file) as config_json_file:
                config_json = json.load(config_json_file)
                print(config_json)
    return "COMPLETED"

if __name__ == '__main__':
    app.run(debug=True,port=8088)
