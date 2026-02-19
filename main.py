import os
import requests
import yfinance as yf
from groq import Groq

def kirim_telegram(pesan):
    token = os.environ.get("BOT_TOKEN")
    chat_id = os.environ.get("CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": pesan,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            print("Pesan berhasil dikirim ke Telegram!")
        else:
            print(f"Gagal kirim Telegram: {response.text}")
    except Exception as e:
        print(f"Error Telegram: {e}")

def dapatkan_analisis_ai(ticker, harga):
    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    prompt = f"Harga waran {ticker} sekarang Rp{harga}. Berikan analisis singkat (1-2 kalimat) untuk trader."
    
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama3-8b-8192",
    )
    return completion.choices[0].message.content

def main():
    ticker = "ISAP-W.JK"
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    
    if not data.empty:
        harga = data['Close'].iloc[-1]
        analisis = dapatkan_analisis_ai(ticker, harga)
        
        # Format pesan untuk Telegram
        pesan_final = (
            f"🔔 *Update Waran Aktif*\n\n"
            f"Ticker: `{ticker}`\n"
            f"Harga: *Rp{harga}*\n\n"
            f"🤖 *Analisis Agent:*\n{analisis}"
        )
        
        kirim_telegram(pesan_final)
    else:
        print("Data tidak ditemukan.")

if __name__ == "__main__":
    main()
