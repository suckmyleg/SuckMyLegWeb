from requests import get
from socket import gethostbyname
from time import time
import sys
c = get(f"http://192.168.1.104:8080/Apis/HoneygainWorkers?c={sys.argv[1]}&devicename={sys.argv[2]}&time={int(time())}").content
print(c.decode("utf-8"))