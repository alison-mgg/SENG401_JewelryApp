#Connect python to mySQL, to import in controller files
import mysql.connector
from flask import current_app

def get_database():
    """Get a MySQL database connection using mysql.connector."""
    if not hasattr(current_app, 'database'):
        # Initialize the connection if it's not already set
        current_app.database = mysql.connector.connect(
            host=current_app.config['MYSQL_HOST'],
            user=current_app.config['MYSQL_USER'],
            password=current_app.config['MYSQL_PASSWORD'],
            database=current_app.config['MYSQL_DB']
        )
    return current_app.database
