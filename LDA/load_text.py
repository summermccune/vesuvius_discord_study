import json
from tqdm import tqdm

# Initialize a list to hold the text of messages with type "Default"
sample_text = []

# Path to your JSON file
json_file = "/Users/nikhil/PycharmProjects/vesuvius_discord_study/JSON_filter/filtered/Vesuvius Challenge - Text Channels - speculation [1164719267565027399]_filtered.json"

# Open and load the JSON file
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

# Get the list of messages (default to empty list if key is missing)
messages = data.get("messages", [])

# Process each message with a progress bar
for message in tqdm(messages, desc="Processing messages"):
    # Check if the message type is "Default"
    if message.get("type") == "Default":
        content = message.get("content", "")
        if content:  # Only add non-empty content
            sample_text.append(content)

print(f"Collected {len(sample_text)} messages with type 'Default'.")
