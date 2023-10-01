# Use the official MariaDB image as the base image
FROM mariadb

# Install the MySQL client
RUN apt-get update && apt-get install -y mysql-client

# Clean up apt cache
RUN apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /mariadb.d

# Copy your SQL script into the container (assuming it's in the same directory as Dockerfile)
COPY nodes.sql /mariadb.d/
COPY links.sql /mariadb.d/
COPY project_links.sql_project_0.sql /mariadb.d/

# Expose the MySQL default port
EXPOSE 3306
