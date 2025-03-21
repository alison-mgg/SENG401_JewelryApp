#Connect python to mySQL, to import in controller files
import mysql.connector
from flask import g
import os

def get_database():
    """Get a MySQL database connection using mysql.connector."""
    if 'database' not in g:
        # Initialize the connection if it's not already set
        g.database = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST"),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB")
        )
    return g.database
