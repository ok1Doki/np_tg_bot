import json

# Read JSON data from file
with open('getCities.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# Process data
output = []
for item in data:
    settlement_type_desc = item['SettlementTypeDescription']
    description = item['Description']
    item['Modified_description'] = f"{settlement_type_desc} {description}"
    output.append(item)

# Write tuples to output file
with open('output.json', 'w', encoding='utf-8') as output_file:
    json.dump(output, output_file, indent=2, ensure_ascii=False)

print("output written to 'output_tuples.json'")
