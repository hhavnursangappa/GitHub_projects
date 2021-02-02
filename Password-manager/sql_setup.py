import sqlite3
import os


class Database:
    def __init__(self):
        self.filename = None

        # Check the existing path for '.db' file. Connect to it if it exists else create a new one
        for f_name in os.listdir('.'):
            if f_name.endswith('.db'):
                self.filename = f_name
                break
            else:
                self.filename = 'password.db'

        # conn.close()
        # self.c = self.conn.cursor()


    def create_master_password_table(self, user, pwd):
        # try:
        #     self.c.execute("""CREATE TABLE master_pwd_table (master_user text, master_password text)""")  # SQL statement to create a Table in the database
        # #     self.c.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='master_pwd'""")  # SQL statement to create a Table in the database
        # except sqlite3.OperationalError:
        #     self.update_master_password_table(user, pwd)
        # self.conn.commit()
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT name FROM sqlite_master WHERE type='table' and name='master_pwd_table'""")
        table_list = c.fetchone()
        if len(table_list) == 1:
            self.update_master_password_table(user, pwd)
        else:
            c.execute("""CREATE TABLE master_pwd_table (master_user text, master_password text)""")
        conn.commit()
        conn.close()
        # c.close()

        # WITH self.c
        # self.c.execute("""SELECT name FROM sqlite_master WHERE type='table' and name='master_pwd_table'""")
        # table_list = self.c.fetchone()
        # if len(table_list) == 1:
        #     self.update_master_password_table(user, pwd)
        # else:
        #     self.c.execute("""CREATE TABLE master_pwd_table (master_user text, master_password text)""")
        # self.conn.commit()


        # self.c.execute("""CREATE TABLE master_pwd_table (master_user text, master_password text)""")


    def update_master_password_table(self, user, pwd):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""INSERT INTO master_pwd_table VALUES (:user, :password)""",
                       {'user': user, 'password': pwd})
        # conn.commit()
        # conn.close()
        # c.close()

        # WITH self.c
        # self.c.execute("""INSERT INTO master_pwd_table VALUES (:user, :password)""",
        #                {'user': user, 'password': pwd})
        # self.conn.commit()
        # self.conn.close()


    def is_present_user(self, user):
        try:
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute("""SELECT * FROM master_pwd_table WHERE master_user=:user """, {'user': user})
            # print(c.fetchall())
            data = c.fetchall()
            conn.commit()  # readlines method
            conn.close()
            # c.close()
            if len(data) == 0:
                return False
            elif user in data[0][0]:
                return True
        except sqlite3.OperationalError:
            return False

        #  WITH self
        # try:
        #     self.conn = sqlite3.connect('password.db')
        #     self.c.execute("""SELECT * FROM master_pwd_table WHERE master_user=:user""", {'user': user})
        #     # self.c.execute("""SELECT * FROM master_pwd_table""")
        #     data = self.c.fetchall() # readlines method
        #     self.conn.commit()
        #     if len(data) == 0:
        #         return False
        #     elif user in data[0][0]:
        #         return True
        # except sqlite3.OperationalError:
        #     return False


    def return_master_password(self, user):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT * FROM master_pwd_table WHERE master_user=:user""", {'user': user})
        mas_pwd = c.fetchall()
        conn.commit()
        conn.close()
        return mas_pwd[0][1]

        # With self
        # password_present = False
        # self.c.execute("""SELECT * FROM master_pwd_table WHERE master_user=:user""", {'user': user})
        # return self.c.fetchall()


    def create_table(self, website, username, password):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT name FROM sqlite_master WHERE type='table' and name='password_manager'""")
        table_list = c.fetchall()
        if len(table_list) == 1:
            self.insert_values(website, username, password)
        else:
            c.execute("""CREATE TABLE password_manager (website text, username text, password text)""")
        conn.commit()
        conn.close()
        # c.close()

        # With self
        # try:
        #     self.c.execute("""CREATE TABLE pwd_manager (website text, username text, password text)""")  # SQL statement to create a Table in the database
        # except sqlite3.OperationalError:
        #     pass
        #
        # self.conn.commit()


    def insert_values(self, website, username, password):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""INSERT INTO password_manager VALUES (:website, :username, :password)""",
                 {'website': website, 'username': username, 'password': password})  # SQL statement to insert entries into a table
        # conn.commit()
        # conn.close()
        # c.close()

        # With self
        # self.c.execute("""INSERT INTO pwd_manager VALUES (:website, :username, :password)""", {'website': website, 'username':username, 'password': password})  # SQL statement to insert entries into a table
        # self.conn.commit()


    def print_value(self, inp_arg):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if inp_arg is None:
            raise TypeError("Please provide a field to remove")
        else:
            if '.com' in inp_arg:
                c.execute("""SELECT * FROM password_manager WHERE website=:web)""", {'web': inp_arg})
            else:
                c.execute("""SELECT * FROM password_manager WHERE username=:user""", {'user': inp_arg})
                conn.commit()
                conn.close()
            return c.fetchall()


        # With self
        # if inp_arg is None:
        #     raise TypeError("Please provide a field to remove")
        # else:
        #     if '.com' in inp_arg:
        #         self.c.execute("""SELECT * FROM pwd_manager WHERE website=:web)""", {'web': inp_arg})
        #     else:
        #         self.c.execute("""SELECT * FROM pwd_manager WHERE username=:user""", {'user': inp_arg})
        #     return self.c.fetchall()


    def print_all_values(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""SELECT * FROM password_manager""")  # SQL command to select all entries in a table
        values = c.fetchall()
        conn.commit()
        conn.close()
        return values

        # With self
        # self.c.execute("""SELECT * FROM pwd_manager""")  # SQL command to select all entries in a table
        # return self.c.fetchall()


    def remove_values(self, inp_arg):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if inp_arg is None:
            raise TypeError("Please provide a field to remove")
        else:
            if '.com' in inp_arg:
                c.execute("""DELETE FROM password_manager WHERE website=:web""", {'web': inp_arg})  # Delete passwords for the mentioned website.
            else:
                c.execute("""DELETE FROM password_manager WHERE username=:user""", {'user': inp_arg})  # Delete password for the given username.
        conn.commit()
        conn.close()
        # c.close()


        # With self
        # if inp_arg is None:
        #     raise TypeError("Please provide a field to remove")
        # else:
        #     if '.com' in inp_arg:
        #         self.c.execute("""DELETE FROM pwd_manager WHERE website=:web""", {'web': inp_arg})  # Delete passwords for the mentioned website.
        #     else:
        #         self.c.execute("""DELETE FROM pwd_manager WHERE website=:user""", {'user': inp_arg})  # Delete password for the given username.
        # self.conn.commit()
        # self.conn.close()


    def remove_all_values(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute("""DELETE FROM password_manager""")  # SQL command to delete all entries from a table
        conn.commit()
        conn.close()
        # c.close()

        # self.c.execute("""DELETE FROM pwd_manager""")  # SQL command to delete all entries from a table
        # self.conn.commit()
        # self.conn.close()


# if __name__ == '__main__':
    # connect_database()
