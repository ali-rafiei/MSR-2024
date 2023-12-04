import json

# Open and read the original JSON file
with open('combined_data.json', 'r') as file:
    json_data = json.load(file)

# Define valid labels for Question and Context
valid_question_labels = ["API Usage", "Discrepancy", "Errors", "Review", "Conceptual", "API Change", "Learning", "none of the above"]
valid_context_labels = ["Code Snippet", "Input/Output", "Error Message", "Request for Explanation", "Task/Goal", "none of the above"]

# Filter out invalid labels from the JSON data
for item in json_data:
    if "Conversations" in item:
        for conversation in item["Conversations"]:
            # Filter out invalid Question Labels
            question_labels = [label for label in conversation.get("QuestionLabels", "").split(", ") if label in valid_question_labels]

            # Filter out invalid Context Labels
            context_labels = [label for label in conversation.get("ContextLabels", "").split(", ") if label in valid_context_labels]

            # Update conversation with filtered labels
            conversation["QuestionLabels"] = ", ".join(question_labels)
            conversation["ContextLabels"] = ", ".join(context_labels)
            if conversation["QuestionLabels"] == "":
                conversation["ErrorGPT"] = "something went wrong"
            if conversation["ContextLabels"] == "":
                conversation["ErrorGPT"] = "something went wrong"

    else:
        # Filter out invalid Question Labels
        question_labels = [label for label in item.get("QuestionLabels", "").split(", ") if label in valid_question_labels]

        # Filter out invalid Context Labels
        context_labels = [label for label in item.get("ContextLabels", "").split(", ") if label in valid_context_labels]

        # Update item with filtered labels
        item["QuestionLabels"] = ", ".join(question_labels)
        item["ContextLabels"] = ", ".join(context_labels)
        if item["QuestionLabels"] == "":
            item["ErrorGPT"] = "something went wrong"
        if item["ContextLabels"] == "":
            item["ErrorGPT"] = "something went wrong"

# Save the filtered JSON data to a new file
with open('combined_data.json', 'w') as output_file:
    json.dump(json_data, output_file, indent=2)

print("Filtered data saved to combined_data.json")
