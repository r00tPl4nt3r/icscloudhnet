import json
import random
from flask import Flask
from flask import request as frequest
from urllib import request as urlrequest
from urllib.parse import quote as url_quote
app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>Provisioner say Hallo!</h2>'

@app.route('/provisioner', methods=['POST'])
def deploy():
    try:
        #Save json from post
        deployment_name=frequest.json['deployment_name']
        interface_public_ip=frequest.json['public_ip_address']
        local_network_address=frequest.json['local_network_address']
        deployment_token=frequest.json['token']
        
        #request pub-private key pair from wg-key-server
        url = "http://wg:5000/keychain"
        post_data = {
        }
        req = urlrequest.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = json.dumps(post_data)
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        client_keys = urlrequest.urlopen(req, jsondataasbytes)
        client_keys = json.loads(client_keys.read())
        server_keys = urlrequest.urlopen(req, jsondataasbytes)
        server_keys = json.loads(server_keys.read())

        local_network_prefix = local_network_address.split("/")[0]
        local_network_prefix = local_network_prefix.split(".")
        local_network_prefix = local_network_prefix[0]+"."+local_network_prefix[1]+"."+local_network_prefix[2]
        
        #Define network address and port
        remote_network_address = "10."+str(random.randint(0,255))+"."+str(random.randint(0,255))+".254/24"
        honeynet_network_address = "172.17.1.0/24"
        honeynet_network_address = honeynet_network_address.split("/")[0]
        honeynet_network_address = honeynet_network_address.split(".")
        honeynet_network_address = honeynet_network_address[0]+"."+honeynet_network_address[1]+"."+honeynet_network_address[2]
        client_port = random.randint(29000,29999)
        server_port = random.randint(29000,29999)
        if deployment_name  == "FT9V":
            associations = {
                local_network_prefix+".20:22": honeynet_network_address.split("/")[0]+".10:2522",
                local_network_prefix+".25:22": honeynet_network_address.split("/")[0]+".5:2022",
                local_network_prefix+".20:80": honeynet_network_address.split("/")[0]+".10:80",
                local_network_prefix+".25:5555": honeynet_network_address.split("/")[0]+".5:5555",
            }
        elif deployment_name == "FT24V":
            associations = {
                local_network_prefix+".100:22": honeynet_network_address.split("/")[0]+".10:2522",
                local_network_prefix+".101:22": honeynet_network_address.split("/")[0]+".5:2022",
                local_network_prefix+".100:1880": honeynet_network_address.split("/")[0]+".10:1880",
                local_network_prefix+".101:4840": honeynet_network_address.split("/")[0]+".5:4840",
            }
             
        
        #return response to client
        response = {
            "deployment_name": deployment_name,
            "deployment_token": deployment_token,
            "client_keys": client_keys,
            "server_keys": server_keys,
            "remote_network_address": remote_network_address,
            "client_port": client_port,
            "server_port": server_port, 
            "associations": associations,
            "client_public_ip": interface_public_ip,
            "local_network_address": local_network_address
        }

        return response
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
