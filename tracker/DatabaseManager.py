import sqlite3
from contextlib import closing


##
# In charge of creating and loading the database for the tracker server
#
# @author Paul Rachwalski
# @date Mar 24, 2015
##
class DatabaseManager:

    ##
    # Constructor that initializes DB and connection
    #
    # @param flask_app The flask application object to refer to
    # @param schema_path The file path to the schema file for the SQLite database
    ##
    def __init__(self, schema_path, db_path):
        self.schema = schema_path
        self.db_path = db_path
        return

    ##
    # Connects to the database
    #
    # @return The sqlite3 database connection if available, otherwise None
    ##
    def connect_db(self):
        if self.db_path is not None:
            return sqlite3.connect(self.db_path)
        else:
            return None


    ##
    # Initializes the tables based on the schema file
    ##
    def init_db(self):
        with closing(self.connect_db()) as db:
            with open(self.schema, "r") as schema:
                schema_str = schema.read().replace('\n', '')
                db.cursor().executescript(schema_str)
            db.commit()
        return


    ##
    # Adds an IP to a file_id
    #
    # @param db_path The path to the database to read from
    # @param file_id The ID of the file in the table
    # @param ip The IP address of the client
    ##
    def add(self, file_id, ip):
        with closing(self.connect_db()) as db_conn:
            # Prevents SQL injection via prepared statement
            db_conn.cursor().execute('INSERT INTO tracker (File, IP) VALUES (?, ?)',
                                [file_id, ip])
            db_conn.commit()
        return

    ##
    # Removes an associated file with an IP address
    #
    # @param db_path The path to the database to read from
    # @param file_id The ID of the file in the table (if file_id is *, delete all files associated with ip)
    # @param ip The IP address of the client
    ##
    def remove(self, file_id, ip):
        with closing(self.connect_db()) as db_conn:
            # Prevents SQL injection via prepared statement
            if file_id is not "*":
                db_conn.cursor().execute('DELETE FROM tracker WHERE File = ? AND IP = ?',
                                         [file_id, ip])
            else:
                db_conn.cursor().execute('DELETE FROM tracker WHERE IP = ?',
                                         [ip])
            db_conn.commit()
        return

    ##
    # Gets a list of IPs associated with a file
    #
    # @param db_path The path to the database to read from
    # @param file_id The ID of the file in the table
    ##
    def get(self, file_id):
        ips = []

        with closing(self.connect_db()) as db_conn:
            # Prevents SQL injection via prepared statement
            db_cursor = db_conn.cursor()
            db_cursor.execute('SELECT IP FROM tracker WHERE File = ?',
                                [file_id])

            rows = db_cursor.fetchall()
            for row in rows:
                ips.append(row[0])

        return ips
