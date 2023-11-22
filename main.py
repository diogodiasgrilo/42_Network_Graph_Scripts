# Import the necessary libraries and modules
import os
import csv
import re
import json
from tqdm import tqdm
from helper_fncts import *
from converter_fncts import *
from ptapi42.api42 import Api42
from create_nodes import make_nodes
from get_users import get_users_data
from to_sql import *

# Initialize the 42-API connection
api: Api42 = Api42(requests_per_second=8, raises=True, log_lvl="WARNING")

def go_for_it(interactions, project_links, interactions_key, project_url, begin_at_split, end_at_split, start_date):
    idx = next((i for i, (key, _) in enumerate(interactions.items()) 
                if key == interactions_key), None)
    if idx is not None:
        # make an array of the project_url, the begin_at time, the end_at time, and the (end_time - begin_time) time
        total_time = total_time_calc(begin_at_split, end_at_split)
        project_links[idx]["project_urls"].append([start_date, project_url, begin_at_split, end_at_split, total_time])
    interactions[interactions_key] += 1

# Function to process each student's data and interactions with other students
def process_students(users, black_list, white_list, student_count):
    interactions = {}
    project_links = []
    links_id = 0
    
    # Iterate through the users and their corrected teams
    with tqdm(total=student_count, desc="Processing students", unit="student") as pbar:
        for user in users:
            if pbar.n == student_count:
                break
            
            corrected_teams_data = get_corrected_teams(user["id"])

            if corrected_teams_data:
                # Process each team's data
                for team in corrected_teams_data:
                    corrector_login = team["corrector"]["login"]
                    project_user_id = team["team"]["users"][0]["projects_user_id"]
                    gitlab_path = team["team"].get("project_gitlab_path", "")
                    if gitlab_path:
                        project_name = gitlab_path.split("/")[-1]
                        if check_project_name(project_name):
                            continue
                        project_url = generate_project_url(project_name, project_user_id)
                    else:
                        continue
                    # Process interactions between correctors and evaluatees
                    evaluatee_login = team["correcteds"][0]["login"]
                    
                    if not checker_for_campus(evaluatee_login, corrector_login, black_list, white_list):
                        continue

                    # Get only the time between the T and the Z in the string example string to split: ""2022-04-11T14:00:00.000Z""
                    begin_at = team["begin_at"]
                    end_at = team["filled_at"]
                    begin_at_split = None
                    end_at_split = None
                    if begin_at != None:
                        begin_at_split = ((begin_at.split("T"))[1]).split(".")[0]
                        start_date = begin_at.split("T")[0]
                    if end_at != None:
                        end_at_split = ((end_at.split("T"))[1]).split(".")[0]
                    
                    interactions_key = tuple([corrector_login, evaluatee_login])
                    reversed_interactions_key = tuple([evaluatee_login, corrector_login])

                    if interactions_key in interactions:
                        go_for_it(interactions, project_links, interactions_key, project_url, begin_at_split, end_at_split, start_date)
                    elif reversed_interactions_key in interactions:
                        go_for_it(interactions, project_links, reversed_interactions_key, project_url, begin_at_split, end_at_split, start_date)
                    else:
                        project_links.append({"links_node_id": links_id, "project_urls": \
                            [[start_date, project_url, begin_at_split, end_at_split, total_time_calc(begin_at_split, end_at_split)]]})
                        interactions[interactions_key] = 1
                        links_id += 1
                pbar.update(1)
    
    return interactions, project_links

def startup_script():
    # File path for links.js
    links_file_path = "student_evaluations/links/links.js"
    
    # Check if the links.js file already exists
    if os.path.exists(links_file_path):
        overwrite = input("File 'links.js' already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() == 'n':
            print("Using existing file.")
            exit()
        
    # User inputs the campus ID and the student count
    campus_id = input("Enter the campus_id: ")
    student_count = int(input("How many students (input -1 for all): "))
    # Fetch basic user data from specific campus
    current_month = get_users_data(campus_id)
    # Create the nodes.js file
    make_nodes(campus_id, student_count)
    
    users = []
    with open("data/users.csv", mode="r") as users_file:
        users_reader = csv.DictReader(users_file)
        for row in users_reader:
            users.append(row)

    # Fetch the blacklisted users list
    black_list = []
    with open("data/black_list.csv", mode="r") as black_list_file:
        black_list_reader = csv.reader(black_list_file)
        for row in black_list_reader:
            black_list.append(row[0])
    
    # Fetch the whitelisted users list
    white_list = []
    with open(f"data/white_list_{current_month}.csv", mode="r") as white_list_file:
        white_list_reader = csv.reader(white_list_file)
        for row in white_list_reader:
            white_list.append(row[0])

    # Set student count if not previously specified
    if student_count == -1:
        student_count = len(users)
    
    return student_count, users, black_list, white_list

def construct_links_json(interactions, project_links):
    links = []  # List to store link objects

    # Construct link objects
    for idx, ((evaluator, evaluatee), interactions_count) in enumerate(interactions.items()):
        link = {"id": idx, "source": evaluator, "target": evaluatee, "interactions": interactions_count}
        links.append(link)

    json_string = json.dumps(links, indent=4)
    project_links_string = json.dumps(project_links, indent=4)

    # Create a folder and save data to CSV files
    csv_folder = "student_evaluations"
    os.makedirs(csv_folder, exist_ok=True)

    csv_filename = f"{csv_folder}/links/links.js"
    csv_filename1 = f"{csv_folder}/project_links/project_links.js"

    with open(csv_filename, mode="w", newline="") as csvfile:
        csvfile.write(f'var links = {json_string};')
        
    with open(csv_filename1, mode="w", newline="") as csvfile:
        csvfile.write(f'var project_links = {project_links_string};')
    print(f"Evaluations data saved to {csv_filename}")


def main():
    create_files()
    # Management for inputs and initial user data fetching
    student_count, users, black_list, white_list = startup_script()
    
    # Process interactions, project links, and also create project_links.js
    interactions, project_links = process_students(users, black_list, white_list, student_count)
    
    # Construct links.js file
    construct_links_json(interactions, project_links)
    
    # Convert JSON to SQL
    convert_all()

if __name__ == "__main__":
    main()
