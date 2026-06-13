import requests
from requests import Response
import pandas as pd
from pandas import DataFrame
from pathlib import Path
import report # import自訂的Module report.py，負責將 DataFrame 內容輸出為 PDF 報表

def main():
    # 台北市 YouBike 2.0 的 Web API 網址
    url:str = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    # 使用 requests 套件裡面的 get 函式，執行後會傳出 Response 的實體
    response:Response = requests.get(url) 

    if response.status_code == 200: # 使用 Response 裡的 Property 叫 status_code，如果取得的數字是 200 代表下載成功，如果不是則代表下載失敗
        data:list[dict] = response.json() # 使用 Response 實體的 json() 方法，會傳出 list 的資料結構

        # list[dict] -> DataFrame
        df:DataFrame = pd.DataFrame(data=data)

        print(df.tail())

        output_file = Path(__file__).with_name("youbike_report.pdf")
        report.export_to_pdf(df, output_file) #使用自訂的 Module report.py 裡的 export_to_pdf 函式，將 DataFrame 內容輸出為 PDF 報表

    else:
        print("下載失敗")

if __name__ == '__main__':
    main()