import http.server # Python標準ライブラリ。HTTPサーバーを構築する為のインポート
import socketserver # ネットワーク通信を簡単にするためのモジュール
from fx_test import fx_trader
import config_p
import json
import argparse

# --- 実行時の引数からdebugフラグを取得 ---
def get_debug_flag():
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help='デバッグモードを有効にする')
    args = parser.parse_args()
    return args.debug

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
        fx.logging("POSTリクエスト：{}".format(req_body))# POSTが正常に届いているか確認用

        # 現在の保有ポジションを取得
        fx.positions()         
        
        # 新規注文（現在の保有ポジションが0の時に実行される）
        data = json.loads(req_body) # 送られきた情報(通貨ペア・数量・注文種類・注文タイプ)を取得
        fx.order(data['instrument'], data['units'], data['side'], data['type']) # 送られてきた情報をorder関数で発注する

        # 決済注文（現在の保有ポジションが0の以外の時に実行される）
        fx.close() # ポジションを決済し、損益を確定
        
        # ステータスコード200を返す
        self.send_response(200) # HTTPステータスコードをクライアントに送信する。200はリクエストが正常に処理された事を示す
        self.end_headers() # ヘッダーの終了を通知し、次にボディを送る準備ができる

#メイン処理
if __name__ == "__main__":
    debug = get_debug_flag()

    if debug:
        print("デモ口座です")
        account_id = config_p.ACCOUNT_ID_P
        access_token = config_p.ACCESS_TOKEN_P
    else:
        print("本番口座です")
        account_id = config_p.ACCOUNT_ID_L
        access_token = config_p.ACCESS_TOKEN_L

    fx = fx_trader(instrument="USD_JPY", account_id=account_id, access_token=access_token, debug=debug)

    port = 8080 #実際のポート番号（ローカルホストの場合は8080）
    with socketserver.TCPServer(("", port), WebhookHandler) as httpd: # TCPサーバーを作成し、TCPサーバーのインスタンス(実際に動作するサーバー"httpd")を作成
        # ("", 3000)の""部分はネットワークインターフェース（ローカルIPアドレス）で接続を受け付けることを意味する
        print("server is starting")
        httpd.serve_forever() # サーバーを永続的に動作させるメソッド。Ctrl+Cでプログラムを停止するまで、サーバーは動作し続ける。
