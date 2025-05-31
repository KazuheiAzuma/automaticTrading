from oandapyV20.endpoints import orders, positions # APIリクエストを管理するためのモジュールから、オーダーとポジションに関する機能を取得
from oandapyV20 import API # OandaのAPIと直接通信するためのクラス(サーバーとデータのやり取りができる。)
import datetime # Pythonの標準モジュール。日付や時間を扱う処理が可能になる


class fx_trader: # FX取引を管理するためのクラス。取引に必要な(APIキーや口座IDなど)を保持し、注文やポジション管理を行う為の処理をまとめる。
    def __init__(self, account_id, access_token, instrument="USD_JPY", environment="practice"):
    # コンストラクタで、クラスのインスタンスを作成
    # account_id(Oanda口座ID),access_token(oanda APIアクセスキー),instrument(取引する通貨ペア),environment(使用する環境/デフォルトはpractice)
    
        # (self.変数名)はクラス内で保持する情報(インスタンス変数)
        self.instrument = instrument # 取引する通貨ペア(例：USD/JPY)
        self.account_id = account_id # FX口座ID(APIアクセス時に必要)
        self.access_token = access_token # Oanda　APIの認証キー
        self.log = [] # ログ(取引履歴など)を保存するためのリスト
        
        # API用のクラスを定義し、Oanda APIとの接続を作成
        self.client = API(access_token=access_token, environment=environment) # API(Oanda APIの認証キー,(練習環境ならpractice、本番環境ならlive))
    
    def logging(self, text): # このメソッドはログを記録する
        # datetime.datetime.now()で現在の日付と時刻を取得、strftime("%Y/%m/%d %H:%M:%S")で日時のフォーマットに変換、textは受け取ったログメッセージを日時に組み合わせる
        logText = "[{}] {}".format(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S"), text)
        print(logText) # logtextをコンソールに出力する、これによりリアルタイムでログの内容が確認できる
        self.log.append(logText) # ログを保存するリストに、logTextをログリストに追加する
        
        return # 戻り値がなく、Noneを返すだけなので、書かなくても問題はない
        
    def order(self, unit): # order(self, unit)はAPIでFXの売買注文を行うための処理
        # 売買注文の内容を設定
        self.data = {
          "order": {
            "units": unit, # 注文するロット数
            "instrument": self.instrument, # 取引通貨ペア(例：USD/JPY)
            "timeInForce": "FOK", # 成約条件("Fill-Or-Kill":即座に約定できない場合はキャンセル)
            "type": "MARKET", # 注文の種類(成行注文)
            "positionFill": "DEFAULT" #通常のポジション管理
          }
        }
        # 売買注文
        self.r = orders.OrderCreate(accountID=self.account_id, data=self.data) # エンドポイントを呼び出し、注文を作成
        self.res = self.client.request(self.r) # self.client(API接続オブジェクト)で注文リクエストを送信
        
        # self.logging()はloggingメソッドを使用し、「何枚の注文を、どの価格で約定したか」をログに記録
        # self.res.get("orderFillTransaction").get("price")はAPIのレスポンスから約定価格を取得
        # ログには　"new entry: {ロット数} at {約定価格}" と記録が残る
        self.logging("new entry: {} at {}".format(unit, self.res.get("orderFillTransaction").get("price")))
        return # 戻り値が指定されていないため、何も返さずメソッドを終了する
    
    def positions(self): # position(self)はAPIで現在の保有ポジションを取得し、ロングとショートの保有数を抽出・表示する処理
        # 保有ポジションを取得
        # 特定の通貨ペアのポジション詳細を取得するAPIリクエストを作成
        self.r = positions.PositionDetails(accountID=self.account_id, instrument=self.instrument)
        # self.clientでAPIリクエストを送信し、レスポンスをself.resに保存
        self.res = self.client.request(self.r)
        
        # ロングとショートの保有数を抽出
        # self.res.getでポジションデータを取得、ロングポジションデータ、保有数量を取得
        self.longPositionUnits = int(self.res.get("position").get("long").get("units"))
        # self.res.getでポジションデータを取得、ショートポジションデータ、保有数量を取得
        self.shortPositionUnits = int(self.res.get("position").get("short").get("units"))
        
        #　結果を表示
        print("longPositionUnits", self.longPositionUnits) # ロングポジションの保有数量を表示
        print("shortPositionUnits", self.shortPositionUnits) # ショートポジションの保有数量を表示
        
        return # 戻り値が指定されていないため、何も返さずメソッドを終了する
    
    def close(self): # close(self)はAPIで現在のポジションを決済するための処理
        # ポジションをクローズ
        if self.longPositionUnits != 0: # 現在のロングポジションが0でない場合、決済処理を実行
            data = {"longUnits": "ALL"} # 保有するすべてのロングポジションを決済する設定
            # positions.PositionClose()でAPIにポジションを閉じるリクエストを作成
            self.r = positions.PositionClose(accountID=self.account_id, instrument=self.instrument, data=data)
            # self.clientでAPIリクエストを送信し、レスポンスをself.resに保存
            self.res = self.client.request(self.r)
            
            # ロングポジションの決済結果を記録
            self.logging("position close: {} at {}. pl: {}".format(
                self.res.get("longOrderFillTransaction").get("units"), # 決済した数量
                self.res.get("longOrderFillTransaction").get("price"), # 約定価格
                self.res.get("longOrderFillTransaction").get("pl"), # (P/L)損益
            )) # 結果は position close: {数量} at {約定価格}. pl: {損益}　と表示される
            
        if self.shortPositionUnits != 0: # 現在のショートポジションが0でない場合、決済処理を実行
            data = {"shortUnits": "ALL"} # 保有するすべてのショートポジションを決済する設定
            # positions.PositionClose()でAPIにポジションを閉じるリクエストを作成
            self.r = positions.PositionClose(accountID=self.account_id, instrument=self.instrument, data=data)
            # self.clientでAPIリクエストを送信し、レスポンスをself.resに保存
            self.res = self.client.request(self.r)
            
            self.logging("position close: {} at {}. pl: {}".format(
                self.res.get("shortOrderFillTransaction").get("units"), # 決済した数量
                self.res.get("shortOrderFillTransaction").get("price"), # 約定価格
                self.res.get("shortOrderFillTransaction").get("pl"), # (P/L)損益
            )) # 結果は position close: {数量} at {約定価格}. pl: {損益}　と表示される
            
        return # 戻り値が指定されていないため、何も返さずメソッドを終了する
