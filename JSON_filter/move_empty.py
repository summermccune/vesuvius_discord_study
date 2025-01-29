import os
import json
import shutil

filtered_directory = "filtered"
empty_directory = "empty_files"

os.makedirs(empty_directory, exist_ok=True)

for file_name in os.listdir(filtered_directory):
    if file_name.endswith(".json"):
        file_path = os.path.join(filtered_directory, file_name)

        with open(file_path, 'r') as file:
            data = json.load(file)

        if "messages" in data and not data["messages"]:
            new_path = os.path.join(empty_directory, file_name)
            shutil.move(file_path, new_path)
            print(f"Moved empty file: {file_name} to {empty_directory}")
