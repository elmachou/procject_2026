import sys
import requests
import yfinance as yf
import pandas as pd
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QTabWidget, QComboBox, QCompleter, QMessageBox,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "SimHei", "Arial"]
matplotlib.rcParams["axes.unicode_minus"] = False
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

DEFAULT_STOCKS = [
    ("2330", "台積電"), ("2303", "聯電"), ("2454", "聯發科"),
    ("2317", "鴻海"), ("2412", "中華電"), ("3008", "大立光"),
    ("1301", "台塑"), ("1303", "南亞"), ("2002", "中鋼"),
    ("1101", "台泥"), ("1216", "統一"), ("2881", "富邦金"),
    ("2882", "國泰金"), ("2891", "中信金"), ("2886", "兆豐金"),
    ("5880", "合庫金"), ("3045", "台灣大"), ("2308", "台達電"),
    ("2357", "華碩"), ("2382", "廣達"), ("3231", "緯創"),
    ("3711", "日月光投控"), ("4904", "遠傳"),
]

def fetch_all_tw_stocks():
    try:
        resp = requests.get(
            "https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL",
            timeout=10,
        )
        if resp.status_code == 200:
            data = resp.json()
            stocks = [(item["Code"], item["Name"]) for item in data]
            stocks.sort(key=lambda x: int(x[0]))
            return stocks
    except Exception:
        pass
    return None

class CorrWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("台灣股票相關係數分析")
        self.resize(720, 620)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Load stock list
        stock_list = fetch_all_tw_stocks()
        if stock_list is None:
            stock_list = DEFAULT_STOCKS
            self.status_info = "使用預設股票清單（無法連線證交所 API）"
        else:
            self.status_info = f"已載入 {len(stock_list)} 檔上市股票"

        items = [f"{code} {name}" for code, name in stock_list]
        self.stock_map = {f"{code} {name}": code for code, name in stock_list}
        self.name_map = {code: name for code, name in stock_list}

        # Stock selection
        select_layout = QVBoxLayout()
        select_layout.addWidget(QLabel(f"選擇 4 檔股票（{self.status_info}）："))

        self.combos = []
        for i in range(4):
            h = QHBoxLayout()
            h.addWidget(QLabel(f"股票 {i+1}："))
            combo = QComboBox()
            combo.setEditable(True)
            combo.addItems(items)
            combo.setCurrentIndex(i if i < len(items) else 0)
            combo.setInsertPolicy(QComboBox.NoInsert)
            completer = QCompleter(items)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setFilterMode(Qt.MatchFlag.MatchContains)
            combo.setCompleter(completer)
            self.combos.append(combo)
            h.addWidget(combo)
            select_layout.addLayout(h)

        layout.addLayout(select_layout)

        self.label = QLabel("選擇股票後按下方按鈕計算")
        layout.addWidget(self.label)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.table = QTableWidget()
        self.tabs.addTab(self.table, "數值表格")

        self.figure = Figure(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.tabs.addTab(self.canvas, "熱力圖")

        btn = QPushButton("抓取資料 & 計算相關係數")
        btn.clicked.connect(self.fetch_and_compute)
        layout.addWidget(btn)

    def get_selected_codes(self):
        codes = []
        for combo in self.combos:
            text = combo.currentText().strip()
            if text in self.stock_map:
                codes.append(self.stock_map[text])
            else:
                # Try to find by pure code or name
                found = False
                for display, code in self.stock_map.items():
                    if text == code:
                        codes.append(code)
                        found = True
                        break
                    parts = display.split(" ", 1)
                    if len(parts) == 2 and text == parts[1]:
                        codes.append(code)
                        found = True
                        break
                if not found:
                    codes.append(text)
        return codes

    def fetch_and_compute(self):
        codes = self.get_selected_codes()

        if len(set(codes)) < 4:
            QMessageBox.warning(self, "警告", "請選擇 4 檔不同的股票！")
            return

        self.label.setText("正在抓取資料，請稍候...")
        QApplication.processEvents()

        tickers = [f"{code}.TW" for code in codes]
        try:
            data = yf.download(
                tickers,
                start="2006-01-01",
                interval="1d",
                auto_adjust=True,
            )
        except Exception as e:
            QMessageBox.critical(self, "錯誤", f"下載失敗：{e}")
            return

        if "Close" not in data.columns:
            QMessageBox.warning(self, "錯誤", "無法取得收盤價資料")
            return

        close = data["Close"]
        if isinstance(close, pd.Series):
            close = close.to_frame()

        col_map = {t: self.name_map.get(t.replace(".TW", ""), t) for t in close.columns}
        close = close.rename(columns=col_map)

        returns = close.pct_change().dropna()
        if returns.empty or returns.shape[1] < 2:
            QMessageBox.warning(self, "錯誤", "資料不足，無法計算相關係數")
            return

        corr = returns.corr()
        self.populate_table(corr)
        self.draw_heatmap(corr)
        self.label.setText(f"日報酬率相關係數（資料筆數: {len(returns)}）")

    def populate_table(self, corr):
        names = list(corr.columns)
        n = len(names)
        self.table.setRowCount(n)
        self.table.setColumnCount(n)
        self.table.setHorizontalHeaderLabels(names)
        self.table.setVerticalHeaderLabels(names)

        for i in range(n):
            for j in range(n):
                val = corr.iloc[i, j]
                item = QTableWidgetItem(f"{val:.4f}")
                item.setTextAlignment(Qt.AlignCenter)
                r = int(abs(val) * 255)
                if val > 0:
                    item.setBackground(QColor(255 - r, 255, 255 - r))
                else:
                    item.setBackground(QColor(255, 255 - r, 255 - r))
                self.table.setItem(i, j, item)

        self.table.resizeColumnsToContents()

    def draw_heatmap(self, corr):
        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)
        names = list(corr.columns)
        data = corr.values

        im = ax.imshow(data, cmap="RdBu_r", vmin=-1, vmax=1, aspect="auto")
        ax.set_xticks(range(len(names)))
        ax.set_yticks(range(len(names)))
        ax.set_xticklabels(names, rotation=45, ha="right")
        ax.set_yticklabels(names)

        for i in range(len(names)):
            for j in range(len(names)):
                ax.text(j, i, f"{data[i, j]:.4f}", ha="center", va="center",
                        fontsize=10, color="black" if abs(data[i, j]) < 0.7 else "white")

        self.figure.colorbar(im, ax=ax, label="相關係數")
        self.figure.tight_layout()
        self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CorrWindow()
    win.show()
    sys.exit(app.exec())
