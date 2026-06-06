#uv環境下安裝The Python Package Index (PyPI) 的套件
#在終端機輸入uv add package_name (ex:uv add pandas)
import requests
import pandas as pd

def main():
     #youbike即時資訊的Application Programming Interface (API) 網址
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    response = requests.get(url)

    if response.status_code == 200:
        data:list[dict] = response.json() # 把內容（JSON）轉成 Python 的 list/dict 結構

        # list[dict] -> DataFrame
        df = pd.DataFrame(data) #把 list[dict] 轉成 DataFrame

        print(df.head())

    else:
        print("下載失敗")

if __name__ == '__main__':
    main()