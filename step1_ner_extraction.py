from pathlib import Path
import spacy

def run_ner_pipeline(input_folder: str, window_size: int = 5):
    input_folder = Path(input_folder)
    output_folder = input_folder / "NER_output"
    output_folder.mkdir(exist_ok=True)

    nlp = spacy.load("en_core_web_sm")

    for file_path in input_folder.glob("*.txt"):
        print(f"Processing {file_path.name}...")
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()

        doc = nlp(text)
        tokens = [token.text for token in doc]
        lemmas = [token.lemma_ for token in doc]

        results = []

        for ent in doc.ents:
            start = ent.start
            end = ent.end
            before = lemmas[max(0, start - window_size):start]
            after = lemmas[end:end + window_size]
            context = " ".join(before + [f"[{ent.text}]"] + after)
            results.append(
                f"ENTITY: {ent.text}\n"
                f"LABEL: {ent.label_}\n"
                f"CONTEXT: {context}\n"
                f"{'-'*60}\n"
            )

        output_file = output_folder / f"{file_path.stem}_entities.txt"
        with open(output_file, "w", encoding="utf-8") as out:
            out.writelines(results)

    print("\nNER extraction done. Check the NER_output folder.")

if __name__ == "__main__":
    run_ner_pipeline(r"C:\Users\zheny\ma_thesis")
