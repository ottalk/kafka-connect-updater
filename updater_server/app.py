from flask import Flask, request, jsonify
import requests
import json
from logging.config import dictConfig

headers = {
    'Content-Type': 'application/json'
}

dictConfig(
    {
        "version": 1,
        "formatters": {
            "default": {
                "format": "[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
            }
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "formatter": "default",
            }
        },
        "root": {"level": "DEBUG", "handlers": ["console"]},
    }
)

app = Flask(__name__)


@app.route('/')
def default():
    r = requests.get('http://connect:8083')
    route_details = """CONNECT VERSION:"""+r.text+"""
FUNCTIONS:
/get_connectors  \t\t\t - list currently configured connectors
/get_connector_config/<connector>\t - print current configuration for supplied connector
/create_update_connectors\t\t - create/update connectors using configuration files

"""
    return route_details


@app.route('/get_connectors')
def get_connectors():
    r = requests.get('http://connect:8083/connectors')
    return r.text


@app.route('/get_connector_config/<string:connector>')
def get_connector_details(connector):
    r = requests.get('http://connect:8083/connectors/'+connector)
    return r.text


@app.route('/create_update_connectors', methods=['GET', 'POST'])
def create_update_connectors():
    # Get list of currently configured connectors
    connectors_list = requests.get('http://connect:8083/connectors')
    app.logger.debug(connectors_list.text)

    if request.method == "POST":
        #app.logger.debug("request="+str(request.environ))
        req = request.form
        app.logger.debug("req="+str(req['connectors_to_update']))
        connectors_to_update_list=req['connectors_to_update'].split(',')
        #connectors_to_update_list=['mm2-cluster']
        app.logger.debug("connectors_to_update_list="+str(connectors_to_update_list))
        config_files = request.files.getlist("config_files")
        app.logger.info("no_of_config_files="+str(len(config_files)))
        for config_file in config_files:
            config = config_file.filename.split(".")[0]
            app.logger.debug("config="+config)
            if config in connectors_to_update_list:
                config_json = json.load(config_file)
                app.logger.debug("config file name="+config_file.filename)         
                if config in connectors_list.text:
                    app.logger.debug("PUT")
                    put_config_json = config_json['config']
                    app.logger.debug(put_config_json)
                    put_response = requests.put('http://connect:8083/connectors/'+config+'/config', headers=headers, json=put_config_json)
                    app.logger.debug("PUT_RESPONSE="+put_response.text)
                else:
                    app.logger.debug("POST")
                    app.logger.debug(config_json)
                    post_response = requests.post('http://connect:8083/connectors', headers=headers, json=config_json)
                    app.logger.debug("POST_RESPONSE="+post_response.text)

    return "COMPLETED\n"


if __name__ == '__main__':
    app.run(debug=True, port=8077)
