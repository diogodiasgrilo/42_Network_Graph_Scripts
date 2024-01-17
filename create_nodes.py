import os
import json
import csv
from tqdm import tqdm
from ptapi42.api42 import Api42

api: Api42 = Api42(requests_per_second=8, raises=True, log_lvl="WARNING")

def get_user_image(user_id):
    endpoint = f"users/{user_id}"
    data = api.get(endpoint)
    image_link = data.get("image", {}).get("versions", {}).get("small", "")
    return image_link

def make_nodes(campus_id, student_count):
    nodes_file_path = "student_evaluations/nodes/nodes.js"
    
    #Check if nodes.js file already exists
    if os.path.exists(nodes_file_path):
        overwrite = input("File 'nodes.js' already exists. Do you want to overwrite it? (y/n): ")
        if overwrite.lower() == 'n':
            print("Using existing file.")
            return
    
    users = []
    with open("data/users.csv", mode="r") as users_file:
        users_reader = csv.DictReader(users_file)
        for row in users_reader:
            users.append(row)

    black_list = []
    with open("data/black_list.csv", mode="r") as black_list_file:
        black_list_reader = csv.reader(black_list_file)
        for row in black_list_reader:
            black_list.append(row[0])

    user_images = []  # List to store user images

    if student_count == -1:
        student_count = len(users)

    with tqdm(total=student_count, desc="Creating student nodes", unit="student") as pbar:
        for idx, user in enumerate(users):
            if pbar.n == student_count:
                break

            user_id = user["id"]
            s1 = user["image"]
            s2 = "'small'"
            s3 = "micro"

            start = s1.find(s2) + 10
            end = s1.find(s3) - 4
            image_link = s1[start:end]
            
            if image_link == "on":
                image_link = None

            if image_link:
                user_image = {"id": idx, "login": user["login"], "picture": image_link}
                user_images.append(user_image)
                pbar.update(1)

    json_string = json.dumps(user_images, indent=4)

    csv_folder = "student_evaluations/nodes"
    os.makedirs(csv_folder, exist_ok=True)

    js_filename = f"{csv_folder}/nodes.js"

    with open(js_filename, mode="w", newline="") as jsfile:
        jsfile.write(f'var nodes = {json_string};')

    print(f"Student nodes saved to {js_filename}")
