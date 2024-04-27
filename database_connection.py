import mysql.connector

class TechnologyTransferDatabase:
    def __init__(self) -> None:
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(user='username',
                                                  password='password',
                                                  host='host',
                                                  database='your_database')

    def close_connection(self):
        self.connection.close()

    def create_cursor(self):
        if not self.cursor:
            self.cursor = self.connection.cursor()
        return self.cursor
    
    def commit_changes(self):
        if self.connection:
            self.connection.commit()
