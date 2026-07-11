import os
import spacy
import pandas as pd
from tqdm import tqdm

# =============================
# SETTINGS
# =============================
FOLDER_PATH = r"C:\Users\zheny\corpus_ma"

nlp = spacy.load("en_core_web_sm")

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
    doc = nlp(text)

    # Extract sentences
    sentences = list(doc.sents)
    num_sentences = len(sentences)

    # Compute sentence lengths (in words)
    if num_sentences > 0:
        lengths = [
            len([token for token in sent if token.is_alpha])
            for sent in sentences
        ]
        avg_length = sum(lengths) / num_sentences
    else:
        avg_length = 0

    results.append({
        "novel": file,
        "num_sentences": num_sentences,
        "avg_sentence_length_words": avg_length
    })

# =============================
# Save results
# =============================
df = pd.DataFrame(results)
df.to_csv("sentence_stats.csv", index=False)

print("\n✅ Done! Check sentence_stats.csv")