FROM python:latest
RUN pip install --no-cache-dir --upgrade pip



WORKDIR /user/app/src

COPY requirements.txt ./
COPY *.py ./
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir data


CMD [ "python", "./spawner.py" ]