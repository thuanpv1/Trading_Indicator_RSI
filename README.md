# RSI Dashboard 4H

Ứng dụng web đơn giản hiển thị chỉ số RSI (Relative Strength Index) khung 4H cho các cặp tiền tệ Forex sử dụng TradingView API.

## Tính năng

- 📊 Hiển thị RSI 4H cho 18 cặp tiền tệ Forex
- 🔄 Reload dữ liệu bằng cách refresh trang hoặc nhấn nút Reload
- 🎯 Giao diện đơn giản với 2 cột: Tên cặp tiền tệ và giá trị RSI
- ⚡ Sử dụng batch request để lấy tất cả dữ liệu trong 1 lần gọi API
- 🌐 Responsive design với Bootstrap

## Cài đặt

1. **Clone repository:**
```bash
git clone <repository-url>
cd Trading_Indicator_RSI
```

2. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

3. **Chạy ứng dụng:**
```bash
python app.py
```

4. **Truy cập ứng dụng:**
   Mở trình duyệt và vào: `http://localhost:5000`

## Cấu trúc project

```
Trading_Indicator_RSI/
├── app.py                 # Flask server và logic RSI
├── requirements.txt       # Dependencies (Flask + tradingview-ta)
├── templates/
│   └── index.html        # Template HTML với JavaScript
└── README.md
```

## API Endpoints

- `GET /` - Trang chủ hiển thị dashboard
- `GET /api/rsi` - API endpoint trả về dữ liệu RSI JSON

## Các cặp tiền tệ được theo dõi

- AUDJPY, AUDUSD, AUDCHF, AUDCAD
- EURUSD, EURCAD, EURJPY, EURAUD, EURGBP
- GBPCHF, GBPCAD, GBPUSD, GBPAUD
- USDJPY, USDCHF, USDCAD
- NZDUSD, EURCHF

## Cách sử dụng

1. Mở trang web
2. Dữ liệu RSI sẽ tự động load
3. Nhấn nút "🔄 Reload" để cập nhật dữ liệu mới
4. Hoặc refresh trang để load lại

## Lưu ý kỹ thuật

- Sử dụng TradingView unofficial API (miễn phí)
- Khung thời gian: 4H (4 giờ)
- RSI được tính toán dựa trên 14 periods
- Batch request giúp tránh rate limit
- Không cần API key hay đăng ký tài khoản
