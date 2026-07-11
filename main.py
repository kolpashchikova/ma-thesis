from pathlib import Path
import spacy
from openpyxl import Workbook

RAW_TEXTS_FOLDER = Path(r"C:\Users\zheny\ma_thesis")   
NER_OUTPUT_FOLDER = RAW_TEXTS_FOLDER / "NER_output"     
EXCEL_OUTPUT_FILE = NER_OUTPUT_FOLDER / "all_entities.xlsx"
WINDOW_SIZE = 7

def run_ner_pipeline():
    NER_OUTPUT_FOLDER.mkdir(exist_ok=True)
    nlp = spacy.load("en_core_web_sm")

    for file_path in RAW_TEXTS_FOLDER.glob("*.txt"):
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
            before = tokens[max(0, start - WINDOW_SIZE):start]
            after = tokens[end:end + WINDOW_SIZE]
            context = " ".join(before + [f"[{ent.text}]"] + after)
            results.append(
                f"ENTITY: {ent.text}\n"
                f"LABEL: {ent.label_}\n"
                f"CONTEXT: {context}\n"
                f"{'-'*60}\n"
            )

        output_file = NER_OUTPUT_FOLDER / f"{file_path.stem}_entities.txt"
        with open(output_file, "w", encoding="utf-8") as out:
            out.writelines(results)

    print("\nNER extraction done. Check the NER_output folder.")


def convert_entities_to_excel():
    wb = Workbook()
    ws = wb.active
    ws.title = "NamedEntities"
    ws.append(["source_file", "entity", "label", "context"])

    for file_path in NER_OUTPUT_FOLDER.glob("*_entities.txt"):
        source_name = file_path.stem.replace("_entities", "")
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        entity = label = context = None
        for line in lines:
            line = line.strip()
            if line.startswith("ENTITY:"):
                entity = line.replace("ENTITY:", "").strip()
            elif line.startswith("LABEL:"):
                label = line.replace("LABEL:", "").strip()
            elif line.startswith("CONTEXT:"):
                context = line.replace("CONTEXT:", "").strip()
                if entity and label and context:
                    ws.append([source_name, entity, label, context])
                    entity = label = context = None

    wb.save(EXCEL_OUTPUT_FILE)
    print(f"Excel file saved: {EXCEL_OUTPUT_FILE}")


if __name__ == "__main__":
    run_ner_pipeline()

    convert_entities_to_excel()





