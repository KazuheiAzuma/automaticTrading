from oandapyV20.endpoints import orders, positions # オーダーとポジションのモジュールを取得
from oandapyV20 import API # class API()でサーバーと接続するクラスを取得
import datetime # Pythonの標準モジュール。日付や時間を扱う処理が可能になるモジュールを取得
import response_sample

class fx_trader: # FX取引を管理するためのクラス
    def __init__(self, account_id, access_token, instrument, environment="practice"):
    # account_id(Oanda口座ID),access_token(oanda APIアクセスキー),instrument(取引する通貨ペア),environment(使用する環境/デフォルトはpractice)
    
        self.instrument = instrument # 取引する通貨ペア(例：USD/JPY)
        self.account_id = account_id # FX口座ID(APIアクセス時に必要)
        self.access_token = access_token # Oanda　APIの認証キー
        self.log = [] # ログ(取引履歴など)を保存するためのリスト
        
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
        #self.r = positions.PositionDetails(accountID=self.account_id, instrument=self.instrument)
        #self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
        self.res = response_sample.positionRes #テスト用のレスポンス

        # ロングとショートの保有数を抽出
        self.longPositionUnits = int(self.res.get("position").get("long").get("units"))
        self.shortPositionUnits = int(self.res.get("position").get("short").get("units"))
        
        #　結果を表示
        print("longPositionUnits", self.longPositionUnits) # ロング保有数量
        print("shortPositionUnits", self.shortPositionUnits) # ショート保有数量
        
        return
 
        
    def order(self, instrument, unit, side, type): # 新規注文の関数
        if self.longPositionUnits == 0 and self.shortPositionUnits == 0: # ポジションが0で新規注文
            self.data = { # 新規注文の内容
            "order": {
                "instrument": instrument, # 取引通貨ペア(例：USD/JPY)
                "units": unit, # 注文するロット数
                "side": side, # 注文種類(buy or sell)
                "type": type, # 注文の種類(成行注文)
                "timeInForce": "FOK", # 成約条件("Fill-Or-Kill":即座に約定できない場合はキャンセル)
                "positionFill": "DEFAULT" #通常のポジション管理
            }
            }
            # 新規注文
            #self.r = orders.OrderCreate(accountID=self.account_id, data=self.data)
            #self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
            #デバッグするにはテスト用のレスポンスを作成すること！
            self.res = response_sample.orderSres
        
            # 新規注文のログを記録する
            self.logging("新規注文：約定価格{}、数量{}です".format(self.res.get("orderFillTransaction").get("price"), unit))
        
            return
 
           
    def close(self): # 決済注文の関数
        if self.longPositionUnits != 0: # ロングポジションが0でない場合、決済処理を実行
            data = {"longUnits": "ALL"} # ロング決済注文の内容
            
            # ロング決済注文
            self.r = positions.PositionClose(accountID=self.account_id, instrument=self.instrument, data=data)
            self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
            
            # ロング決済注文のログを記録する
            self.logging("ロング決済：約定価格{}数量{}、損益{}です".format(
                self.res.get("longOrderFillTransaction").get("price"), # 約定価格
                self.res.get("longOrderFillTransaction").get("units"), # 決済した数量
                self.res.get("longOrderFillTransaction").get("pl"), # (P/L)損益
            ))                                    
            
        if self.shortPositionUnits != 0: # ショートポジションが0でない場合、決済処理を実行
            data = {"shortUnits": "ALL"} # ショート決済注文の内容
            
            # ショート決済注文
            self.r = positions.PositionClose(accountID=self.account_id, instrument=self.instrument, data=data)
            self.res = self.client.request(self.r) # self.clientでAPIと接続し、requestで送信
            
            # ショート決済注文のログを記録する
            self.logging("ショート決済：約定価格{}数量{}、損益{}です".format(
                self.res.get("shortOrderFillTransaction").get("price"), # 約定価格
                self.res.get("shortOrderFillTransaction").get("units"), # 決済した数量
                self.res.get("shortOrderFillTransaction").get("pl"), # (P/L)損益
            ))
            
        return
