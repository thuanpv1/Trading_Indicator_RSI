// RSI Trading Dashboard JavaScript

class RSIDashboard {
    constructor() {
        this.refreshInterval = null;
        this.autoRefreshTime = 30000; // 30 seconds
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadData();
        this.startAutoRefresh();
    }

    bindEvents() {
        document.getElementById('refreshBtn').addEventListener('click', () => {
            this.loadData();
        });
    }

    async loadData() {
        try {
            this.showLoading();
            this.hideError();
            
            const response = await fetch('/api/rsi');
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const result = await response.json();
            this.displayData(result.data);
            this.updateSummary(result.data);
            this.updateLastUpdateTime(result.timestamp);
            this.hideLoading();
            
        } catch (error) {
            console.error('Error loading data:', error);
            this.showError('Không thể tải dữ liệu. Vui lòng kiểm tra kết nối API.');
            this.hideLoading();
        }
    }

    displayData(data) {
        const tbody = document.getElementById('rsiTableBody');
        tbody.innerHTML = '';

        data.forEach(item => {
            const row = this.createTableRow(item);
            tbody.appendChild(row);
        });

        document.getElementById('rsiTable').classList.remove('d-none');
    }

    createTableRow(item) {
        const row = document.createElement('tr');
        
        // Xác định class CSS cho RSI
        let rsiClass = 'rsi-neutral';
        let signalText = 'Neutral';
        let signalClass = 'signal-neutral';
        
        if (item.RSI !== null) {
            if (item.RSI < 30) {
                rsiClass = 'rsi-oversold';
                signalText = 'Mua';
                signalClass = 'signal-buy';
            } else if (item.RSI > 70) {
                rsiClass = 'rsi-overbought';
                signalText = 'Bán';
                signalClass = 'signal-sell';
            }
        }

        // Định dạng giá
        const formattedPrice = item.price ? item.price.toFixed(5) : 'N/A';
        const rsiValue = item.RSI !== null ? item.RSI.toFixed(2) : 'N/A';
        
        // Trạng thái
        const statusIcon = item.status === 'success' ? 
            '<i class="fas fa-check-circle status-success"></i>' : 
            '<i class="fas fa-exclamation-circle status-error"></i>';

        row.innerHTML = `
            <td class="symbol">${item.symbol}</td>
            <td class="price">${formattedPrice}</td>
            <td class="${rsiClass}">${rsiValue}</td>
            <td><span class="badge ${signalClass}">${signalText}</span></td>
            <td>${statusIcon}</td>
        `;

        return row;
    }

    updateSummary(data) {
        let oversoldCount = 0;
        let neutralCount = 0;
        let overboughtCount = 0;

        data.forEach(item => {
            if (item.RSI !== null) {
                if (item.RSI < 30) {
                    oversoldCount++;
                } else if (item.RSI > 70) {
                    overboughtCount++;
                } else {
                    neutralCount++;
                }
            }
        });

        document.getElementById('oversoldCount').textContent = oversoldCount;
        document.getElementById('neutralCount').textContent = neutralCount;
        document.getElementById('overboughtCount').textContent = overboughtCount;
    }

    updateLastUpdateTime(timestamp) {
        const date = new Date(timestamp);
        const formattedTime = date.toLocaleString('vi-VN');
        document.getElementById('lastUpdate').textContent = `Cập nhật lần cuối: ${formattedTime}`;
    }

    showLoading() {
        document.getElementById('loadingSpinner').classList.remove('d-none');
        document.getElementById('rsiTable').classList.add('d-none');
    }

    hideLoading() {
        document.getElementById('loadingSpinner').classList.add('d-none');
    }

    showError(message) {
        document.getElementById('errorMessage').textContent = message;
        document.getElementById('errorAlert').classList.remove('d-none');
    }

    hideError() {
        document.getElementById('errorAlert').classList.add('d-none');
    }

    startAutoRefresh() {
        this.refreshInterval = setInterval(() => {
            this.loadData();
        }, this.autoRefreshTime);
    }

    stopAutoRefresh() {
        if (this.refreshInterval) {
            clearInterval(this.refreshInterval);
            this.refreshInterval = null;
        }
    }
}

// Khởi tạo dashboard khi trang được load
document.addEventListener('DOMContentLoaded', () => {
    new RSIDashboard();
});

// Dừng auto-refresh khi trang bị ẩn
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Trang bị ẩn, có thể dừng auto-refresh để tiết kiệm tài nguyên
        console.log('Page hidden - auto refresh continues');
    } else {
        // Trang được hiển thị lại
        console.log('Page visible - auto refresh active');
    }
});
