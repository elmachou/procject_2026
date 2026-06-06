#uv環境下安裝The Python Package Index (PyPI) 的套件
#在終端機輸入uv add package_name (ex:uv add pandas)
import requests
from requests import Response

def main():
    #youbike即時資訊的Application Programming Interface (API) 網址
    url:str = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    # 發送 HTTP GET 請求，取得伺服器回應
    response:Response = requests.get(url)

    # 顯示 response 的型別
    print(type(response))

    if response.status_code == 200: #200代表成功 404代表找不到網頁 500代表伺服器錯誤
        data:list[dict] = response.json() # 把內容（JSON）轉成 Python 的 list/dict 結構
        print("下載成功")
        print(type(data))
        print(len(data))
        print(type(data[0]))
        print(data[0])
    else:
        print("下載失敗")
        print(response.status_code)

if __name__ == '__main__':
    main()