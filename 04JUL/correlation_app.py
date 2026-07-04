import sys
import yfinance as yf
import pandas as pd
import numpy as np
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout,
    QTableWidget, QTableWidgetItem, QPushButton, QLabel,
    QTabWidget,
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

tickers = {
    "台積電": "2330.TW",
    "聯電": "2303.TW",
    "聯發科": "2454.TW",
    "鴻海": "2317.TW",
}

class CorrWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("股票相關係數")
        self.resize(620, 520)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        self.label = QLabel("按下方按鈕抓取資料並計算相關係數")
        layout.addWidget(self.label)

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        # Table tab
        self.table = QTableWidget()
        self.tabs.addTab(self.table, "數值表格")

        # Heatmap tab
        self.figure = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.tabs.addTab(self.canvas, "熱力圖")

        btn = QPushButton("抓取資料 & 計算相關係數")
        btn.clicked.connect(self.fetch_and_compute)
        layout.addWidget(btn)

    def fetch_and_compute(self):
        self.label.setText("正在抓取資料，請稍候...")
        QApplication.processEvents()

        data = yf.download(
            list(tickers.values()),
            start="2006-01-01",
            interval="1d",
            auto_adjust=True,
        )
        close = data["Close"]
        code_to_name = {v: k for k, v in tickers.items()}
        close = close.rename(columns=code_to_name)

        returns = close.pct_change().dropna()
        corr = returns.corr()

        self.populate_table(corr)
        self.draw_heatmap(corr)
        self.label.setText(f"日報酬率相關係數 (資料筆數: {len(returns)})")

    def populate_table(self, corr: pd.DataFrame):
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
                    color = QColor(255 - r, 255, 255 - r)
                else:
                    color = QColor(255, 255 - r, 255 - r)
                item.setBackground(color)

                self.table.setItem(i, j, item)

        self.table.resizeColumnsToContents()

    def draw_heatmap(self, corr: pd.DataFrame):
        self.figure.clear()
        ax = self.figure.add_subplot(1, 1, 1)

        names = list(corr.columns)
        data = corr.values

        im = ax.imshow(data, cmap="RdYlBu", vmin=-1, vmax=1, aspect="auto")

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
