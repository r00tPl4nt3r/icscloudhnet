import json
from flask import Flask
from flask import request as frequest
from urllib import request as urlrequest
from urllib.parse import quote as url_quote
app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>Hello from Flask & Docker</h2>'

'''
  "deployment_name": "FT9V",
  "public_ip_address": "public_ip_address",
  "token": "ABCDEF12345",
  "interface_id": "interface_id"
'''
@app.route('/deploy', methods=['POST'])
def deploy():
    try:
        #Save json from post
        deployment_name=frequest.json['deployment_name']
        interface_public_ip=frequest.json['public_ip_address']
        deployment_token=frequest.json['token']
        interface_id=frequest.json['interface_id']
        #send request to provisioner
        url = "http://provisioner:5000/deploy"
        req = urlrequest.Request(url)
        req.add_header('Content-Type', 'application/json; charset=utf-8')
        jsondata = urlrequest.json
        jsondata = json.dumps(jsondata)
        jsondataasbytes = jsondata.encode('utf-8')
        req.add_header('Content-Length', len(jsondataasbytes))
        response = urlrequest.urlopen(req, jsondataasbytes)
        #return response from provisioner
        return response
        
    except Exception as e:
        return str(e)


'''
    #Send request to provisioner
    url = "http://provisioner:5000/deploy"
    req = request.Request(url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = request.json
    jsondata = json.dumps(jsondata)
    jsondataasbytes = jsondata.encode('utf-8')
    req.add_header('Content-Length', len(jsondataasbytes))
    response = request.urlopen(req, jsondataasbytes)
    return response #Return response from provisioner
'''

if __name__ == "__main__":
    app.run(debug=True)
