import json

import together


with open("jokes_dataset.json", "r") as f:
    jokes_list = json.load(f)["jokes_list"]

print("Sample from dataset:")
print(">" * 10)
print(jokes_list[:5])
print("<" * 10)

together.Files.save_jsonl(jokes_list, "converted_jokes.jsonl")
