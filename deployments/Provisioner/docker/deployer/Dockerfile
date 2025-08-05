FROM python:3.9-slim

RUN apt-get update 

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD [ "python3", "app.py", "--host=0.0.0.0"]