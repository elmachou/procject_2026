from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
txt_path = BASE_DIR / "student.txt"

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
from pathlib import Path
import csv

BASE_DIR = Path(__file__).resolve().parent.parent
csv_path = BASE_DIR / "考試分數_3年6班.csv"

with open(csv_path, "r", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    print(type(reader))
    for row in reader:
        if int(row["數學"]) > 90:
            print(row["學生姓名"])