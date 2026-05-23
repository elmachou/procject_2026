#猜數字遊戲
import random

answer = random.randint(1, 100) # 產生1到100的隨機整數
count = 0

print("歡迎來到猜數字遊戲！")
print("一個1到100的數字，請開始猜吧！")

while True:
    guess = int(input("請猜一個1到100的數字:"))
    count += 1

    if guess < answer:
        print("太小了！")
    elif guess > answer:
        print("太大了！")
    else:
        print(f"恭喜你猜對了！答案就是{answer}！")
        print(f"你總共猜了 {count} 次。")
        break # 猜對了，跳出迴圈   