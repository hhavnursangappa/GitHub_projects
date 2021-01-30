import sqlite3
import os


class Database:
    def __init__(self):
        self.conn = None

        # Check the existing path for '.db' file. Connect to it if it exists else create a new one
        for f_name in os.listdir('.'):
            if f_name.endswith('.db'):
                self.conn = sqlite3.connect(f_name)
                break
            else:
                self.conn = sqlite3.connect('passsword.db')

        self.c = self.conn.cursor()


    def create_master_password_table(self, user, pwd):
        # try:
        #     # self.c.execute("""CREATE TABLE master_pwd_table (master_user text, master_password text)""")  # SQL statement to create a Table in the database
        #     self.c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='master_pwd'""")  # SQL statement to create a Table in the database
        #     self.conn.commit()
        # except sqlite3.OperationalError:
        #     self.update_master_password_table(user, pwd)
        self.c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='master_pwd'""")
        if len(self.c.fetchone()[0]) == 1:
            self.update_master_password_table(user, pwd)
        else:
            self.c.execute("""CREATE TABLE master_pwd_table (master_user text, master_password text)""")
        self.conn.commit()


        # self.c.execute("""CREATE TABLE master_pwd_table (master_user text, master_password text)""")


    def update_master_password_table(self, user, pwd):
        self.c.execute("""INSERT INTO master_pwd_table VALUES (:user, :password)""",
                       {'user': user, 'password': pwd})
        self.conn.commit()
        # self.conn.close()


    def is_present_user(self, user):
        try:
            # self.c.execute("""SELECT * FROM master_pwd_table WHERE master_user=:user""", {'user': user})
            self.c.execute("""SELECT * FROM master_pwd_table""")
            self.c.fetchall() # readlines method
            self.conn.commit()
            if len(self.c.fetchall()) == 0:
                return False
            elif user in self.c.fetchall()[0]:
                return True
        except sqlite3.OperationalError:
            return False


    def return_master_password(self, user):
        # password_present = False
        self.c.execute("""SELECT * FROM master_pwd_table WHERE master_user=:user""", {'user': user})
        return self.c.fetchall()


    def create_table(self):
        try:
            self.c.execute("""CREATE TABLE pwd_manager (website text, username text, password text)""")  # SQL statement to create a Table in the database
        except sqlite3.OperationalError:
            pass

        self.conn.commit()


    def insert_values(self, website, username, password):
        self.c.execute("""INSERT INTO pwd_manager VALUES (:website, :username, :password)""", {'website': website, 'username':username, 'password': password})  # SQL statement to insert entries into a table
        self.conn.commit()


    def print_value(self, inp_arg):
        if inp_arg is None:
            raise TypeError("Please provide a field to remove")
        else:
            if '.com' in inp_arg:
                self.c.execute("""SELECT * FROM pwd_manager WHERE website=:web)""", {'web': inp_arg})
            else:
                self.c.execute("""SELECT * FROM pwd_manager WHERE username=:user""", {'user': inp_arg})
            return self.c.fetchall()


    def print_all_values(self):
        self.c.execute("""SELECT * FROM pwd_manager""")  # SQL command to select all entries in a table
        return self.c.fetchall()


    def remove_values(self, inp_arg):
        if inp_arg is None:
            raise TypeError("Please provide a field to remove")
        else:
            if '.com' in inp_arg:
                self.c.execute("""DELETE FROM pwd_manager WHERE website=:web""", {'web': inp_arg})  # Delete passwords for the mentioned website.
            else:
                self.c.execute("""DELETE FROM pwd_manager WHERE website=:user""", {'user': inp_arg})  # Delete password for the given username.
        self.conn.commit()
        self.conn.close()


    def remove_all_values(self):
        self.c.execute("""DELETE FROM pwd_manager""")  # SQL command to delete all entries from a table
        self.conn.commit()
        self.conn.close()


# if __name__ == '__main__':
    # connect_database()
