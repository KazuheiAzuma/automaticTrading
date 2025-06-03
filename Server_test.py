import http.server # Python標準ライブラリ。HTTPサーバーを構築する為のインポート
import socketserver # ネットワーク通信を簡単にするためのモジュール


class WebhookHandler(http.server.BaseHTTPRequestHandler):
# WebhookHandlerは自分でつけるクラスの名称、()は独自のリクエスト処理を実装
    def do_POST(self): # このメゾットはPOSTリクエストがサーバーに送信された時に実行される
        
        # データの抽出
        content_length = int(self.headers['content-length']) # content-lengthとはHTTPヘッダーの項目の一つでデータサイズを取得
        # self.headers['content-length'] は、HTTPヘッダーの辞書型オブジェクトから "content-length" の値を文字列型で取得するための記述
        # int()で値を文字列型から整数型に変換している
        
        # 取得したデータサイズをファイルオブジェクトで読み込み、デコードで文字列に変換
        req_body = self.rfile.read(content_length).decode("utf-8") 
        # self.rfileは、クライアントから送られたデータを読み取るためのファイルオブジェクト
        # read(content_length)は、指定されたバイト数(content_length)だけデータを読み取る処理
        # decode("utf-8")はエンコードされたバイト列を元の文字列に変換する処理
        
        
        print(req_body) #受け取ったデータをサーバーのコンソールに表示
        
        # ステータスコード200を返す
        self.send_response(200) #HTTPステータスコードをクライアントに送信する。200はリクエストが正常に処理された事を示す
        self.end_headers() #ヘッダーの終了を通知し、次にボディを送る準備ができる
        
with socketserver.TCPServer(("", 3000), WebhookHandler) as httpd: #TCPサーバーを作成し、TCPサーバーのインスタンス(実際に動作するサーバー"httpd")を作成
    #("", 3000)の""部分はネットワークインターフェース（ローカルIPアドレス）で接続を受け付けることを意味する
    httpd.serve_forever() #サーバーを永続的に動作させるメソッド。Ctrl+Cでプログラムを停止するまで、サーバーは動作し続ける。