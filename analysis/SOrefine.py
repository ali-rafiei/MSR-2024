import re
import json
import random

def extract_entries(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
        # Use a regular expression to find entries that match the specified format
        entries = re.findall(r'<row\s(.*?)\s\/>', content, re.DOTALL)
    return entries

def random_sample(entries, sample_size, seed):
    random.seed(seed)
    return random.sample(entries, sample_size)

def organize_entries(selected_entries):
    organized_entries = []
    for entry in selected_entries:
        # Use regular expressions to extract relevant attributes
        entry_data = dict(re.findall(r'(\S+?)="([^"]*)"', entry))
        entry_info = {
            "Post ID": entry_data.get("Id"),
            "Type": "Question" if entry_data.get("PostTypeId") == "1" else "Answer",
            "Accepted Answer ID": entry_data.get("AcceptedAnswerId"),
            "Creation Date": entry_data.get("CreationDate"),
            "Score": entry_data.get("Score"),
            "View Count": entry_data.get("ViewCount"),
            "Title": entry_data.get("Title"),
            "Tags": entry_data.get("Tags"),
            "Owner User ID": entry_data.get("OwnerUserId"),
            "Last Editor User ID": entry_data.get("LastEditorUserId"),
            "Answer Count": entry_data.get("AnswerCount"),
            "Comment Count": entry_data.get("CommentCount"),
            "Last Edit Date": entry_data.get("LastEditDate"),
            "Last Activity Date": entry_data.get("LastActivityDate"),
            "Content License": entry_data.get("ContentLicense"),
            "Body": entry_data.get("Body"),
        }
        organized_entries.append(entry_info)
    return organized_entries

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=2)

# File paths
input_file = 'so.txt'
output_file = 'refined_so.json'

# Random sampling parameters
sample_size = 4688
random_seed = 77

# Extract entries from the file
all_entries = extract_entries(input_file)

# Randomly sample entries
selected_entries = random_sample(all_entries, sample_size, random_seed)

# Organize selected entries
organized_entries = organize_entries(selected_entries)

# Save to JSON file
save_to_json(organized_entries, output_file)
