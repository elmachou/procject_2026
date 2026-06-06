#uv環境下安裝The Python Package Index (PyPI) 的套件
#在終端機輸入uv add package_name
import requests

#youbike即時資訊的Application Programming Interface (API) 網址
url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

def main():
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        print("下載成功")
        print(type(data))
        print(len(data))
        print(data[0])
    else:
        print("下載失敗")
        print(response.status_code)

if __name__ == '__main__':
    main()