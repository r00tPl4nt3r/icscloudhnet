import json
import base64

data = {}
with open('./data/00.jpg', mode='rb') as file:
    img = file.read()
data['data'] = "data:image/jpeg;base64,"+base64.encodebytes(img).decode('utf-8')

print(json.dumps(data))