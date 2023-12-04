import json
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
# pip install langdetect

# List of JSON file paths
file_paths = ['DevGPT/snapshot_20230727/20230727_195816_hn_sharings.json', 'DevGPT/snapshot_20230727/20230727_195927_pr_sharings.json', 'DevGPT/snapshot_20230727/20230727_195941_issue_sharings.json', 'DevGPT/snapshot_20230727/20230727_195954_discussion_sharings.json', 'DevGPT/snapshot_20230727/20230727_200003_commit_sharings.json', 'DevGPT/snapshot_20230803/20230803_093947_pr_sharings.json', 'DevGPT/snapshot_20230803/20230803_094705_issue_sharings.json', 'DevGPT/snapshot_20230803/20230803_094811_discussion_sharings.json', 'DevGPT/snapshot_20230803/20230803_095317_commit_sharings.json', 'DevGPT/snapshot_20230803/20230803_105332_hn_sharings.json', 'DevGPT/snapshot_20230810/20230810_123110_pr_sharings.json', 'DevGPT/snapshot_20230810/20230810_123938_issue_sharings.json', 'DevGPT/snapshot_20230810/20230810_124048_discussion_sharings.json', 'DevGPT/snapshot_20230810/20230810_124807_commit_sharings.json', 'DevGPT/snapshot_20230810/20230810_134011_hn_sharings.json', 'DevGPT/snapshot_20230817/20230817_125147_pr_sharings.json', 'DevGPT/snapshot_20230817/20230817_130502_issue_sharings.json', 'DevGPT/snapshot_20230817/20230817_130721_discussion_sharings.json', 'DevGPT/snapshot_20230817/20230817_131244_commit_sharings.json', 'DevGPT/snapshot_20230817/20230817_170022_hn_sharings.json', 'DevGPT/snapshot_20230824/20230824_100450_pr_sharings.json', 'DevGPT/snapshot_20230824/20230824_101836_issue_sharings.json', 'DevGPT/snapshot_20230824/20230824_102000_discussion_sharings.json', 'DevGPT/snapshot_20230824/20230824_102435_commit_sharings.json', 'DevGPT/snapshot_20230824/20230824_112153_hn_sharings.json', 'DevGPT/snapshot_20230831/20230831_060603_pr_sharings.json', 'DevGPT/snapshot_20230831/20230831_061759_issue_sharings.json', 'DevGPT/snapshot_20230831/20230831_061926_discussion_sharings.json', 'DevGPT/snapshot_20230831/20230831_063412_commit_sharings.json', 'DevGPT/snapshot_20230831/20230831_073827_hn_sharings.json', 'DevGPT/snapshot_20230907/20230907_091631_pr_sharings.json', 'DevGPT/snapshot_20230907/20230907_092956_issue_sharings.json', 'DevGPT/snapshot_20230907/20230907_093129_discussion_sharings.json', 'DevGPT/snapshot_20230907/20230907_110036_commit_sharings.json', 'DevGPT/snapshot_20230907/20230907_123434_hn_sharings.json', 'DevGPT/snapshot_20230914/20230914_074826_pr_sharings.json', 'DevGPT/snapshot_20230914/20230914_080417_issue_sharings.json', 'DevGPT/snapshot_20230914/20230914_080601_discussion_sharings.json', 'DevGPT/snapshot_20230914/20230914_083202_commit_sharings.json', 'DevGPT/snapshot_20230914/20230914_105439_hn_sharings.json', 'DevGPT/snapshot_20231012/20231012_230826_commit_sharings.json', 'DevGPT/snapshot_20231012/20231012_232232_hn_sharings.json', 'DevGPT/snapshot_20231012/20231012_233628_pr_sharings.json', 'DevGPT/snapshot_20231012/20231012_235128_issue_sharings.json', 'DevGPT/snapshot_20231012/20231012_235320_discussion_sharings.json']  # Add more file paths if needed

# Read JSON files
data_list = []
for file_path in file_paths:
    with open('../'+file_path, 'r') as file:
        data = json.load(file)
        data_list.append(data)

# Check if prompt is in English and filter sources (ensuring uniqueness based on URL)
encountered_urls = set()  # Set to store encountered URLs
encountered_sources = set()  # Set to store encountered source objects
filtered_out_sources = []  # List to store filtered out sources

for data in data_list:
    for source in data["Sources"]:
        chatgpt_sharing = source.get("ChatgptSharing", [])
        for chatgpt_data in chatgpt_sharing:
            url = chatgpt_data.get("URL", "")
            conversations = chatgpt_data.get("Conversations", [])
            for conversation in conversations:
                prompt = conversation.get("Prompt", "")
                if prompt and len(prompt) > 0:  # Check if prompt is not empty
                    try:
                        detected_language = detect(prompt)
                        # Check if the URL is not in encountered URLs and is not a repeat
                        if (
                            url not in encountered_urls and
                            not any(item['Source']['ChatgptSharing'][0]['URL'] == url for item in filtered_out_sources)
                        ):
                            if detected_language != 'en':
                                filtered_out_sources.append({"Source": source, "DetectedLanguage": detected_language})
                            else:
                                encountered_urls.add(url)
                                encountered_sources.add(json.dumps(source))
                    except LangDetectException:
                        filtered_out_sources.append({"Source": source, "DetectedLanguage": None})

# Convert the set of unique sources back to a list of JSON objects
english_sources = [json.loads(source) for source in encountered_sources]

# Write filtered data to a new JSON file
filtered_data = {"Sources": english_sources}
with open('filtered_data.json', 'w') as outfile:
    json.dump(filtered_data, outfile, indent=4)

# Write filtered out data to another JSON file with detected language information
filtered_out_data = {"Sources": filtered_out_sources}
with open('filtered_out_data.json', 'w') as outfile:
    json.dump(filtered_out_data, outfile, indent=4)

print("Filtered data with unique entries has been saved to 'filtered_data.json'.")
print("Filtered out data with detected language information has been saved to 'filtered_out_data.json'.")
