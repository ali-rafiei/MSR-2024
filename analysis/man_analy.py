import json
import random

# Set a random seed for reproducibility
random.seed(77)

manual_analysis = "gpt_labels"  # change string to either "gpt_labels" or "context_labels" depending on task

# Open and read the JSON file

if manual_analysis == "gpt_labels":
    with open('combined_data_final.json', 'r') as file:
        json_data = json.load(file)
    filename = 'man_analy2.json'

if manual_analysis == "context_labels":
    with open("refined_devgpt.json", "r") as file:
        devgpt_data = json.load(file)
    with open("refined_so.json", "r") as file:
        so_data = json.load(file)
    json_data = so_data + devgpt_data
    filename = 'man_analy1.json'


# Create a list of all conversations/items
all_items = []
for item in json_data:
    if "Conversations" in item:
        all_items.extend(item["Conversations"])
    else:
        all_items.append(item)

# Get a random sample of 96 items (statistically significant)
# Confidence Level 95% +- 10%
random_sample = random.sample(all_items, 96)

# Store the random sample in a new file
with open(filename, 'w') as output_file:
    json.dump(random_sample, output_file, indent=2)

print("Random sample stored in man_analy.json")
