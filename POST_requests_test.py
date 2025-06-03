import requests
import time

url = "https://808c-49-98-216-2.ngrok-free.app" #ngrokのURLを起動時に毎回入力する

requests.post(url=url, json={"contents": "this is the test message"})
print(requests.status_codes)