import json

# Read JSON data from the file
with open('20231012_235320_discussion_sharings.json', 'r') as file:
    data = json.load(file)

# Access the list of sources
sources = data.get("Sources", [])
i = 0
# Iterate through the sources and print information from ChatgptSharing
for source in sources:
    chatgpt_sharing_objects = source.get("ChatgptSharing", [])  # Access ChatgptSharing inside each source object
    i += 1
    # Iterate through ChatgptSharing objects and print information
    for sharing_object in chatgpt_sharing_objects:
        sharing_url = sharing_object.get("URL", "N/A")
        # title = sharing_object.get("Title", "N/A")
        # number_of_prompts = sharing_object.get("NumberOfPrompts", "N/A")
        # tokens_of_answers = sharing_object.get("TokensOfAnswers", "N/A")

        print(i,"Sharing URL:", sharing_url)
        # print("Title:", title)
        # print("Number of Prompts:", number_of_prompts)
        # print("Tokens of Answers:", tokens_of_answers)
        print("---------------------------")
