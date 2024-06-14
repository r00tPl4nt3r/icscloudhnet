cd deployments/FT9V/docker
docker image build ./ft-sensor/ -t ft/ft-sensor 
docker image build ./ft-ui/ -t ft/ft-ui 
cd deployments/FT24V/docker
docker image build ./ft-ui/ -t ft/ft-ui-opcua
docker image build ./opcua-plc -t plc/opcua