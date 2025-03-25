import json
import os
from datetime import datetime

# Define date range
start_date = datetime.strptime("2023-03-15", "%Y-%m-%d")
end_date = datetime.strptime("2023-10-28", "%Y-%m-%d")


# Normalize timestamp
def normalize_timestamp(timestamp):
    try:
        if "." in timestamp:
            parts = timestamp.split(".")
            if len(parts[1]) < 3:
                parts[1] = parts[1].ljust(3, '0')
            timestamp = ".".join(parts)
        return datetime.fromisoformat(timestamp)
    except ValueError:
        return None

    # Filter messages in JSON file


def filter_messages(file_path, output_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    if "messages" in data:
        filtered_messages = [
            message for message in data["messages"]
            if "timestamp" in message and (timestamp := normalize_timestamp(message["timestamp"].split('+')[0])) and (
                        start_date <= timestamp <= end_date)
        ]
        data["messages"] = filtered_messages

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)


# Process all JSON files in the directory
input_directory = "discordout-2025-01"
output_directory = "filtered"

for file_name in os.listdir(input_directory):
    if file_name.endswith(".json"):
        input_file_path = os.path.join(input_directory, file_name)
        output_file_name = file_name.replace(".json", "_filtered.json")
        output_file_path = os.path.join(output_directory, output_file_name)
        filter_messages(input_file_path, output_file_path)
        print(f"Filtered data has been saved to {output_file_path}")
