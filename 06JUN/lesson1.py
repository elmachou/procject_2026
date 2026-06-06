from pathlib import Path

BASE_DIR_TEXT = Path(__file__).resolve().parent.parent
txt_path = BASE_DIR_TEXT / "student.txt"

file = open(txt_path, "r", encoding="utf-8")
print(type(file))
content = file.read()
print(content)
file.close()
file.closed

#=======================

with open(txt_path, "r", encoding="utf-8") as file:
	content = file.read()

print(file.closed)

#==============
import csv

BASE_DIR_CSV = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR_CSV / "考試分數_3年6班.csv"

with open(csv_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    print(type(reader))
    for row in reader:
        if int(row["數學"]) > 90:
            print(row["學生姓名"])