import json

def does_not_match_substrings(my_string, substrings):
    for substring in substrings:
        if substring in my_string:
            return False
    return True

# Read filtered_data.json
with open('filtered_data.json', 'r') as file:
    filtered_data = json.load(file)

# Define the valid months and days
valid_dates = ["October"]
for number in range(4, 31):    # data dump ends on sep 12, but last entry in data is sep 3
    september_string = f"September {number}"
    valid_dates.append(september_string)

# Refine data by excluding entries with invalid DateOfConversation strings
refined_data = {"Sources": []}
for source in filtered_data["Sources"]:
    chatgpt_sharing = source.get("ChatgptSharing", [])

    for chatgpt_data in chatgpt_sharing:
        DateOfConversation = chatgpt_data.get("DateOfConversation", [])
        if does_not_match_substrings(DateOfConversation, valid_dates):
            refined_data["Sources"].append(source)
            break

# Convert the set of unique sources back to a list of JSON objects
english_sources = list(refined_data["Sources"])

# Convert the format of "filtered_data" to the specified structure
formatted_refined_data = []

for source in english_sources:
    chatgpt_sharing = source.get("ChatgptSharing", [])

    for chatgpt_data in chatgpt_sharing:
        formatted_item = {
            "URL": chatgpt_data.get("URL", ""),
            "MentionedURL": chatgpt_data.get("Mention", {}).get("MentionedURL", ""),
            "MentionedProperty": chatgpt_data.get("Mention", {}).get("MentionedProperty", ""),
            "MentionedAuthor": chatgpt_data.get("Mention", {}).get("MentionedAuthor", ""),
            "MentionedText": chatgpt_data.get("Mention", {}).get("MentionedText", ""),
            "Status": chatgpt_data.get("Status", 200),
            "DateOfConversation": chatgpt_data.get("DateOfConversation", ""),
            "DateOfAccess": chatgpt_data.get("DateOfAccess", ""),
            "Title": chatgpt_data.get("Title", ""),
            "NumberOfPrompts": chatgpt_data.get("NumberOfPrompts", 0),
            "TokensOfPrompts": chatgpt_data.get("TokensOfPrompts", 0),
            "TokensOfAnswers": chatgpt_data.get("TokensOfAnswers", 0),
            "Model": chatgpt_data.get("Model", ""),
            "Conversations": [{"Prompt": conversation.get("Prompt", "")} for conversation in chatgpt_data.get("Conversations", [])]
        }
        formatted_refined_data.append(formatted_item)

# Write refined data to a new JSON file
with open('refined_devgpt.json', 'w') as outfile:
    json.dump(formatted_refined_data, outfile, indent=4)

print("Refined data has been saved to 'refined_data.json' excluding invalid DateOfConversation entries.")
