import json
import os

# Function to convert JSON to SQL
def json_to_sql_nodes(json_file, sql_file, table_name):
    try:
        with open(json_file, 'r') as json_file:
            data = json.load(json_file)

        # Define the SQL schema
        sql_schema = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT PRIMARY KEY,
                login VARCHAR(255),
                picture VARCHAR(255)
            );
        """

        # Open the SQL file for writing (creates it if it doesn't exist)
        with open(sql_file, 'w') as sql_output:
            sql_output.write(sql_schema)

            for item in data:
                # Customize this part to match your JSON structure
                id = item['id']
                login = item['login']
                picture = item['picture']

                sql_insert = f"""
                    INSERT INTO {table_name} (id, login, picture)
                    VALUES ({id}, '{login}', '{picture}');
                """

                sql_output.write(sql_insert)

        print("Conversion complete. SQL file saved as {}".format(sql_file))
    except Exception as e:
        print("Error: {}".format(str(e)))
        
def json_to_sql_links(json_file, sql_file, table_name):
    try:
        with open(json_file, 'r') as json_file:
            data = json.load(json_file)

        # Define your SQL schema here
        sql_schema = f"""
            CREATE TABLE IF NOT EXISTS {table_name} (
                id INT PRIMARY KEY,
                source VARCHAR(255),
                target VARCHAR(255),
                interactions INT,
                child_link VARCHAR(255)
            );
        """

        # Open SQL file for writing (creates it if it doesn't exist)
        with open(sql_file, 'w') as sql_output:
            sql_output.write(sql_schema)

            for item in data:
                # Customize this part to match your JSON structure
                id = item['id']
                source = item['source']
                target = item['target']
                interactions = item['interactions']
                actual_child_link = 'localhost:8080/?server=mariadb&username=root&db=Student_Evaluations&table=project_' + str(item['id'])
                
                # Store the actual link in the database
                sql_insert = f"""
                    INSERT INTO {table_name} (id, source, target, interactions, child_link)
                    VALUES ({id}, '{source}', '{target}', {interactions}, '{actual_child_link}');
                """

                sql_output.write(sql_insert)

        print("Conversion complete. SQL file saved as {}".format(sql_file))
    except Exception as e:
        print("Error: {}".format(str(e)))

def json_to_sql_project_links(json_file, sql_file_prefix):
    try:
        with open(json_file, 'r') as json_file:
            data = json.load(json_file)

        parent_id = 0
        # Extract and create SQL tables for each project_urls block
        for item in data:
            table_name = f"project_{item['links_node_id']}"
            sql_file = f"{sql_file_prefix}_{table_name}.sql"  # Use a separate variable for the SQL file name

            # Define your SQL schema for each table
            sql_schema = f"""
                CREATE TABLE IF NOT EXISTS {table_name} (
                    id INT PRIMARY KEY,
                    project_url_date DATE,
                    project_url VARCHAR(255),
                    begin_at TIME,
                    end_at TIME,
                    total_time TIME,
                    links_parent_id INT
                );
            """

            # Open the SQL file for writing (creates it if it doesn't exist)
            with open(sql_file, 'w') as sql_output:
                sql_output.write(sql_schema)
                node_id = 0
                for url_block in item['project_urls']:
                    project_url_date, project_url, begin_at, end_at, total_time = url_block
                    sql_insert = f"""
                        INSERT INTO {table_name} (id, project_url_date, project_url, begin_at, end_at, total_time, links_parent_id)
                        VALUES ({node_id}, '{project_url_date}', '{project_url}', '{begin_at}', '{end_at}', '{total_time}', {parent_id});
                    """
                    sql_output.write(sql_insert)
                    node_id += 1
            parent_id += 1
    except Exception as e:
        print("Error: {}".format(str(e)))
    print(f"Conversion complete. SQL files saved as {sql_file_prefix}_*.sql. Total project_links SQL files created = {len(data)}")
