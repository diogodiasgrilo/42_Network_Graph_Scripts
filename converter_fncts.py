import re
import json
from to_sql import *

def convert_all():
    json_nodes_converter()
    json_to_sql_nodes("./student_evaluations/nodes/nodes.json", "./student_evaluations/nodes/nodes.sql", "Users")
    json_links_converter()
    json_to_sql_links("./student_evaluations/links/links.json", "./student_evaluations/links/links.sql", "Links")
    json_project_links_converter()
    json_to_sql_project_links("./student_evaluations/project_links/project_links.json", "./student_evaluations/project_links/project_links.sql")

def json_nodes_converter():
    #Read the JavaScript file(nodes.js)
    with open("./student_evaluations/nodes/nodes.js", "r") as js_file:
        js_code = js_file.read()

    # Use a regular expression to extract the 'nodes' variable
    match = re.search(r"var nodes = (\[.*?\]);", js_code, re.DOTALL)

    if match:
        nodes_json_str = match.group(1)
        # Parse the extracted JSON data
        nodes = json.loads(nodes_json_str)
        # Serialize the Python data to JSON
        json_data = json.dumps(nodes, indent=4)  # You can use 'indent' to format the JSON nicely

        # Write the JSON data to a file (e.g., nodes.json)
        with open('./student_evaluations/nodes/nodes.json', 'w') as json_file:
            json_file.write(json_data)
    else:
        print("Could not find 'nodes' variable in the JavaScript file.")

def json_links_converter():
    # Read the JavaScript file (links.js)
    with open("./student_evaluations/links/links.js", "r") as js_file:
        js_code = js_file.read()

    # Use regular expression to extract the 'links' variable
    match = re.search(r"var links = (\[.*?\]);", js_code, re.DOTALL)

    if match:
        links_json_str = match.group(1)
        # Parse the extracted JSON data
        links = json.loads(links_json_str)
        # Serialize the Python data to JSON
        json_data = json.dumps(links, indent=4)  # You can use 'indent' to format the JSON nicely

        # Write the JSON data to a file (e.g., links.json)
        with open('./student_evaluations/links/links.json', 'w') as json_file:
            json_file.write(json_data)
    else:
        print("Could not find 'links' variable in the JavaScript file.")

def json_project_links_converter():
    # Read the JavaScript file (project_links.js)
    with open("./student_evaluations/project_links/project_links.js", "r") as js_file:
        js_code = js_file.read()

    # Use regular expression to extract the 'project_links' variable
    match = re.search(r"var project_links = (\[.*?\]);", js_code, re.DOTALL)

    if match:
        project_links_json_str = match.group(1)
        # Parse the extracted JSON data
        project_links = json.loads(project_links_json_str)
        # Serialize Python data to JSON
        json_data = json.dumps(project_links, indent=4)  # You can use 'indent' to format the JSON nicely

        # Write the JSON data to a file (e.g.,project_links.json)
        with open('./student_evaluations/project_links/project_links.json', 'w') as json_file:
            json_file.write(json_data)
    else:
        print("Could not find 'project_links' variable in the JavaScript file.")
