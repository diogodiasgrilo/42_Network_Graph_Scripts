# Import the necessary libraries and modules
import os
import json
from datetime import datetime, timedelta
from ptapi42.api42 import Api42

# Initialize the API connection
api: Api42 = Api42(requests_per_second=8, raises=True, log_lvl="WARNING")

# Function to fetch the user's corrected teams
def get_corrected_teams(user_id):
    # JSON file path for the user's corrected teams
    data_filepath = f"data/corrected_teams/{user_id}.json"
    
    # Check if the JSON file exists
    if os.path.exists(data_filepath):
        # Read the data from the existing JSON file
        with open(data_filepath, mode="r") as jsonfile:
            data = json.load(jsonfile)
        return data
    else:
        # Fetch data from the API
        endpoint = f"users/{user_id}/scale_teams/as_corrector"
        data = api.get(endpoint)
        
        # Save fetched data to a new JSON file
        with open(data_filepath, mode="w") as jsonfile:
            json.dump(data, jsonfile, indent=2)
        
        return data

# Function to generate the project URL based on project name and user ID
def generate_project_url(project_name, project_user_id):
    # List of excluded project names to append 42cursus- prefix
    dont_append = ["cpp", "born2beroot", "pipex", "cub3d", "netpractice", "ft_transcendence"
                    "so_long", "minitalk", "inception", "minirt", "ft_irc", "webserv", "libasm"]
    
    # Modify the project name based on the conditions
    if not any(x in project_name for x in dont_append):
        project_name = "42cursus-" + project_name
    elif "cpp" in project_name:
        project_name = "cpp-module-" + project_name.split("-")[-1]
    
    # Construct and return the project URL
    return f"https://projects.intra.42.fr/projects/{project_name}/projects_users/{project_user_id}"

# Function to check if a project name meets specific criteria
def check_project_name(project_name):
    return "c-" in project_name or ("shell-" in project_name and "minishell" not in project_name)

def checker_for_campus(evaluatee_login, evaluator_login, black_list, white_list):
    if evaluatee_login in black_list or evaluatee_login not in white_list:
        return False
    if evaluator_login in black_list or evaluator_login not in white_list:
        return False
    return True

def total_time_calc(begin_at, end_at):
    if begin_at is None or end_at is None:
        return None

    # Convert timestamps to datetime objects
    begin_time = datetime.strptime(begin_at, "%H:%M:%S")
    end_time = datetime.strptime(end_at, "%H:%M:%S")

    # Calculate the time difference
    time_diff = end_time - begin_time

    # Ensure the result is a positive time duration
    if time_diff.total_seconds() < 0:
        time_diff += timedelta(hours=24)

    # Format the result as HH:MM:SS
    # pad with 0 if needed
    if len(str(time_diff).split(":")[0]) == 1:
        return "0" + str(time_diff)
    else:
        return str(time_diff)

def create_files():
    if not os.path.exists("student_evaluations"):
        os.makedirs("student_evaluations")
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists("data/corrected_teams"):
        os.makedirs("data/corrected_teams")
    if not os.path.exists("student_evaluations/nodes"):
        os.makedirs("student_evaluations/nodes")
    if not os.path.exists("student_evaluations/links"):
        os.makedirs("student_evaluations/links")
    if not os.path.exists("student_evaluations/project_links"):
        os.makedirs("student_evaluations/project_links")
