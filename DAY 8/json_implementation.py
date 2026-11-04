import json
from pathlib import Path

json_path = Path("DAY 8/data/users.json")

user_profile = {
    "username":"Hamza",
    "coding ability":"Decently Poor",
    "skills":["Python,SQL,FastAPI"]
}

with open(json_path,"w",encoding="utf-8") as f:
    json.dump(user_profile,f,indent=4)

with open(json_path,"r",encoding="utf-8") as f:
    data = json.load(f)
    print([data["skills"]])
