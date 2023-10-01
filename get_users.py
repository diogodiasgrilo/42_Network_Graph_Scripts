import csv
import os
from datetime import datetime
from ptapi42.api42 import Api42

# have all the months in a list
months = ["january", "february", "march", "april", "may", "june", "july", "august",
          "september", "october", "november", "december"]

api: Api42 = Api42(requests_per_second=8, raises=True, log_lvl="WARNING")

def get_users_data(campus_id):
    #find the current month
    current_month = months[datetime.now().month - 1]
    print("Is there a piscine ongoing? (y/n)")
    ongoing_piscine = input()
    if ongoing_piscine == "y":
        print("On what month does the piscine end?")
        piscine_month = input()
        print("What is the year of the piscine?")
        piscine_year = input()
    if not (os.path.exists("data/black_list.csv") or os.path.exists("data/users.csv") or os.path.exists(f"data/white_list_{current_month}.csv")):
        print("Fetching users data from API...")
        endpoint = f"/campus/{campus_id}/users"
        data = api.get(endpoint)
        filtered_users = filter_active_students(data)
        filtered_users = filter_42lisboa_email(filtered_users)
        filtered_users = filter_staff_and_alumni(filtered_users)
        if ongoing_piscine == "y":
            filtered_users = filter_pisciners_year_and_month(filtered_users, piscine_month, piscine_year)

        all_users = {user["id"]: user["login"] for user in data}
        main_group_users = {user["id"] for user in filtered_users}

        black_list_ids = all_users.keys() - main_group_users
        white_list_ids = main_group_users - black_list_ids
        black_list = [all_users[user_id] for user_id in black_list_ids]
        white_list = [all_users[user_id] for user_id in white_list_ids]

        csv_folder = "data"
        os.makedirs(csv_folder, exist_ok=True)

        black_list_filename = f"{csv_folder}/black_list.csv"
        white_list_filename = f"{csv_folder}/white_list_{current_month}.csv"
        users_filename = f"{csv_folder}/users.csv"
        
        # Save to CSV files
        with open(black_list_filename, "w", newline="") as f_black:
            writer = csv.writer(f_black)
            writer.writerow(["login"])
            writer.writerows([[user] for user in black_list])
            
        with open(white_list_filename, "w", newline="") as f_white:
            writer = csv.writer(f_white)
            writer.writerow(["login"])
            writer.writerows([[user] for user in white_list])

        with open(users_filename, "w", newline="") as f_users:
            writer = csv.DictWriter(f_users, fieldnames=filtered_users[0].keys())
            writer.writeheader()
            writer.writerows(filtered_users)
    else:
        print("Student data already fetched from API. Using cached data.")
    return current_month

def filter_active_students(users_data):
    return [user for user in users_data if user.get("active?")]

def filter_pisciners_year_and_month(users_data, piscine_month, piscine_year):
    users = []
    for user in users_data:
        if not (user.get("pool_month") == piscine_month and user.get("pool_year") == piscine_year):
            users.append(user)
    return users

def filter_42lisboa_email(users_data):
    return [user for user in users_data if "42lisboa" in user.get("email", "")]

def filter_staff_and_alumni(users_data):
    return [user for user in users_data if not (user.get("staff?") or user.get("alumni?"))]
