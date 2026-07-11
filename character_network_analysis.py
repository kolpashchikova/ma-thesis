import os
import spacy
from collections import Counter
import networkx as nx
import pandas as pd
from tqdm import tqdm

# =============================
# SETTINGS
# =============================
FOLDER_PATH = r"C:\Users\zheny\corpus_ma"
MIN_FREQUENCY = 5

nlp = spacy.load("en_core_web_sm")

# =============================
# Extract characters
# =============================
def extract_characters(doc):
    return [ent.text for ent in doc.ents if ent.label_ == "PERSON"]


# =============================
# Normalize names
# =============================
def normalize_names(characters, min_freq=5):
    counts = Counter(characters)
    return Counter({c: n for c, n in counts.items() if n >= min_freq})


# =============================
# Build network (sentence-based)
# =============================

def build_network(doc):
    G = nx.Graph()

    for sent in doc.sents:
        chars = [ent.text for ent in sent.ents if ent.label_ == "PERSON"]
        unique_chars = list(set(chars))

        # 🚨 skip if too many names (likely noise)
        if len(unique_chars) > 10:
            continue

        for i in range(len(unique_chars)):
            for j in range(i + 1, len(unique_chars)):
                c1, c2 = unique_chars[i], unique_chars[j]

                if G.has_edge(c1, c2):
                    G[c1][c2]["weight"] += 1
                else:
                    G.add_edge(c1, c2, weight=1)

    nx.write_gexf(G, file.replace(".txt", ".gexf"))

    return G


# =============================
# Process files
# =============================
results = []

files = [f for f in os.listdir(FOLDER_PATH) if f.endswith(".txt")]

if not files:
    print("❌ No .txt files found in folder!")
    exit()

for file in tqdm(files):
    path = os.path.join(FOLDER_PATH, file)

    with open(path, "r", encoding="utf-8") as f:
        text = f.read()

    print(f"\n📖 Processing: {file}")

    # Run spaCy
    print("Starting spaCy...")
    doc = nlp(text)
    print("Finished spaCy!")

    # Extract + count
    characters = extract_characters(doc)
    char_counts = normalize_names(characters, MIN_FREQUENCY)

    print("Number of sentences:", len(list(doc.sents)))
    # Build graph
    G = build_network(doc)

    # Stats
    num_characters = len(char_counts)
    density = nx.density(G) if len(G.nodes) > 1 else 0

    results.append({
        "novel": file,
        "num_characters": num_characters,
        "density": density,
        "top_characters": char_counts.most_common(5)
    })


# =============================
# Save results
# =============================
df = pd.DataFrame(results)
df.to_csv("character_network_results.csv", index=False)

print("\n✅ Done! Check character_network_results.csv")