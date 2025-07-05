from oandapyV20 import API
import oandapyV20.endpoints.accounts as accounts
import config_p

# 接続情報（← あなたのトークンとアカウントIDを入力）
account_id = config_p.ACCOUNT_ID_P
access_token = config_p.ACCESS_TOKEN

# OANDA APIクライアント（デモ環境）
client = API(access_token=access_token, environment="practice")

# アカウント情報取得リクエスト
r = accounts.AccountDetails(accountID=account_id)

# リクエスト送信＆レスポンス表示
try:
    response = client.request(r)
    print("✅ 接続成功！アカウント情報：")
    print(response)
except Exception as e:
    print("❌ 接続失敗:", e)