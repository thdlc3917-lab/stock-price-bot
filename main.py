!pip install yfinance requests
import yfinance as yf
import requests
import time
from datetime import datetime

# --- 設定エリア ---
WEBHOOK_URL = "https://discord.com/api/webhooks/1471103745952579796/223rJQws4-4YEqusaSaP2OU5-EsLR9GrPIuoJ6zIjrDqBFXShHnVgVXhnMKS3stdaZJH"
STOCK_CODE = "6330.T"  # 東洋エンジニアリング
CHECK_INTERVAL = 300   # 5分ごとにチェック

# その日の記録用
todays_high = 0
todays_low = float('inf')
current_day = ""

def send_discord(message):
    payload = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Discord送信エラー: {e}")

print("🚀 監視ボットを起動しました。このタブを開いたままにしてください。")

while True:
    try:
        # 日本時間の現在時刻を取得
        now = datetime.now()
        today_str = now.strftime("%Y-%m-%d")

        # 日付が変わったらリセット
        if current_day != today_str:
            current_day = today_str
            todays_high = 0
            todays_low = float('inf')
            print(f"--- {today_str} の監視を開始しました ---")

        # 株価データ取得
        stock = yf.Ticker(STOCK_CODE)
        data = stock.history(period="1d", interval="1m")

        if not data.empty:
            latest_price = data['Close'].iloc[-1]
            market_high = data['High'].max()
            market_low = data['Low'].min()

            # 高値更新チェック
            if market_high > todays_high:
                todays_high = market_high
                msg = f"📈 【高値更新】東洋エンジニア(6330)\n現在の高値: {todays_high}円\n(現在値: {latest_price}円)"
                send_discord(msg)
                print(f"[{now.strftime('%H:%M')}] {msg}")

            # 安値更新チェック
            if market_low < todays_low:
                todays_low = market_low
                msg = f"📉 【安値更新】東洋エンジニア(6330)\n現在の安値: {todays_low}円\n(現在値: {latest_price}円)"
                send_discord(msg)
                print(f"[{now.strftime('%H:%M')}] {msg}")

    except Exception as e:
        print(f"エラー発生: {e}")

    # 指定した秒数待機
    time.sleep(CHECK_INTERVAL)
