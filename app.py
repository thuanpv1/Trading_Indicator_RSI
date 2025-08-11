from tradingview_ta import get_multiple_analysis, Interval
import time

# Danh sách cặp và khung thời gian
pairs = [
    {"symbol": "AUDJPY", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "AUDUSD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "AUDCHF", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "AUDCAD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURUSD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURCAD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURJPY", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURAUD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURGBP", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "GBPCHF", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "GBPCAD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "GBPUSD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "USDJPY", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "USDCHF", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "USDCAD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "NZDUSD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "GBPAUD", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
    {"symbol": "EURCHF", "exchange": "OANDA", "interval": Interval.INTERVAL_4_HOURS},
]

# Tạo danh sách symbols theo format EXCHANGE:SYMBOL cho get_multiple_analysis
symbols_list = [f"{pair['exchange']}:{pair['symbol']}" for pair in pairs]

print(f"=== RSI Dashboard M15 - Batch Request ===")
print(f"Đang lấy dữ liệu cho {len(symbols_list)} symbols...")

try:
    # Request tất cả symbols cùng một lúc
    analysis_results = get_multiple_analysis(
        screener="forex",  # Tất cả symbols đều là forex
        interval=Interval.INTERVAL_4_HOURS,
        symbols=symbols_list
    )

    print(f"{'Symbol':<12} {'RSI':<8} {'Signal':<10} {'Status':<10}")
    print("-" * 50)

    # Xử lý kết quả
    for symbol_key, analysis in analysis_results.items():
        # Lấy tên symbol từ key (bỏ exchange prefix)
        symbol_name = symbol_key.split(':')[1] if ':' in symbol_key else symbol_key

        if analysis is not None:
            try:
                rsi = analysis.indicators.get("RSI")
                if rsi is not None:
                    # Xác định tín hiệu
                    if rsi < 30:
                        signal = "BUY"
                    elif rsi > 70:
                        signal = "SELL"
                    else:
                        signal = "NEUTRAL"

                    print(f"{symbol_name:<12} {rsi:<8.2f} {signal:<10} {'SUCCESS':<10}")
                else:
                    print(f"{symbol_name:<12} {'N/A':<8} {'N/A':<10} {'NO_RSI':<10}")
            except Exception as e:
                print(f"{symbol_name:<12} {'ERROR':<8} {'N/A':<10} {str(e)[:10]:<10}")
        else:
            print(f"{symbol_name:<12} {'N/A':<8} {'N/A':<10} {'NO_DATA':<10}")

    print(f"\n=== Tổng kết ===")
    successful_count = sum(1 for analysis in analysis_results.values() if analysis is not None)
    print(f"Thành công: {successful_count}/{len(symbols_list)} symbols")
    print("Hoàn thành trong 1 request duy nhất!")

except Exception as e:
    print(f"Lỗi khi lấy dữ liệu: {e}")
    print("Có thể do rate limit hoặc lỗi kết nối.")
