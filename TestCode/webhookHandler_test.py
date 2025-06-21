import http.server # Python標準ライブラリ。HTTPサーバーを構築する為のインポート
import socketserver # ネットワーク通信を簡単にするためのモジュール
from fx_test import fx_trader
import config_p

account_id = config_p.ACCOUNT_ID_P
access_token = config_p.ACCESS_TOKEN

class WebhookHandler(http.server.BaseHTTPRequestHandler):# ()はクラス継承
    def do_POST(self): # POSTリクエストがこのサーバーに送信された時に実行される
        
        # データの抽出
        content_length = int(self.headers['content-length'])
        # content-lengthでデータサイズを取得
        # self.headersは、HTTPヘッダーの辞書型オブジェクトから[]の値を取得
        # int()で値を文字列型から整数型に変換
        
        # 取得したデータサイズをファイルオブジェクトで読み込み、デコードで文字列に変換
        req_body = self.rfile.read(content_length).decode("utf-8")
        # self.rfileは、クライアントから送られたデータを読み取るためのファイルオブジェクト
        # read(content_length)は、指定されたバイト数(content_length)だけデータを読み取る処理
        # decode("utf-8")はエンコードされたバイト列を元の文字列に変換する処理
        print(req_body) # POSTが正常に届いているか確認用
        
        # 現在の保有ポジションを取得
        fx.positions()         
        
        # 新規注文（現在の保有ポジションが0の時に実行される）
        flag = int(req_body) # 送られきた情報(通貨ペア・数量・注文種類・注文タイプ)を変数に代入
        fx.order(flag) # 送られてきた情報をorder関数で発注する
        
        # 決済注文（現在の保有ポジションが0の以外の時に実行される）
        fx.close() # ポジションを決済し、損益を確定
        
        # ステータスコード200を返す
        self.send_response(200) # HTTPステータスコードをクライアントに送信する。200はリクエストが正常に処理された事を示す
        self.end_headers() # ヘッダーの終了を通知し、次にボディを送る準備ができる


fx = fx_trader(instrument="USD_JPY", account_id=account_id, access_token=access_token)

with socketserver.TCPServer(("", 3000), WebhookHandler) as httpd: # TCPサーバーを作成し、TCPサーバーのインスタンス(実際に動作するサーバー"httpd")を作成
    # ("", 3000)の""部分はネットワークインターフェース（ローカルIPアドレス）で接続を受け付けることを意味する
    httpd.serve_forever() # サーバーを永続的に動作させるメソッド。Ctrl+Cでプログラムを停止するまで、サーバーは動作し続ける。
