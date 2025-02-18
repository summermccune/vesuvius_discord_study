import json
import re
import spacy
import nltk
nltk.download('stopwords')
import gensim
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
import matplotlib.pyplot as plt
from gensim.utils import simple_preprocess
from gensim.corpora.dictionary import Dictionary
from gensim.models.ldamodel import LdaModel
from nltk.corpus import stopwords
from tqdm import tqdm

# Load spaCy model for lemmatization
nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

# Path to your JSON file
json_file = "/Users/nikhil/PycharmProjects/vesuvius_discord_study/JSON_filter/filtered/Vesuvius Challenge - Text Channels - general [1079907750265499772]_filtered.json"

# Load JSON and extract messages
sample_text = []

with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

messages = data.get("messages", [])

for message in tqdm(messages, desc="Processing messages"):
    if message.get("type") == "Default":
        content = message.get("content", "")
        if content:
            sample_text.append(content)

print(f"Collected {len(sample_text)} messages with type 'Default'.")

# Preprocessing function
def preprocess_text(text):
    text = re.sub(r"http\S+|www\S+|@\S+", "", text)  # Remove links and mentions
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Keep only letters
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    words = simple_preprocess(text, deacc=True)  # Tokenization
    words = [word for word in words if word not in stop_words]  # Remove stopwords
    words = [nlp(word)[0].lemma_ for word in words]  # Lemmatization
    return words

# Apply preprocessing to all messages
processed_texts = [preprocess_text(msg) for msg in sample_text]

# Create Dictionary and Corpus
dictionary = Dictionary(processed_texts)
corpus = [dictionary.doc2bow(text) for text in processed_texts]

# Train LDA Model
num_topics = 5  # Change based on how many topics you want
lda_model = LdaModel(corpus=corpus, id2word=dictionary, num_topics=num_topics, passes=10, random_state=42)

# Print topics
print("\nTop Topics Found:\n")
for idx, topic in lda_model.print_topics():
    print(f"Topic {idx}: {topic}")

# Function to assign topics to messages
def get_topic(text):
    bow = dictionary.doc2bow(preprocess_text(text))
    topics = lda_model.get_document_topics(bow)
    return max(topics, key=lambda x: x[1])[0] if topics else None

# Assign topics to each message
chat_topics = [(msg, get_topic(msg)) for msg in sample_text]

# Save topic results to a file
output_file = "discord_chat_topics.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(chat_topics, f, indent=4)

print(f"\nTopic assignments saved to {output_file}")

# Visualize with pyLDAvis
vis = gensimvis.prepare(lda_model, corpus, dictionary)
pyLDAvis.save_html(vis, "lda_visualization.html")
print("LDA visualization saved as lda_visualization.html")
pyLDAvis.display(vis)
