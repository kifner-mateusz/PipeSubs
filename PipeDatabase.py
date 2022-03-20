import sqlite3
""""""


class PipeDatabase:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(PipeDatabase)
        return cls._instance

    def __init__(self, db_name='newpipe.db'):
        self.name = db_name
        # connect takes url, dbname, user-id, password
        self.conn = self.connect()
        self.cursor = self.conn.cursor()
        self.cache = {}

    def connect(self):
        try:
            return sqlite3.connect(self.name, check_same_thread=False)
        except sqlite3.Error as e:
            print("Connection to database failed")

    def get_data(self, table_name, clear_cache=False):
        if clear_cache:
            self.cursor.execute(f"SELECT * FROM {table_name}")
            self.cache[table_name] = self.cursor.fetchall()

        return self.cache[table_name]

    def get_columns(self, table_name):
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        return self.cursor.fetchall()

    def get_tables(self):
        sql_get_tables = """SELECT 
                        name
                    FROM 
                        sqlite_schema
                    WHERE 
                        type ='table' AND 
                        name NOT LIKE 'sqlite_%';"""
        self.cursor.execute(sql_get_tables)
        return self.cursor.fetchall()

    def add_row(self, table_name, *args, **kwargs):
        if len(args) > 0:
            print("add_row doesn't allow positional arguments after table_name")
            return

        keys = ""
        vals = ""
        for key in kwargs:
            keys += key+","
            vals += "?,"

        keys = keys[:-1]
        vals = vals[:-1]
        sql = f"INSERT INTO {table_name}({keys}) VALUES({vals})"
        values = list(kwargs.values())
        for i in range(len(values)):
            values[i] = str(values[i])
        self.cursor.execute(sql, values)
        self.conn.commit()

    def remove_row(self, table_name, uid):
        sql = f"DELETE FROM {table_name} WHERE uid=?"
        self.cursor.execute(sql, (uid,))
        self.conn.commit()

    def remove_all_with(self, table_name, *args, **kwargs):
        if len(args) > 0:
            print("remove_all_with doesn't allow positional arguments after table_name")
            return

        query = ""
        for key, value in kwargs.items():
            if key != "uid":
                val_str = str(value)
                query += f"{key} = \"{val_str}\" AND "

        query = query[:-4]
        sql = f"DELETE FROM {table_name} WHERE {query}"
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()

    def update_row(self, table_name, *args, **kwargs):
        if len(args) > 0:
            print("update_row doesn't allow positional arguments after table_name")
            return

        query = ""
        for key, value in kwargs.items():
            if key != "uid":
                val_str = str(value)
                query += f"{key} = \"{val_str}\","

        query = query[:-1]

        sql = f"UPDATE {table_name} SET {query} WHERE uid = ?"
        # print(sql)
        self.cursor.execute(sql, (str(kwargs["uid"])))
        self.conn.commit()

    def __del__(self):
        self.cursor.close()
        self.conn.close()
