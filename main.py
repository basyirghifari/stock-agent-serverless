import yfinance as yf
import os

def check_stock():
    print("Memulai pengecekan harga...")
    # Kita tes dengan GOTO-W
    ticker = "GOTO-W.JK"
    stock = yf.Ticker(ticker)
    
    try:
        data = stock.history(period="1d")
        if not data.empty:
            price = data['Close'].iloc[-1]
            print(f"Harga terakhir {ticker} adalah: Rp{price}")
        else:
            print(f"Data untuk {ticker} tidak ditemukan atau pasar sedang tutup.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    check_stock()
