FROM python:latest
RUN pip install --no-cache-dir --upgrade pip



WORKDIR /user/app/src

COPY requirements.txt ./
COPY sensors.py ./
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./sensors.py" ]