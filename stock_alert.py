import requests
import os
from datetime import datetime

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

now = datetime.now()
message = (
    f"🚨 株価アラート！\n"
    f"銘柄: ラウンドワン（4680.T）\n"
    f"目標価格 1,400円 に到達！\n"
    f"━━━━━━━━━━\n"
    f"高値: 1,423円\n"
    f"安値: 1,385円\n"
    f"始値: 1,390円\n"
    f"終値: 1,415円\n"
    f"━━━━━━━━━━\n"
    f"チェック時刻: {now.strftime('%Y/%m/%d %H:%M')}"
)
send_line_message(message)
