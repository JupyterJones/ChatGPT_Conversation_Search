#!/home/jack/miniconda3/envs/cloned_base/bin/python
import json
import logging
import os
import glob
import subprocess
import os
import string


def clean_title(title):
    valid_chars = set(string.ascii_letters + string.digits + string.whitespace)
    cleaned_title = ''.join(char if char in valid_chars else '_' for char in title)
    cleaned_title = cleaned_title.replace(' ', '_')  # Replace spaces with underscores
    return cleaned_title.strip()

# make a function tooocreate folder if it doesn't exist
'''
This code defines a function make_path_exist that takes a directory path as input and creates the directory if it does not already exist. It then calls this function three times with different directory names.
'''
def make_path_exist(directory):
    path = os.path.join(os.getcwd(), directory)
    if not os.path.exists(path):
        os.makedirs(path)




def split_and_save_and_convert(conversations_file):
    directory1 = 'CHATGPT/JSON'
    make_path_exist(directory1)
    directory2 = 'CHATGPT/HTML'
    make_path_exist(directory2)
    directory3 = 'CHATGPT/TEXT'
    make_path_exist(directory3)
    try:
        with open(conversations_file, 'r', encoding='utf-8') as file:
            data = json.load(file)
            
            for conversation in data:
                title = conversation.get('title', 'Unknown_Title')
                title_with_underscores = clean_title(title)
                chapter_filename = f"{title_with_underscores}.json"
                chapter_filepath = os.path.join(directory1, chapter_filename)
                
                logging.info(f"Saving data for conversation '{title}' to {chapter_filepath}")
                
                with open(chapter_filepath, 'w', encoding='utf-8') as chapter_file:
                    json.dump([conversation], chapter_file, indent=2)

                # Convert JSON to HTML
                html_output_file = os.path.join(directory2, f"{title_with_underscores}.html")
                convert_to_html(chapter_filepath, html_output_file)

                # Convert JSON to TXT
                txt_output_file = os.path.join(directory3, f"{title_with_underscores}.txt")
                convert_to_txt(chapter_filepath, txt_output_file)

    except FileNotFoundError:
        logging.error(f"File not found: {conversations_file}")
    except json.JSONDecodeError:
        logging.error(f"Error decoding JSON in file: {conversations_file}")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")

def convert_to_html(json_file, html_output_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    result_str = get_conversation_result(json_data)

    with open(html_output_file, "w", encoding='utf-8') as html_output:
        result_html = result_str.replace("/n", "XXXXXXX\n")
        result_html = result_html.replace("<", "&lt;")
        result_html = result_html.replace(">", "&gt;")
        for line in result_html.split("XXXXXXX"):
            line = line.replace("\n", "<br />\n")
            html_output.write(line)

def convert_to_txt(json_file, txt_output_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    result_str = get_conversation_result(json_data)

    with open(txt_output_file, "w", encoding='utf-8') as txt_output:
        result_txt = result_str.replace("/n", "XXXXXXX\n")
        for line in result_txt.split("XXXXXXX"):
            txt_output.write(line)

def get_conversation_result(json_data):
    result_str = ""
    for conversation in json_data:
        title = conversation.get('title', '')
        messages = get_conversation_messages(conversation)

        result_str += title + '\n'
        for message in messages:
            result_str += message['author'] + '\n' + message['text'] + '\n'
        result_str += '\n'

    return result_str

def get_conversation_messages(conversation):
    messages = []
    current_node = conversation.get('current_node')
    while current_node:
        node = conversation['mapping'][current_node]
        message = node.get('message')
        if (message and message.get('content') and message['content'].get('content_type') == 'text' and
                len(message['content'].get('parts', [])) > 0 and len(message['content']['parts'][0]) > 0 and
                (message['author']['role'] != 'system' or message.get('metadata', {}).get('is_user_system_message'))):
            author = message['author']['role']
            if author == 'assistant':
                author = 'ChatGPT'
            elif author == 'system' and message['metadata'].get('is_user_system_message'):
                author = 'Custom user info'
            messages.append({'author': author, 'text': message['content']['parts'][0]})
        current_node = node.get('parent')
    return messages[::-1]

# Example usage
conversations_file_path = 'CHATGPT/conversations.json'
#output_folder = 'CHATDPT/output_txt_html_json'

# Ensure the output folder exists
#os.makedirs(output_folder, exist_ok=True)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Call the split, save, and convert function
split_and_save_and_convert(conversations_file_path)
