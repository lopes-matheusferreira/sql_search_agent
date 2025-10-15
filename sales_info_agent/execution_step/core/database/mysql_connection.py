"""
MySQL database connection and query execution.
"""

import os
import mysql.connector
from mysql.connector import Error
from typing import List, Dict, Any, Optional


def get_mysql_connection():
    """
    Create and return a MySQL connection using environment variables.

    Returns:
        MySQL connection object or None if connection fails
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "127.0.0.1"),
            port=int(os.getenv("MYSQL_PORT", "3306")),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "test_base")
        )

        if connection.is_connected():
            print(f"✓ Connected to MySQL database: {connection.get_server_info()}")
            return connection

    except Error as e:
        print(f"✗ Error connecting to MySQL: {e}")
        return None


def execute_query(sql_query: str) -> tuple[Optional[List[Dict[str, Any]]], Optional[str]]:
    """
    Execute a SQL query and return results.

    Args:
        sql_query: SQL SELECT query to execute

    Returns:
        Tuple of (results, error_message)
        - results: List of dictionaries with query results, or None if error
        - error_message: Error message if query failed, or None if successful
    """
    connection = None
    cursor = None

    try:
        connection = get_mysql_connection()

        if not connection:
            return None, "Failed to connect to database"

        cursor = connection.cursor(dictionary=True)
        cursor.execute(sql_query)
        results = cursor.fetchall()

        print(f"✓ Query executed successfully: {len(results)} rows returned")
        return results, None

    except Error as e:
        error_msg = f"MySQL Error: {str(e)}"
        print(f"✗ {error_msg}")
        return None, error_msg

    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()


def test_connection() -> bool:
    """
    Test if database connection is working.

    Returns:
        True if connection successful, False otherwise
    """
    connection = get_mysql_connection()

    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            cursor.fetchone()
            cursor.close()
            connection.close()
            print("✓ Database connection test successful")
            return True
        except Error as e:
            print(f"✗ Database connection test failed: {e}")
            return False

    return False