from flask import Flask, render_template, jsonify
from tradingview_ta import get_multiple_analysis, Interval
from datetime import datetime
import time
import threading
import requests

app = Flask(__name__)

# Danh sách cặp và khung thời gian
pairs = [
    {"symbol": "AUDUSD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "AUDCHF", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "AUDCAD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURUSD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURAUD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURGBP", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "GBPCHF", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "GBPCAD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "GBPUSD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "USDJPY", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "USDCHF", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "NZDUSD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "GBPAUD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
]

def get_rsi_data():
    """
    Lấy dữ liệu RSI cho tất cả các cặp hàng hóa
    """
    # Tạo danh sách symbols theo format EXCHANGE:SYMBOL cho get_multiple_analysis
    symbols_list = [f"{pair['exchange']}:{pair['symbol']}" for pair in pairs]

    try:
        # Request tất cả symbols cùng một lúc
        analysis_results = get_multiple_analysis(
            screener="forex",  # Tất cả symbols đều là forex
            interval=Interval.INTERVAL_4_HOURS,
            symbols=symbols_list
        )

        results = []

        # Xử lý kết quả
        for symbol_key, analysis in analysis_results.items():
            # Lấy tên symbol từ key (bỏ exchange prefix)
            symbol_name = symbol_key.split(':')[1] if ':' in symbol_key else symbol_key

            if analysis is not None:
                try:
                    rsi = analysis.indicators.get("RSI")
                    if rsi is not None:
                        results.append({
                            "symbol": symbol_name,
                            "rsi": round(rsi, 2),
                            "status": "success"
                        })
                    else:
                        results.append({
                            "symbol": symbol_name,
                            "rsi": None,
                            "status": "no_rsi"
                        })
                except Exception as e:
                    results.append({
                        "symbol": symbol_name,
                        "rsi": None,
                        "status": "error"
                    })
            else:
                results.append({
                    "symbol": symbol_name,
                    "rsi": None,
                    "status": "no_data"
                })

        # Sắp xếp theo RSI tăng dần (RSI None sẽ ở cuối)
        results.sort(key=lambda x: x['rsi'] if x['rsi'] is not None else float('inf'))

        return results

    except Exception as e:
        print(f"Lỗi khi lấy dữ liệu: {e}")
        return []

def keep_alive_service():
    """
    Gửi request định kỳ để giữ service không bị sleep
    """
    url = "https://trading-indicator-rsi.onrender.com"

    while True:
        try:
            response = requests.get(url, timeout=10)
            print(f"Keep-alive ping: {response.status_code} at {datetime.now().strftime('%H:%M:%S')}")
        except Exception as e:
            print(f"Keep-alive failed: {e}")

        # Chờ 60 giây (1 phút)
        time.sleep(60)

def start_keep_alive():
    """
    Khởi động keep-alive service trong background thread
    """
    keep_alive_thread = threading.Thread(target=keep_alive_service, daemon=True)
    keep_alive_thread.start()
    print("Keep-alive service started - pinging every 1 minute")

@app.route('/')
def index():
    """
    Trang chủ hiển thị bảng RSI
    """
    return render_template('index.html')

@app.route('/api/rsi')
def api_rsi():
    """
    API endpoint để lấy dữ liệu RSI
    """
    data = get_rsi_data()
    return jsonify({
        "data": data,
        "timestamp": datetime.now().isoformat(),
        "total_pairs": len(data)
    })

if __name__ == '__main__':
    # Khởi động keep-alive service
    start_keep_alive()

    # Chạy Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
