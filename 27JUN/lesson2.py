import pandas as pd
import tkinter as tk
from tkinter import ttk

# --- 資料處理 ---
# 讀取 CSV 檔案，實際欄位名稱為英文
df = pd.read_csv('各鄉鎮市區人口密度.csv', encoding='utf-8')

# 第一筆資料為中文欄位說明列，予以移除；同時移除最後 5 筆非資料內容
df = df.iloc[1:-5]

# 選取所需欄位並重新命名
# site_id: 區域別、people_total: 人口數、area: 土地面積
df = df[['site_id', 'people_total', 'area']].rename(
    columns={'site_id': '區域別', 'people_total': '人口數', 'area': '土地面積'}
)

# 將 '人口數' 與 '土地面積' 轉換為數值型態，並移除 NaN 列
df['人口數'] = pd.to_numeric(df['人口數'], errors='coerce')
df['土地面積'] = pd.to_numeric(df['土地面積'], errors='coerce')
df = df.dropna()

# 新增 '人口密度' 欄位
df['人口密度'] = df['人口數'] / df['土地面積']


class App:
    """台灣鄉鎮市區人口密度查詢系統 GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title('台灣鄉鎮市區人口密度查詢系統')
        self.root.geometry('900x600')

        # 儲存原始資料副本
        self.data = df.copy()

        # --- 上方控制區 ---
        control_frame = ttk.Frame(root)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text='輸入區域名稱：').pack(side=tk.LEFT)

        self.keyword_entry = ttk.Entry(control_frame, width=30)
        self.keyword_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(control_frame, text='查詢', command=self.query).pack(side=tk.LEFT)

        # --- 下方表格區 ---
        table_frame = ttk.Frame(root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        columns = ('區域別', '人口數', '土地面積', '人口密度')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')

        # 設定各欄位標題與寬度
        col_width = 180
        for col in columns:
            self.tree.heading(col, text=col, anchor=tk.CENTER)
            self.tree.column(col, width=col_width, anchor=tk.CENTER)

        # 加入垂直捲軸
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 初始顯示所有資料
        self.show_data(self.data)

    def show_data(self, data):
        """將資料填入表格"""
        # 清除現有資料
        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in data.iterrows():
            self.tree.insert(
                '',
                tk.END,
                values=(
                    row['區域別'],
                    int(row['人口數']),
                    round(row['土地面積'], 2),
                    round(row['人口密度'], 2),
                ),
            )

    def query(self):
        """根據關鍵字篩選區域別，並更新表格"""
        keyword = self.keyword_entry.get().strip()
        if keyword:
            filtered = self.data[self.data['區域別'].str.contains(keyword, na=False)]
        else:
            filtered = self.data
        self.show_data(filtered)


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()
