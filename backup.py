import json
from pathlib import Path

backup_file = "backup.json"
input_file = "input.json"

links_set = set()
with open(backup_file, "r") as f:
    backup_data = json.load(f)
    
with open(input_file, "r") as f:
    input_data = json.load(f)

joint_data = []

for data in backup_data:
    if data["url"] not in links_set:
        joint_data.append(data)
        links_set.add(data["url"])

for data in input_data:
    if data["url"] not in links_set:
        joint_data.append(data)
        links_set.add(data["url"])

joint_data.sort(key=lambda x: (x["genre"], x["artist"]))

with open(backup_file, "w") as joint_file:
    json.dump(joint_data, joint_file, indent=4)

with open(input_file, "w") as f:
    f.write("[]")
