#保有ポジション取得のテストレスポンス
positionRes = {
    "position": {
        "instrument": "USD_JPY",
        "long": {
        "units": "0",
        "averagePrice": "110.500",
        "pl": "50.000",
        "resettablePL": "50.000",
        "unrealizedPL": "50.000"
        },
        "short": {
        "units": "0",
        "averagePrice": "0.000",
        "pl": "0.000",
        "resettablePL": "0.000",
        "unrealizedPL": "0.000"
        },
        "pl": "50.000",
        "unrealizedPL": "50.000",
        "marginUsed": "33.000"
    },
    "lastTransactionID": "12345"
}


#注文実施後のテストレスポンス
orderSres = {
  "orderCreateTransaction": {
    "id": "12345",
    "time": "2024-06-21T08:17:54.123456789Z",
    "userID": 123456789,
    "accountID": "101-011-12345678-001",
    "batchID": "12345",
    "request": {
      "type": "MARKET",
      "instrument": "USD_JPY",
      "units": "100",
      "timeInForce": "FOK",
      "positionFill": "DEFAULT"
    },
    "instrument": "USD_JPY",
    "units": "100",
    "type": "MARKET_ORDER",
    "reason": "CLIENT_ORDER"
  },
  "orderFillTransaction": {
    "id": "12346",
    "time": "2024-06-21T08:17:54.123456789Z",
    "userID": 123456789,
    "accountID": "101-011-12345678-001",
    "instrument": "USD_JPY",
    "units": "100",
    "price": "143.500",
    "reason": "MARKET_ORDER",
    "pl": "1.234",
    "financing": "0.000",
    "commission": "0.000",
    "guaranteedExecutionFee": "0.000"
  },
  "relatedTransactionIDs": [
    "12345",
    "12346"
  ],
  "lastTransactionID": "12346"
}