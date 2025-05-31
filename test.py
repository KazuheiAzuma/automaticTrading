import http.server
import socketserver
from oandapyV20.endpoints import orders, positions
from oandapyV20 import API
import datetime
import config_p

# ---- fx_trader クラスの定義 ----
class fx_trader:
    def __init__(self, account_id, access_token, instrument="USD_JPY", environment="practice"):
        self.instrument = instrument
        self.account_id = account_id
        self.access_token = access_token
        self.log = []
        
        # OANDA API のクライアント作成
        self.client = API(access_token=access_token, environment=environment)

    def logging(self, text):
        logText = "[{}] {}".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), text)
        print(logText)
        self.log.append(logText)

    def order(self, unit):
        # 売買注文のデータを設定
        data = {
          "order": {
            "units": unit,
            "instrument": self.instrument,
            "timeInForce": "FOK",
            "type": "MARKET",
            "positionFill": "DEFAULT"
          }
        }
        
        # 売買注文を実行
        r = orders.OrderCreate(accountID=self.account_id, data=data)
        res = self.client.request(r)
        
        self.logging(f"New entry: {unit} at {res.get('orderFillTransaction').get('price')}")

    def positions(self):
        # 保有ポジションの取得
        r = positions.PositionDetails(accountID=self.account_id, instrument=self.instrument)
        res = self.client.request(r)
        
        # ポジション情報を取得
        self.longPositionUnits = int(res.get("position").get("long").get("units"))
        self.shortPositionUnits = int(res.get("position").get("short").get("units"))
        
        print(f"Long Position Units: {self.longPositionUnits}")
        print(f"Short Position Units: {self.shortPositionUnits}")

    def close(self):
        # ロングポジションを閉じる
        if self.longPositionUnits != 0:
            data = {"longUnits": "ALL"}
            r = positions.PositionClose(accountID=self.account_id, instrument=self.instrument, data=data)
            res = self.client.request(r)
            
            self.logging(f"Position closed: {res.get('longOrderFillTransaction').get('units')} at {res.get('longOrderFillTransaction').get('price')}")

        # ショートポジションを閉じる
        if self.shortPositionUnits != 0:
            data = {"shortUnits": "ALL"}
            r = positions.PositionClose(accountID=self.account_id, instrument=self.instrument, data=data)
            res = self.client.request(r)
            
            self.logging(f"Position closed: {res.get('shortOrderFillTransaction').get('units')} at {res.get('shortOrderFillTransaction').get('price')}")


# ---- WebhookHandler クラスの定義 ----
class WebhookHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        # データの抽出
        content_length = int(self.headers['content-length'])
        req_body = self.rfile.read(content_length).decode("utf-8")

        # 受信データから売買フラグを取得
        flag = int(req_body.split(" ")[-1])

        # ポジションの管理
        fx.positions()
        fx.close()

        # エントリー: 1ならロング、-1ならショート
        fx.order(unit * flag)

        # HTTP レスポンスを返す
        self.send_response(200)
        self.end_headers()


# ---- サーバーの起動 ----
unit = 100
account_id = "ACCOUNT_ID_P"
access_token = "ACCESS_TOKEN"

print("test")

fx = fx_trader(account_id=account_id, access_token=access_token, instrument="USD_JPY")

with socketserver.TCPServer(("", 3000), WebhookHandler) as httpd:
    print("Server is running on port 3000...")
    httpd.serve_forever()