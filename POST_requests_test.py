import requests
import time

url = "http://localhost:8080" #ローカルホストのテスト用
#url = "https://808c-49-98-216-2.ngrok-free.app" #ngrokのURLを起動時に毎回入力する

#テスト用のリクエスト
data ={
    "instrument": "USD/JPY",
    "units": "100",
    "side": "buy", 
    "type": "MARKET"
 }

requests.post(url=url, json=data)
#requests.post(url=url, json={"contents": "this is the test message"})
print(requests.status_codes)