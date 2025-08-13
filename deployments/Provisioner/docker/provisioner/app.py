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
        deployment_name=frequest.json['deployment_name'] #e.g. FT9V, FT24V
        deployment_type=frequest.json['deployment_type'] #e.g. "cloud", "on-premises"
        
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

       
        #Define network address and port
        tunnel_network_address = "10."+str(random.randint(0,255))+"."+str(random.randint(0,255))+".0/24"
        tunnel_network_prefix = tunnel_network_address.split("/")[0]
        tunnel_network_prefix = tunnel_network_prefix.split(".")
        tunnel_network_prefix = tunnel_network_prefix[0]+"."+tunnel_network_prefix[1]+"."+tunnel_network_prefix[2]
        tunnel_server_network_address = tunnel_network_prefix+".254/24"
        tunnel_client_network_address = tunnel_network_prefix+".1/24"
        honeynet_network_address = "172.17.0.0/24"
        honeynet_network_prefix = honeynet_network_address.split("/")[0]
        honeynet_network_prefix = honeynet_network_prefix.split(".")
        honeynet_network_prefix = honeynet_network_prefix[0]+"."+honeynet_network_prefix[1]+"."+honeynet_network_prefix[2]
        honeynet_network_address = honeynet_network_address.split("/")[0]
        honeynet_network_address = honeynet_network_address.split(".")
        honeynet_network_address = honeynet_network_address[0]+"."+honeynet_network_address[1]+"."+honeynet_network_address[2]
        client_port = random.randint(29000,29999)
        server_port = random.randint(29000,29999)
        
        if deployment_name  == "FT9V":
            associations = {
                "mqtt_server": honeynet_network_address.split("/")[0]+".5",
                "hmi": honeynet_network_address.split("/")[0]+".10",      
                }
            server_url = "ft9v.westeurope.cloudapp.azure.com"
        elif deployment_name == "FT24V":
            associations = {
                "mqtt_server": honeynet_network_address.split("/")[0]+".5",
                "hmi": honeynet_network_address.split("/")[0]+".10",
                "opcua_server": honeynet_network_address.split("/")[0]+".15",
            }
            server_url = "ft24v.westeurope.cloudapp.azure.com"

        #return response to client
        if deployment_type == "cloud":
            response = {
                "deployment_name": deployment_name,
                "client_keys": client_keys,
                "server_public_key": server_keys["public_key"],
                "tunnel_client_network_address": tunnel_client_network_address,
                "tunnel_server_network_address": tunnel_server_network_address,
                "client_port": client_port,
                "server_port": server_port, 
                "server_url": server_url,
                "associations": associations,
            }
        elif deployment_type == "on-premises":
            response = {
                "deployment_name": deployment_name,
                "client_keys": client_keys,
                "server_keys": server_keys,
                "tunnel_client_network_address": tunnel_client_network_address,
                "tunnel_server_network_address": tunnel_server_network_address,
                "client_port": client_port,
                "server_port": server_port, 
                "server_url": server_url,
                "associations": associations,
            }


        return response
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
