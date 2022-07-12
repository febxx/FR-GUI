import sqlite3 as sq


def check_func(func):
    def wrapper_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (sq.OperationalError, sq.IntegrityError):
            print(f"{func.__name__} returns an error, please try again with another id or value.")
            return None
    return wrapper_func

class DataBase():
    def __init__(self):
        self.conn = sq.connect("my_database.db")
        self.curs = self.conn.cursor()

        self.curs.execute("""CREATE TABLE IF NOT EXISTS main_table (id TEXT PRIMARY KEY, password TEXT)""")

    @check_func
    def create_secondary(self, login):
        self.curs.execute(f"""CREATE TABLE {login}(application TEXT PRIMARY KEY, login TEXT,  password TEXT)""")


    @check_func
    def add_account(self, log, pword):
        """ Add a value to the main table and
        """
        #Placeholder : insert variables in sqlite3
        self.curs.execute(f"""INSERT INTO main_table VALUES (?, ?)""", (log, pword))
        self.conn.commit()

    @check_func
    def add_in_secondary(self, login, app, id, lock):
        """Add data to user's table
        """
        self.curs.execute(f"""INSERT INTO  {login} VALUES (?, ?, ?)""", ( app,  id, lock))
        self.conn.commit()


    @check_func
    def check_pass(self, user, app):
        """
        Get a password from the database and return it as  string
        """
        infos = self.curs.execute(f"SELECT login, password FROM {user} WHERE application = '{app}'")
        return list(infos)[0]

    @check_func
    def delete_table(self, user):
        """
        Delete account
        """
        try:
            self.curs.execute(f"""DROP TABLE  {user}""")
        except sq.OperationalError:
            return self.err_find

    @check_func
    def delete_entry(self, user, entry):
        """
        Delete an entry from a user's data base
        """
        try:
            self.curs.execute(f"""DELETE FROM  {user} WHERE application = ? """, (entry))
        except sq.OperationalError:
            return self.err_find

    @check_func
    def update_entry(self, user, entry, change):
        """Update the entry of a user's data base
        """
        self.curs.execute(f"""UPDATE {user} SET password = ? WHERE application = ? """, (change, entry))
        self.conn.commit()


    @check_func
    def add_many(self, list_data):
        self.curs.executemany("INSERT INTO main_table VALUES (?, ?)", list_data)
        self.conn.commit()

    @check_func
    def delete_entry(self, table, id_val):
        self.curs.execute(f"""DELETE FROM {table} WHERE id = ?""", (id_val,))
        self.conn.commit()

    @check_func
    def save_query(self):
       """ save a modification after user verification
       """
       self.conn.commit()

    @check_func
    def check_table(self, table='main_table'):
        """print every row of the table
        """
        logins = {}

        for row in self.curs.execute(f"SELECT * FROM {table}"):
            logins[row[0]] = row[1]
        return logins


    @check_func
    def users_list(self):
        logins = []

        for row in self.curs.execute(f"SELECT id FROM main_table "):
            logins.append(row[0])
        return(logins)


    @check_func
    def control_center(self):
        """ For a custom query, more complex than a one liner
        """
        c_command = input("Enter your command : ")
        self.curs.executescript(c_command)
        self.conn.commit()

    @check_func
    def close_app(self):
        self.conn.close()

if __name__ =='__main__':
    r1 = [("Jack", 217),
          ("Ripley", 'USS Sulaco'),
          ("Radamanthe", 1234)
          ]
    first_test = DataBase()
    # first_test.add_many(r1)
    first_test.create_secondary("Jack")
    first_test.save_query()
    first_test.add_in_secondary("Jack", "facebook", "jack D", "123" )
    print(first_test.check_table("Jack"))
    first_test.update_entry("Jack", 'facebook', 'pass2')
    print(first_test.check_account)
    print(first_test.users_list())
    print(type(first_test.users_list()))