import json
from datetime import datetime
from uuid import uuid4
import collections
import matplotlib.pyplot as plt

from langchain.docstore.document import Document
from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores.utils import filter_complex_metadata

# ----------------------------
# Parameters
# ----------------------------
# Set the grouping threshold in seconds (here, approx. 16.6 minutes = 1000 seconds)
TIME_THRESHOLD_SECONDS = 1000

# ----------------------------
# Load and sort messages
# ----------------------------
import glob, os

# ----------------------------
# Load all JSONs in a folder and sort messages
# ----------------------------
all_messages = []
for path in glob.glob(os.path.join("/Users/nikhil/PycharmProjects/vesuvius_discord_study/JSON_filter/filtered", "*.json")):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        all_messages.extend(data.get("messages", []))

# Now sort them by timestamp as before
messages = all_messages
messages.sort(key=lambda x: x["timestamp"])


def parse_timestamp(ts_str):
    # Assumes ISO 8601 format; adjust if necessary.
    return datetime.fromisoformat(ts_str)

# ----------------------------
# Group messages by time proximity.
# ----------------------------
groups = []
current_group = []
prev_time = None

for msg in messages:
    try:
        msg_time = parse_timestamp(msg["timestamp"])
    except Exception:
        # Skip messages with unparseable timestamps.
        continue

    if prev_time is None:
        current_group.append(msg)
    else:
        # If the time difference is within the threshold, group the message together.
        if (msg_time - prev_time).total_seconds() <= TIME_THRESHOLD_SECONDS:
            current_group.append(msg)
        else:
            groups.append(current_group)
            current_group = [msg]
    prev_time = msg_time

if current_group:
    groups.append(current_group)

# ----------------------------
# Generate a bar graph for the frequency distribution.
# ----------------------------
# Compute the number of messages in each chunk.
chunk_sizes = [len(group) for group in groups]
# Count the frequency of each chunk size.
size_counts = collections.Counter(chunk_sizes)
# Sort the keys for plotting.
keys = sorted(size_counts.keys())
values = [size_counts[k] for k in keys]

plt.bar(keys, values)
plt.xlabel("Number of Messages in Chunk")
plt.ylabel("Frequency (Number of Chunks)")
plt.title("Distribution of Messages per Chunk")
plt.xlim(0, 100)
plt.ylim(0, 2000)
plt.show()

# ----------------------------
# Create Document objects with metadata.
# ----------------------------
docs = []
for group in groups:
    content_lines = []
    authors = set()
    for msg in group:
        author_info = msg.get("author", {})
        # Use 'nickname' if available; otherwise, 'name'. Defaults to "Unknown".
        author_display = author_info.get("nickname") or author_info.get("name", "Unknown")
        authors.add(author_display)
        # Construct a line with timestamp, author, and content.
        line = f'{msg["timestamp"]} - {author_display}: {msg.get("content", "")}'
        content_lines.append(line)
    group_content = "\n".join(content_lines)
    # Store the list of authors in metadata.
    doc = Document(page_content=group_content, metadata={"authors": list(authors)})
    docs.append(doc)

print(f"Created {len(docs)} document chunks from the grouped messages.")

# ----------------------------
# Filter out complex metadata.
# ----------------------------
filtered_docs = filter_complex_metadata(docs)

# ----------------------------
# Store documents in the vector store.
# ----------------------------
embedding_model = HuggingFaceEmbeddings()
database_loc = "./chroma_db_test6"
vector_store = Chroma(embedding_function=embedding_model, persist_directory=database_loc)

uuids = [str(uuid4()) for _ in range(len(filtered_docs))]
vector_store.add_documents(filtered_docs, ids=uuids)

print("Documents have been added to the vector store.")
