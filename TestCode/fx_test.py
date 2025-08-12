from oandapyV20.endpoints import orders, positions # オーダーとポジションのモジュールを取得
from oandapyV20.exceptions import V20Error
from oandapyV20 import API # class API()でサーバーと接続するクラスを取得
import datetime # Pythonの標準モジュール。日付や時間を扱う処理が可能になるモジュールを取得
import response_sample

class fx_trader: # FX取引を管理するためのクラス
    def __init__(self, account_id, access_token, instrument, environment="practice", debug=False):
    # account_id(Oanda口座ID),access_token(oanda APIアクセスキー),instrument(取引する通貨ペア),environment(使用する環境/デフォルトはpractice)
    
        self.instrument = instrument # 取引する通貨ペア(例：USD/JPY)
        self.account_id = account_id # FX口座ID(APIアクセス時に必要)
        self.access_token = access_token # Oanda　APIの認証キー
        self.log = [] # ログ(取引履歴など)を保存するためのリスト
        self.debug = debug
        
        # API用のクラスを定義し、Oanda APIとの接続を作成
        self.client = API(access_token=access_token, environment=environment)
 
    
    def logging(self, text): # ログを記録する関数
        # 現在の日付と時刻を取得
        logText = "[{}] {}".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), text)
        # now()で日時時刻を取得、strftime()でフォーマットを整え、textにする
        
        print(logText) # logtextをコンソールに出力する
        self.log.append(logText) # ログリストに、logTextを保存する
        
        return
 
    
    def positions(self): # 保有ポジション取得の関数
        # 保有ポジションを取得
        self.logging("■■■ポジション取得処理 start")
        
        try:
            # if self.debug:
            #     self.logging("positions(): デモ口座を使用")
            #     self.r = positions.PositionDetails(accountID=self.account_id, instrument=self.instrument)
            #     self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
            #     long_unit = int(self.res.get("position").get("long").get("units"))
            #     short_unit = int(self.res.get("position").get("short").get("units"))
            # else:
            #     self.logging("positions(): 本番口座を使用")
            #self.res = response_sample.positionRes #テスト用のレスポンス
            
            self.r = positions.PositionDetails(accountID=self.account_id, instrument=self.instrument)
            self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
            long_unit = int(self.res.get("position").get("long").get("units"))
            short_unit = int(self.res.get("position").get("short").get("units"))

        except Exception as e:
            self.logging("保有ポジションなし")
            long_unit = 0
            short_unit = 0

        # ロングとショートの保有数を抽出
        self.longPositionUnits = long_unit
        self.shortPositionUnits = short_unit
        
        #　結果を表示
        self.logging("longPositionUnits：{}".format(self.longPositionUnits)) # ロング保有数量
        self.logging("shortPositionUnits：{}".format(self.shortPositionUnits)) # ショート保有数量
        
        self.logging("■■■ポジション取得処理 end")
        return
 
    def order(self, instrument, unit, side, type): # 新規注文の関数
        if self.longPositionUnits == 0 and self.shortPositionUnits == 0: # ポジションが0で新規注文
            self.logging("■■■新規注文処理 start")

            self.data = { # 新規注文の内容
            "order": {
                "instrument": instrument, # 取引通貨ペア(例：USD/JPY)
                "units": unit, # 注文する通貨
                "side": side, # 注文種類(buy or sell)
                "type": "MARKET", # 注文の種類(成行注文)
                "timeInForce": "FOK", # 成約条件("Fill-Or-Kill":即座に約定できない場合はキャンセル)
                "positionFill": "DEFAULT" #通常のポジション管理
            }
            }
            # 新規注文
            self.r = orders.OrderCreate(accountID=self.account_id, data=self.data)
            self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
            self.logging("レスポンス{}".format(self.res))
        
            if "orderFillTransaction" in self.res:
                # 注文成功
                self.logging("新規注文：約定価格{}、数量{}です".format(self.res.get("orderFillTransaction").get("price"), unit))

            elif "orderCancelTransaction" in self.res:
                # 注文キャンセル
                self.logging("注文キャンセル：{}".format(self.res.get("orderCancelTransaction").get("reason")))
        
            self.logging("■■■新規注文処理 end")
        return
 
           
    def close(self): # 決済注文の関数
        if self.longPositionUnits != 0: # ロングポジションが0でない場合、決済処理を実行
            self.logging("■■■ロング決済注文処理 start")
            data = {"longUnits": "ALL"} # ロング決済注文の内容
            
            # ロング決済注文
            self.r = positions.PositionClose(accountID=self.account_id, instrument=self.instrument, data=data)
            self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
            #self.res = response_sample.closeLongRes #テスト用のレスポンス
            self.logging("レスポンス{}".format(self.res))

            # ロング決済注文のログを記録する
            self.logging("ロング決済：約定価格{}数量{}、損益{}です".format(
                self.res.get("longOrderFillTransaction").get("price"), # 約定価格
                self.res.get("longOrderFillTransaction").get("units"), # 決済した数量
                self.res.get("longOrderFillTransaction").get("pl"), # (P/L)損益
            ))

            self.logging("■■■ロング決済注文処理 end")                              
            
        if self.shortPositionUnits != 0: # ショートポジションが0でない場合、決済処理を実行
            self.logging("■■■ショート決済注文処理 start")
            data = {"shortUnits": "ALL"} # ショート決済注文の内容
            
            # ショート決済注文
            self.r = positions.PositionClose(accountID=self.account_id, instrument=self.instrument, data=data)
            self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
            #self.res = response_sample.closeLongRes #テスト用のレスポンス
            self.logging("レスポンス{}".format(self.res))
            
            # ショート決済注文のログを記録する
            self.logging("ショート決済：約定価格{}数量{}、損益{}です".format(
                self.res.get("shortOrderFillTransaction").get("price"), # 約定価格
                self.res.get("shortOrderFillTransaction").get("units"), # 決済した数量
                self.res.get("shortOrderFillTransaction").get("pl"), # (P/L)損益
            ))

            self.logging("■■■ショート決済注文処理 end")
            
        return
