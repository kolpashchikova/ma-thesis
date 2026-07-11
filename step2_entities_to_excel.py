from pathlib import Path
from openpyxl import Workbook

def convert_entities_to_excel(input_folder: str, output_file: str):
    input_folder = Path(input_folder)
    wb = Workbook()
    ws = wb.active
    ws.title = "NamedEntities"
    ws.append(["source_file", "entity", "label", "context"])

    for file_path in input_folder.glob("*_entities.txt"):
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

    wb.save(output_file)
    print(f"Excel file saved: {output_file}")

if __name__ == "__main__":
    convert_entities_to_excel(
        r"C:\Users\zheny\ma_thesis\NER_output",
        r"C:\Users\zheny\ma_thesis\NER_output\all_entities.xlsx"
    )
