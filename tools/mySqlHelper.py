from mysql.connector import connect, Error

class MySqlHelper:
    """Class for saving data to a MySQL database."""

    def __init__(self, db_config):
        self.db_config = db_config

    def save_data(self, data_list, table):
        """
        Save data to the specified table in the MySQL database.
        :param data_list: List of data to be saved (list of tuples)
        :param table: The table name in the database where data should be stored
        """
        try:
            connection = connect(**self.db_config)
            if connection.is_connected():
                print("Connected to database")

            insert_query = f"INSERT INTO {table} (title, content) VALUES (%s, %s)"
            with connection.cursor() as cursor:
                cursor.executemany(insert_query, data_list)
                connection.commit()
                print("Data inserted successfully")
        except Error as e:
            print(f"Database operation failed: {e}")
        finally:
            if connection and connection.is_connected():
                connection.close()
                print("Database connection closed")
