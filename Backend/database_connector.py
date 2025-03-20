#Connect python to mySQL, to import in controller files
import mysql.connector
from flask import current_app
import os

def get_database():
    """Get a MySQL database connection using mysql.connector."""
    if not hasattr(current_app, 'database'):
        # Initialize the connection if it's not already set
        current_app.database = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
    return current_app.database

# Moved out from Backend/app.py
# MySQL Database configuration using environment variables
# app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
# app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
# app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
# app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

# # Function to get database connection
# def get_db_connection():
#     connection = mysql.connector.connect(
#         host=app.config['MYSQL_HOST'],
#         user=app.config['MYSQL_USER'],
#         password=app.config['MYSQL_PASSWORD'],
#         database=app.config['MYSQL_DB']
#     )
#     return connection
