from flask import Flask,request,jsonify
import requests

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
    if request.method == "POST":
        files = request.files.getlist("file")
        for file in files:
            print(file.filename)
    return 'FILES='.join(files)

if __name__ == '__main__':
    app.run(debug=True,port=8088)
