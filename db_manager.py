import sqlite3
import json

from uuid import uuid4
from pydantic import BaseModel

class DBRequestPayload(BaseModel):
    """
    Represents a payload for a database request.

    Attributes:
        query (str): The query string for the database request.
    """
    query: str

class DBManager:
    """
    Class representing a database manager.

    Args:
        app: The application object.

    Attributes:
        app: The application object.
        db: The database object.

    """
    def __init__(self, app, db_path: str):
        self.app = app
        self._db = DB(db_path)
        self._current_action_id = uuid4().hex
    
    def update_action_id(self, action_uuid: str):
        self._current_action_id = action_uuid
        return True

    def db_execute(self, db_query: str, action_uuid: str):
        if self._current_action_id != action_uuid:
            raise ValueError("Action ID does not match the current action ID")
        return self._db.execute(db_query)

class DB:
    """
    A class representing a database manager.

    Attributes:
        db_path (str): The path to the database file.
        client: The SQLite database connection object.
        cursor: The cursor object for executing SQL queries.

    Methods:
        __init__: Initializes the DB object.
        __del__: Closes the database connection.
        execute: Executes a SELECT query and fetches the data.
        convert_to_json: Converts data to JSON format.
    """

    def __init__(self, db_path: str):
        """
        Initializes the DB object.

        Args:
            db_path (str, optional): The path to the database file. Defaults to '/Users/neilchou/vocabulary-backend/db/GRE_3333.db'.
        """
        self.client = sqlite3.connect(db_path, check_same_thread=False)
        self.cursor = self.client.cursor()
    
    def __del__(self):
        """
        Closes the database connection.
        """
        self.client.close()

    def execute(self, db_query: str):
        """
        Executes the given query and fetches the data from the database.

        Args:
            query (str): The SQL query to execute.

        Returns:
            list or dict: The fetched data in JSON format.
        """
        if "SELECT" in db_query:
            self.cursor.execute(db_query)
            return self.convert_to_json(self.cursor.fetchall())
        elif "PRAGMA" in db_query:
            self.cursor.execute(db_query)
            return self.convert_to_json(self.cursor.fetchall())
        else:
            raise ValueError("Only SELECT and PRAGMA queries are supported")

    def convert_to_json(self, data):
        """
        Converts the given data to JSON format.

        Args:
            data: The data to be converted.

        Returns:
            str: The JSON representation of the data.
        """
        if isinstance(data, list):
            return json.dumps([
                {self.cursor.description[i][0]: value for i, value in enumerate(row)}
                for row in data
            ], ensure_ascii=False)
        elif isinstance(data, tuple):
            return json.dumps({
                self.cursor.description[i][0]: value for i, value in enumerate(data)
            }, ensure_ascii=False)
        else:
            raise ValueError("Data must be a list or tuple")

if "__main__" == __name__:
    db = DB('')

    # query = 'PRAGMA table_info(Description)'
    query = 'SELECT * FROM Description'
    result = db.execute(query)
    print(result)
