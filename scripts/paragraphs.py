import os
import pandas as pd
from tqdm import tqdm

FOLDER_PATH = r"C:\Users\zheny\corpus_ma"

def get_paragraphs(text):
    # Split on empty lines (handles multiple newline styles)
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    return paragraphs

def paragraph_word_length(paragraph):
    return len(paragraph.split())

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

    paragraphs = get_paragraphs(text)
    num_paragraphs = len(paragraphs)

    if num_paragraphs > 0:
        lengths = [paragraph_word_length(p) for p in paragraphs]
        avg_length = sum(lengths) / num_paragraphs
    else:
        avg_length = 0

    results.append({
        "novel": file,
        "num_paragraphs": num_paragraphs,
        "avg_paragraph_length_words": avg_length
    })


df = pd.DataFrame(results)
df.to_csv("paragraph_stats.csv", index=False)

print("\n✅ Done! Check paragraph_stats.csv")