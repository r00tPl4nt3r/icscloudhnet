FROM python:3.9-slim

RUN apt-get update 
RUN apt-get install -y wireguard
RUN apt-get install -y openresolv

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "app.py", "--host=0.0.0.0"]