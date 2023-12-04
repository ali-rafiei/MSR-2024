import json

# Open the JSON file and load the data
with open('20231012_235320_discussion_sharings.json', 'r') as json_file:
    data = json.load(json_file)

# Get the length of the "Sources" array
sources_length = len(data.get('Sources', []))

# Print the length of the "Sources" array
print(f"Length of 'Sources' array: {sources_length}")