import yfinance as yf
import requests
import os
from datetime import datetime

# --- 設定エリア (GitHub Secretsから読み込む) ---
WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
STOCK_CODE = "6330.T"

def send_discord(message):
    if not WEBHOOK_URL:
        print("Webhook URLが設定されていません")
        return
    payload = {"content": message}
    try:
        requests.post(WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"Discord送信エラー: {e}")

def main():
    try:
        now = datetime.now()
        stock = yf.Ticker(STOCK_CODE)
        # 当日の1分足データをすべて取得
        data = stock.history(period="1d", interval="1m")

        if data.empty:
            print("データが取得できませんでした（市場閉場中など）")
            return

        latest_price = round(data['Close'].iloc[-1], 1)
        market_high = round(data['High'].max(), 1)
        market_low = round(data['Low'].min(), 1)

        # 直近の価格が「今日の高値」または「今日の安値」に等しいかチェック
        # GitHub Actionsで数分おきに起動するため、その瞬間に更新されていれば通知
        if latest_price >= market_high:
            msg = f"📈 【高値圏】東洋エンジニア(6330)\n本日高値: {market_high}円\n(現在値: {latest_price}円)"
            send_discord(msg)
        
        elif latest_price <= market_low:
            msg = f"📉 【安値圏】東洋エンジニア(6330)\n本日安値: {market_low}円\n(現在値: {latest_price}円)"
            send_discord(msg)

        print(f"[{now.strftime('%H:%M')}] Check completed. Price: {latest_price}")

    except Exception as e:
        print(f"エラー発生: {e}")

if __name__ == "__main__":
    main()
