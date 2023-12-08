


import datetime
import json
import os
from mitosheet import __version__ as mitosheet_version
import getpass
from mitosheet.streamlit.v1 import RunnableAnalysis


def get_file_name_from_provider_name(provider_name):
    safe_provider_name = ""
    for c in provider_name:
        if c.isalpha() or c.isdigit() or c == ' ' or c == '_':
            safe_provider_name += c
        else:
            safe_provider_name += '_'
    return safe_provider_name + '.txt'

def save_analysis(
        provider_name,
        analysis,
        description,
    ):

    if not os.path.exists(os.path.join(os.getcwd(), 'automations')):
        os.mkdir(os.path.join(os.getcwd(), 'automations'))

    file_name = get_file_name_from_provider_name(provider_name)
    file_path = os.path.join(os.getcwd(), 'automations', file_name)
    if os.path.exists(file_path):
        return False, f"File {provider_name}.py already exists. Please choose a different name."

    with open(file_path, 'w') as f:
        f.write(json.dumps({
            "provider_name": provider_name,
            "analysis": analysis.to_json(),
            "mitosheet_version": mitosheet_version,
            "user": getpass.getuser(),
            "creation_time": str(datetime.datetime.now()),
            "description": description
        }))

    return True, None

def get_all_provider_names_from_automations():
    if not os.path.exists(os.path.join(os.getcwd(), 'automations')):
        return []

    file_names = os.listdir(os.path.join(os.getcwd(), 'automations'))

    # Then, go and read the contents of each file -- if it's valid JSON, then we can add it to the list
    providers = []
    for file_name in file_names:
        file_path = os.path.join(os.getcwd(), 'automations', file_name)
        with open(file_path, 'r') as f:
            try:
                json_string = f.read()
                json_object = json.loads(json_string)
                providers.append(json_object['provider_name'])
            except:
                pass

    return providers

def get_runnable_analysis_and_description_from_provider_name(provider_name):
    file_name = get_file_name_from_provider_name(provider_name)
    file_path = os.path.join(os.getcwd(), 'automations', file_name)
    with open(file_path, 'r') as f:
        json_string = f.read()


    automation_json = json.loads(json_string)
    analysis = RunnableAnalysis.from_json(automation_json['analysis'])

    # The description key was added in a later release of the app, 
    # so we first check that the description exists before trying to read it
    description =  automation_json['description'] if 'description' in automation_json else "No description provided for this automation"

    return analysis, description