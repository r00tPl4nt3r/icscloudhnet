import subprocess
import time


subprocess.Popen(["python3", "data/camsub.py"], shell=False)
subprocess.Popen(["python3", "data/sensor.py"], shell=False)
while True:
    time.sleep(60)