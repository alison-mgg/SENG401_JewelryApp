#Connect python to mySQL, to import in controller files
import mysql.connector
from mysql.connector import Error
from flask import current_app, g
import logging
import os

def get_database():
    """Get a MySQL database connection using mysql.connector."""
    try:
        if 'database' not in g:
            # Initialize the connection if it's not already set
            g.database = mysql.connector.connect(
                host=current_app.config['MYSQL_HOST'],
                user=current_app.config['MYSQL_USER'],
                password=current_app.config['MYSQL_PASSWORD'],
                database=current_app.config['MYSQL_DB']
            )
        return g.database
    except Error as e:
        logging.error(f"Database connection error: {e}")
        raise

def close_database(exception):
    """Close the database connection at the end of the request."""
    database = g.pop('database', None)
    if database is not None:
        database.close()

