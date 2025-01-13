import requests
import json
import random
import time


while True:
    t = time.time()
    url = 'http://127.0.0.1:5000/host'
    print(t)
    response = requests.get(url)
    #print(response)
    r = response.json()
    response = r['data']
    # print(response)

    if time.time() - t == 5.0:
        timing = time.time()
        data = {"type": "invisible"}
        requests.post(url, json=data)
    # if time.time() - t >= 5.0:
    #     print("Post")
    #     t = time.time()
    #     data = {"type": "invisible"}
    #     res = requests.post(url, json=data)
    #     print(res)

    time.sleep(5)

#venv\Scripts\activate.bat


