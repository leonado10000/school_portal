import json
import csv

# Load JSON from dumpdata
with open('all_data_utf_8.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Group rows by model name
models_data = {}
for obj in data:
    model_name = obj['model'].split('.')[-1]
    # Insert id from "pk" into the fields dict
    fields_with_id = {"id": obj["pk"], **obj["fields"]}
    models_data.setdefault(model_name, []).append(fields_with_id)

# Save each model to CSV
for model, rows in models_data.items():
    with open(f"{model}.csv", 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"✅ Exported {model}.csv with id column")
