import json

#Open input file
def convert_json_to_txt(input_file, output_file):
  with open(input_file, 'r') as json_file:
    data = json.load(json_file)

  with open(output_file, 'w') as txt_file:
    for message in data.get("messages", []):
      #get message details
      timestamp = message.get("timestamp", "No Timestamp")
      author = message.get("author", {})
      author_name = author.get("nickname") or f"{author.get('name', 'Unknown Author')}#{author.get('discriminator', '0000')}"
      content = message.get("content", "[No Content]")
            
      #write message details
      txt_file.write(f"[{timestamp}] {author_name}\n")
      txt_file.write(f"Content: {content}\n")

      #Stickers
      stickers = message.get("stickers", [])
      for sticker in stickers:
        sticker_name = sticker.get("name", "Unknown Sticker")
        sticker_format = sticker.get("format", "Unknown Format")
        txt_file.write(f"Sticker: {sticker_name} (Format: {sticker_format})\n")
            
      #Attachments
      attachments = message.get("attachments", [])
      for attachment in attachments:
        txt_file.write(f"Attachment: {attachment.get('url', '[No URL]')}\n")
            
      #Reactions
      reactions = message.get("reactions", [])
      if reactions:
        reaction_summary = ', '.join([f"{reaction['emoji']} ({reaction['count']})" for reaction in reactions])
        txt_file.write(f"Reactions: {reaction_summary}\n")
            
      #Add blank line between messages
      txt_file.write("\n")

  print(f"Converted JSON data has been saved to {output_file}")

input_file = "/content/Vesuvius Challenge - Text Channels - papyrology [1108134343295127592]_filtered.json"
output_file = "/content/Vesuvius Challenge - Text Channels - papyrology [1108134343295127592]_filtered.txt"
convert_json_to_txt(input_file, output_file)
