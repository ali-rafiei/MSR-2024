import tiktoken
import json

# pip install tiktoken
# pip install openai

encoding = tiktoken.get_encoding("cl100k_base")
model = "cl100k_base"  # Specify the model or engine you plan to use
file_path = 'prompt.txt'
num = 0
count = 0

def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

try:
    with open(file_path, 'r') as file:
        prompt = file.read()
except FileNotFoundError:
    print(f"The file '{file_path}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")


def process_json(json_data):
    global num, count
    for item in json_data:
        if "Conversations" in item:
            for conversation in item["Conversations"]:
                content = conversation.get("Prompt")
                num += num_tokens_from_string(prompt+content+'"', model)
                count += 1
        else:
            content = item.get("Body") or item.get("Prompt")
            num += num_tokens_from_string(prompt+content+'"', model)
            count += 1

# Read and process the first JSON file (ChatGPT)
with open("refined_devgpt.json", "r") as file:
    devgpt_data = json.load(file)
    process_json(devgpt_data)

# Read and process the second JSON file (StackOverflow)
with open("refined_so.json", "r") as file:
    so_data = json.load(file)
    process_json(so_data)

print(f"Token count for all prompts: {num}")
print(f"Number of prompts: {count}")
print("Total price of tokens using gpt-3.5-turbo-1106 ($):", num/1000*0.0010)

