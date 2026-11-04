import csv
from pathlib import Path

csv_path = Path("DAY 8/data/students.csv")


headers = ["Name","grade","Friends"]
students = {
    "Name":"Hamza",
    "grade":"A",
    "Friends":0
},{
    "Name":"Faizan",
    "grade":"A",
    "Friends":8
}

with open(csv_path,"w",newline='',encoding="utf-8") as f:
    writer = csv.DictWriter(f,headers)
    writer.writeheader()
    writer.writerows(students)

with open(csv_path,"r",newline='',encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for i in reader:
        # print(i)
        print(f"The Person {i["Name"]} has {i["grade"]} grade and has {i["Friends"]} Friends")
