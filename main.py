import os
import json

from difflib import SequenceMatcher
from bin.common.learn_response import learn_chat, read_cortex
from bin.common.configuration_controller import config_controller

script_dir = os.path.dirname(os.path.abspath(__file__))
prefix_dir = os.path.abspath(os.path.join(script_dir))
config_settings = config_controller(script_dir, "var/conf/default.conf", "var/conf/local.conf")
app_name = config_settings.get('general', 'app_name')
version = config_settings.get('general', 'version')
description = config_settings.get('general', 'description')
ai_memory = config_settings.get('database', 'ai_memory')


def learn_new_things(memory, keyword, response):
    memory = os.path.abspath(os.path.join(prefix_dir, memory))
    print(memory)
    temp_memory = {}
    temp_memory["keyword"] = keyword
    temp_memory["response"] = response
    chat_list = []
    chat_list = read_cortex(memory)
    chat_list = json.loads(chat_list)
    chat_list.append(temp_memory)
    chat_list = json.dumps(chat_list, indent=2)
    learn_chat(memory, chat_list)


def ai_brain(memory):
    memory = os.path.abspath(os.path.join(prefix_dir, memory))
    print(memory)
    chat_list = []
    chat_list = read_cortex(memory)
    chat_list = json.loads(chat_list)
    return chat_list


def chat_analyzer(user_txt, system_txt):
    ratio = SequenceMatcher(None, user_txt, system_txt).ratio()
    return ratio


def compare_database(user_txt, chat_list):

    response = "Sorry I'm still learning!"
    past_ratio = 0

    for item in chat_list:
        ratio = chat_analyzer(item['keyword'], user_txt.lower())
        percentage = "{:.0%}".format(float(ratio))
        print("Item compared: {} | Percentage: {}".format(item, percentage))
        if ratio > past_ratio:
            past_ratio = ratio
            response = item['response']

    return response


chat_list = ai_brain(ai_memory)
#learn_new_things(ai_memory, 'testing', 'What are we testing for?')
print(chat_list)
while True:
 user_text = input("Chat:")
 response = compare_database(user_text, chat_list)
 print(response)