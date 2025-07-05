#保有ポジション取得のテストレスポンス
positionRes = {
    "position": {
        "instrument": "USD_JPY",
        "long": {
        "units": "100",
        "averagePrice": "110.500",
        "pl": "50.000",
        "resettablePL": "50.000",
        "unrealizedPL": "50.000"
        },
        "short": {
        "units": "200",
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
orderRes = {
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

#ロングポジションクローズのテストレスポンス
closeLongRes = {
  "longOrderCreateTransaction": {
    "id": "12345",
    "time": "2023-08-25T12:34:56.789Z",
    "userID": 1010101,
    "accountID": "001-001-1234567-001",
    "batchID": "12345",
    "type": "MARKET_ORDER",
    "instrument": "USD_JPY",
    "units": "-1000",  
    "timeInForce": "FOK",
    "positionFill": "REDUCE_ONLY",
    "reason": "POSITION_CLOSEOUT"
  },
  "orderFillTransaction": {
    "id": "12346",
    "time": "2023-08-25T12:34:56.890Z",
    "userID": 1010101,
    "accountID": "001-001-1234567-001",
    "batchID": "12345",
    "type": "ORDER_FILL",
    "instrument": "USD_JPY",
    "units": "-1000",
    "price": "145.67",
    "pl": "5.00",
    "financing": "-0.01",
    "commission": "0.00",
    "accountBalance": "10005.00"
  },
  "relatedTransactionIDs": [
    "12345",
    "12346"
  ],
  "lastTransactionID": "12346"
}

#ショートポジションクローズのテストレスポンス
closeShortRes = {
  "shortOrderCreateTransaction": {
    "id": "23456",
    "time": "2025-07-05T10:20:30.123456789Z",
    "userID": 1010101,
    "accountID": "001-001-1234567-001",
    "batchID": "23456",
    "type": "MARKET_ORDER",
    "instrument": "USD_JPY",
    "units": "1000",
    "timeInForce": "FOK",
    "positionFill": "REDUCE_ONLY",
    "reason": "POSITION_CLOSEOUT"
  },
  "orderFillTransaction": {
    "id": "23457",
    "time": "2025-07-05T10:20:30.223456789Z",
    "userID": 1010101,
    "accountID": "001-001-1234567-001",
    "batchID": "23456",
    "type": "ORDER_FILL",
    "instrument": "USD_JPY",
    "units": "1000",
    "price": "160.55",
    "pl": "-8.50",
    "financing": "-0.02",
    "commission": "0.00",
    "accountBalance": "9991.48"
  },
  "relatedTransactionIDs": [
    "23456",
    "23457"
  ],
  "lastTransactionID": "23457"
}