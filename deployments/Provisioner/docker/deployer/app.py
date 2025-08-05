import subprocess
from flask import Flask
from flask import request as frequest
from urllib import request as urlrequest
from urllib.parse import quote as url_quote
app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>deployer say hallo!</h2>'


@app.route('/tofu', methods=['POST'])
def deploy():
    try:
        '''
        #Save json from post
        deployment_name = frequest.json['deployment_name']  # e.g. FT9V, FT24V
        local_network_address = frequest.json['local_network_address']
        tunnel_network_address = frequest.json['tunnel_network_address']
        tunnel_client_network_address = frequest.json['tunnel_client_network_address']
        tunnel_server_network_address = frequest.json['tunnel_server_network_address']
        client_port = frequest.json['client_port']
        server_port = frequest.json['server_port']
        server_url = frequest.json['server_url']
        associations = frequest.json['associations']
        '''

        # azure cli login
        subprocess.run(['az', 'login', '--service-principal', '-u', 'APP_ID', '-p', 'PASSWORD', '--tenant', 'TENANT_ID'])
        # tofu command to deploy honeynet: tofu apply -var-file="provisioner.tfvars"
        subprocess.run(['tofu', 'apply', '-var-file="provisioner.tfvars"'])
        

        response = {
            "status": "success",
            }      
        return response
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)

