# $curl -X POST -d "instrument=EUR_USD&units=2&side=sell&type=market" "http://api-sandbox.oanda.com/v1/accounts/12345/orders"をpython形式に変換

import requests

# APIのURL
url = "http://api-sandbox.oanda.com/v1/accounts/12345/orders"

# 送信するデータ（辞書型）
data = {
    "instrument": "EUR_USD",
    "units": "2",
    "side": "sell",
    "type": "market"
}

# POSTリクエストを送信
response = requests.post(url, data=data)

# レスポンスを表示
print(response.status_code)  # HTTPステータスコード(200なら成功)
print(response.text)  # サーバーからのレスポンスを取得

# 実行結果　サーバーが応答してない為エラーになる