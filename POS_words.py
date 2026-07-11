import os
import spacy
from collections import Counter
import pandas as pd
from tqdm import tqdm
from wordcloud import WordCloud

# =============================
# SETTINGS
# =============================
FOLDER_PATH = r"C:\Users\zheny\corpus_ma"
TOP_N = 20
OUTPUT_DIR = "wordclouds"

nlp = spacy.load("en_core_web_sm")

# Create output folder
os.makedirs(OUTPUT_DIR, exist_ok=True)

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

    doc = nlp(text)

    nouns = Counter()
    verbs = Counter()
    adjs = Counter()
    advs = Counter()

    for token in doc:
        if not token.is_alpha or token.is_stop:
            continue

        lemma = token.lemma_.lower()

        if token.pos_ == "NOUN":
            nouns[lemma] += 1
        elif token.pos_ == "VERB":
            verbs[lemma] += 1
        elif token.pos_ == "ADJ":
            adjs[lemma] += 1
        elif token.pos_ == "ADV":
            advs[lemma] += 1

    total_verbs = sum(verbs.values())
    unique_verbs = len(verbs)

    # Save top-20 results
    results.append({
        "novel": file,
        "total_verbs": total_verbs,
        "unique_verbs": unique_verbs,
        "top_nouns": nouns.most_common(TOP_N),
        "top_verbs": verbs.most_common(TOP_N),
        "top_adjectives": adjs.most_common(TOP_N),
        "top_adverbs": advs.most_common(TOP_N)
    })

    # =============================
    # Generate word clouds
    # =============================
    def save_wordcloud(counter, name):
        if not counter:
            return
        wc = WordCloud(width=800, height=400, background_color="white")
        wc.generate_from_frequencies(counter)

        filename = f"{file.replace('.txt', '')}_{name}.png"
        wc.to_file(os.path.join(OUTPUT_DIR, filename))

    save_wordcloud(nouns, "nouns")
    save_wordcloud(verbs, "verbs")
    save_wordcloud(adjs, "adjectives")
    save_wordcloud(advs, "adverbs")

# =============================
# Save CSV
# =============================
df = pd.DataFrame(results)
df.to_csv("pos_top20_words_new.csv", index=False)

print("\n✅ Done! Check CSV and wordcloud images.")