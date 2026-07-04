import yfinance as yf
import requests
import os
from datetime import datetime

# 監視銘柄の設定
STOCKS = [
    {"symbol": "4680.T", "name": "ラウンドワン", "target_price": 1400},
]

def send_line_message(message):
    token = os.environ.get("LINE_CHANNEL_ACCESS_TOKEN")
    user_id = os.environ.get("LINE_USER_ID")
    url = "https://api.line.me/v2/bot/message/push"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }
    payload = {
        "to": user_id,
        "messages": [{"type": "text", "text": message}]
    }
    response = requests.post(url, headers=headers, json=payload)
    print(f"LINE送信結果: {response.status_code}")

def check_stocks():
    now = datetime.now()
    print(f"チェック開始: {now.strftime('%Y-%m-%d %H:%M:%S')}")

    for stock in STOCKS:
        symbol = stock["symbol"]
        name = stock["name"]
        target = stock["target_price"]

        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d", interval="1h")

            if hist.empty:
                print(f"{name}: データ取得できず")
                continue

            latest = hist.iloc[-1]
            high = latest["High"]
            low = latest["Low"]
            open_ = latest["Open"]
            close = latest["Close"]

            print(f"{name}: 高値={high:.0f}円, 目標={target}円")

            if high >= target:
                message = (
                    f"🚨 株価アラート\n"
                    f"銘柄: {name}（{symbol}）\n"
                    f"目標価格 {target:,}円 に到達！\n"
                    f"━━━━━━━━━━\n"
                    f"高値: {high:,.0f}円\n"
                    f"安値: {low:,.0f}円\n"
                    f"始値: {open_:,.0f}円\n"
                    f"終値: {close:,.0f}円\n"
                    f"━━━━━━━━━━\n"
                    f"チェック時刻: {now.strftime('%Y/%m/%d %H:%M')}"
                )
                send_line_message(message)
            else:
                print(f"  → 未達（あと{target - high:,.0f}円）")

        except Exception as e:
            print(f"{name}: エラー - {e}")

if __name__ == "__main__":
    check_stocks()
