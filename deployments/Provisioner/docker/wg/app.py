import subprocess
from flask import Flask
from flask import request as frequest
from urllib import request as urlrequest
from urllib.parse import quote as url_quote
app = Flask(__name__)

@app.route('/')
def hello_geek():
    return '<h1>wg say hallo!</h2>'


@app.route('/keychain', methods=['POST'])
def deploy():
    try:
        #Save json from post
        #create wg key pair (run wg genkey | tee /etc/wireguard/client_id.deployment_id.key | wg pubkey | tee /etc/wireguard/public.key)
        private_key = subprocess.run(['wg', 'genkey'], stdout=subprocess.PIPE)
        private_key = private_key.stdout.decode('utf-8').split('\n')[0]
        public_key = subprocess.run(["wg", "pubkey"], input=private_key.encode('utf-8'), stdout=subprocess.PIPE)
        public_key = public_key.stdout.decode('utf-8').split('\n')[0]
        #return public keys to client in format {"private_key": "private_key", "public_key": "public_key"} as json
        response = {
            "private_key": private_key,
            "public_key": public_key 
            }      
        return response
    except Exception as e:
        return str(e)


if __name__ == "__main__":
    app.run(debug=True)
