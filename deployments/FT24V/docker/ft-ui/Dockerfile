FROM nodered/node-red:1.0.4

COPY data/settings.js /usr/src/node-red/
COPY data/flows_IOTpi2.json /data/

RUN npm install --no-audit --no-update-notifier --no-fund --save --save-prefix=~ --production --engine-strict node-red-contrib-iiot-opcua@3.12.0
RUN npm install --no-audit --no-update-notifier --no-fund --save --save-prefix=~ --production --engine-strict node-red-dashboard@2.19.4