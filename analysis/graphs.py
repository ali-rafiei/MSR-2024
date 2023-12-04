import json
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud
# pip3 install numpy
# pip3 install matplotlib
# pip3 install wordcloud


# Open and read the JSON file
with open('combined_data_final.json', 'r') as file:
    json_data = json.load(file)

# Initialize counters
chatgpt_question_label_counts = {}
chatgpt_context_label_counts = {}
chatgpt_keyword_label_counts = {}

stackoverflow_question_label_counts = {}
stackoverflow_context_label_counts = {}
stackoverflow_keyword_label_counts = {}

# Loop through each item in the JSON data
for item in json_data:
    # Check if "Conversations" key is present in the item
    if "Conversations" in item:
        # Iterate through each conversation in "Conversations"
        for conversation in item["Conversations"]:
            # Extract labels from the conversation
            question_labels = conversation.get("QuestionLabels", "")
            context_labels = conversation.get("ContextLabels", "")
            keyword_labels = conversation.get("KeywordLabels", "")

            # Update counts for ChatGPT QuestionLabels
            for label in question_labels.split(", "):
                chatgpt_question_label_counts[label] = chatgpt_question_label_counts.get(label, 0) + 1

            # Update counts for ChatGPT ContextLabels
            for label in context_labels.split(", "):
                chatgpt_context_label_counts[label] = chatgpt_context_label_counts.get(label, 0) + 1

            # Update counts for ChatGPT KeywordLabels
            for label in keyword_labels.split(", "):
                chatgpt_keyword_label_counts[label] = chatgpt_keyword_label_counts.get(label, 0) + 1
    else:
        # Extract labels from the item
        question_labels = item.get("QuestionLabels", "")
        context_labels = item.get("ContextLabels", "")
        keyword_labels = item.get("KeywordLabels", "")

        # Update counts for Stack Overflow QuestionLabels
        for label in question_labels.split(", "):
            stackoverflow_question_label_counts[label] = stackoverflow_question_label_counts.get(label, 0) + 1

        # Update counts for Stack Overflow ContextLabels
        for label in context_labels.split(", "):
            stackoverflow_context_label_counts[label] = stackoverflow_context_label_counts.get(label, 0) + 1

        # Update counts for Stack Overflow KeywordLabels
        for label in keyword_labels.split(", "):
            stackoverflow_keyword_label_counts[label] = stackoverflow_keyword_label_counts.get(label, 0) + 1

# Sort the label counts dictionaries from highest to lowest for each category
chatgpt_question_label_counts = dict(sorted(chatgpt_question_label_counts.items(), key=lambda item: item[1], reverse=True))
chatgpt_context_label_counts = dict(sorted(chatgpt_context_label_counts.items(), key=lambda item: item[1], reverse=True))
chatgpt_keyword_label_counts = dict(sorted(chatgpt_keyword_label_counts.items(), key=lambda item: item[1], reverse=True))

stackoverflow_question_label_counts = dict(sorted(stackoverflow_question_label_counts.items(), key=lambda item: item[1], reverse=True))
stackoverflow_context_label_counts = dict(sorted(stackoverflow_context_label_counts.items(), key=lambda item: item[1], reverse=True))
stackoverflow_keyword_label_counts = dict(sorted(stackoverflow_keyword_label_counts.items(), key=lambda item: item[1], reverse=True))

# Dictionaries are defined as the following
# chatgpt_question_label_counts = {'none of the above': 1422, 'Conceptual': 943, 'Review': 753, 'API Usage': 678, 'Discrepancy': 410, 'Errors': 312, 'Learning': 124, 'API Change': 73}
# chatgpt_context_label_counts = {'Task/Goal': 1684, 'Request for Explanation': 1554, 'none of the above': 1531, 'Code Snippet': 1380, 'Error Message': 325, 'Input/Output': 238}
# stackoverflow_question_label_counts = {'Discrepancy': 1716, 'Errors': 1064, 'Conceptual': 841, 'API Usage': 616, 'Review': 215, 'none of the above': 199, 'API Change': 77, 'Learning': 63}
# stackoverflow_context_label_counts = {'Request for Explanation': 3820, 'Code Snippet': 3620, 'Error Message': 1425, 'Task/Goal': 1218, 'Input/Output': 438, 'none of the above': 240}

def plot_double_bar_graph(dict1, dict2, title, filename):
    labels = list(set(list(dict1.keys()) + list(dict2.keys())))
    dict1_vals = [dict1.get(key, 0) for key in labels]
    dict2_vals = [dict2.get(key, 0) for key in labels]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, dict1_vals, width, label='ChatGPT', color='#add8e6')
    rects2 = ax.bar(x + width/2, dict2_vals, width, label='Stack Overflow', color='#ff7f7f')

    ax.set_ylabel('Counts')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    fig.tight_layout()
    plt.savefig(filename)

def plot_stacked_bar_graph(dict1, dict2, title, filename):
    labels = list(set(list(dict1.keys()) + list(dict2.keys())))
    dict1_vals = [dict1.get(key, 0) for key in labels]
    dict2_vals = [dict2.get(key, 0) for key in labels]

    x = np.arange(len(labels))

    fig, ax = plt.subplots()
    rects1 = ax.bar(x, dict1_vals, label='ChatGPT', color='#add8e6')
    rects2 = ax.bar(x, dict2_vals, bottom=dict1_vals, label='Stack Overflow', color='#ff7f7f')

    ax.set_ylabel('Counts')
    ax.set_title(title)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=45, ha='right')
    ax.legend()

    fig.tight_layout()
    plt.savefig(filename)


def plot_radar_chart(dict1, dict2, title, filename):
    labels = sorted(set(list(dict1.keys()) + list(dict2.keys())))
    dict1_vals = [dict1.get(key, 0) for key in labels]
    dict2_vals = [dict2.get(key, 0) for key in labels]

    num_vars = len(labels)
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))
    ax.fill(angles, dict1_vals, color='skyblue', alpha=0.6, edgecolor='black')  # Lighter color and edge color
    ax.fill(angles, dict2_vals, color='salmon', alpha=0.6, edgecolor='black')  # Lighter color and edge color

    ax.set_yticklabels([])
    ax.set_xticks(angles)
    ax.set_xticklabels(labels, fontsize=14)

    for label, angle in zip(ax.get_xticklabels(), angles):
        if angle in (0, np.pi):
            label.set_horizontalalignment('center')
        elif 0 < angle < np.pi:
            label.set_horizontalalignment('left')
        else:
            label.set_horizontalalignment('right')
        label.set_rotation_mode('anchor')
        label.set_rotation(angle * 180 / np.pi - 90)

    ax.set_title(title, size=24, color='black', y=1.1)
    ax.legend(['ChatGPT', 'Stack Overflow'], loc='upper right', bbox_to_anchor=(1.1, 1.1), fontsize=14)

    ax.grid(True)
    plt.tight_layout()
    plt.savefig(filename)

def generate_wordcloud(dict_counts, title, filename):
    wordcloud = WordCloud(background_color='white', width = 1000, height = 500).generate_from_frequencies(dict_counts)

    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud)
    plt.axis("off")
    # plt.title(title)
    plt.savefig(filename)

# Plotting double bar graphs
plot_double_bar_graph(chatgpt_question_label_counts, stackoverflow_question_label_counts, 'Question Labels Comparison', 'graphs/doublebar_question_labels.png')
plot_double_bar_graph(chatgpt_context_label_counts, stackoverflow_context_label_counts, 'Context Labels Comparison', 'graphs/doublebar_context_labels.png')

# # Plotting stacked bar graphs
# plot_stacked_bar_graph(chatgpt_question_label_counts, stackoverflow_question_label_counts, 'Question Labels Comparison', 'graphs/stackedbar_question_labels.png')
# plot_stacked_bar_graph(chatgpt_context_label_counts, stackoverflow_context_label_counts, 'Context Labels Comparison', 'graphs/stackedbar_context_labels.png')

# # Plotting radar chart graphs
# plot_radar_chart(chatgpt_question_label_counts, stackoverflow_question_label_counts, 'Question Labels Comparison', 'graphs/radar_question_labels.png')
# plot_radar_chart(chatgpt_context_label_counts, stackoverflow_context_label_counts, 'Context Labels Comparison', 'graphs/radar_context_labels.png')

# Create word clouds
generate_wordcloud(stackoverflow_keyword_label_counts, "StackOverflow Keyword Label Counts", 'graphs/wordcloud_stackoverflow.png')
generate_wordcloud(chatgpt_keyword_label_counts, "ChatGPT Keyword Label Counts", 'graphs/wordcloud_chatgpt.png')
