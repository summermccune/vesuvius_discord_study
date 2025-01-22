import json
from datetime import datetime

start_date = datetime.strptime("2023-03-15", "%Y-%m-%d")
end_date = datetime.strptime("2024-02-16", "%Y-%m-%d")

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

def filter_messages(file_path, output_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    if "messages" in data:
        filtered_messages = [
            message for message in data["messages"]
            if "timestamp" in message and (timestamp := normalize_timestamp(message["timestamp"].split('+')[0])) and (start_date <= timestamp <= end_date)
        ]
        data["messages"] = filtered_messages

    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)

input_file = "Vesuvius Challenge - Text Channels - papyrology [1108134343295127592].json"
output_file = "Vesuvius Challenge - Text Channels - papyrology [1108134343295127592]_filtered.json"  

filter_messages(input_file, output_file)

print(f"Filtered data has been saved to {output_file}")
