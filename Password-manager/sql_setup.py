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


    def create_master_password_table(self, pwd):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if self.is_master_table():
            self.insert_master_password(pwd)
        else:
            c.execute(""" CREATE TABLE master_pwd_table (master_password text) """)
        conn.commit()
        conn.close()


    def insert_master_password(self, pwd):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" INSERT INTO master_pwd_table VALUES (:password) """,
                 {'password': pwd})
        conn.commit()
        conn.close()
        # c.close()


    # def delete_master_user(self, inp_arg):
    #     conn = sqlite3.connect(self.filename)
    #     c = conn.cursor()
    #     if inp_arg is None:
    #         raise TypeError("Please provide a field to remove")
    #     else:
    #         if '.com' in inp_arg:
    #             c.execute("""DELETE FROM password_manager WHERE website=:web""",
    #                       {'web': inp_arg})  # Delete passwords for the mentioned website.
    #         else:
    #             c.execute("""DELETE FROM password_manager WHERE username=:user""",
    #                       {'user': inp_arg})  # Delete password for the given username.
    #     conn.commit()
    #     conn.close()


    def update_master_pwd(self, new_pwd):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        try:
            c.execute(""" UPDATE master_pwd_table SET master_password = :new_val) """, {'new_val': new_pwd})
            conn.commit()
            conn.close()
            return True
        except sqlite3.OperationalError:
            return False


    def is_present_pass(self):
        try:
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute(""" SELECT * FROM master_pwd_table """)
            data = c.fetchall()
            conn.commit()
            conn.close()
            if len(data) == 0:
                return False
            else:
                return True
        except sqlite3.OperationalError:
            return False


    def return_master_password(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT * FROM master_pwd_table """)
        mas_pwd = c.fetchall()
        conn.commit()
        conn.close()
        return mas_pwd[0][0]


    def create_pwd_table(self, sl_no, website, username, password):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT name FROM sqlite_master WHERE type='table' and name='password_manager' """)
        table_list = c.fetchall()
        # conn.commit()
        # conn.close()
        if len(table_list) == 1:
            self.insert_values(sl_no, website, username, password)
        else:
            c.execute(""" CREATE TABLE password_manager (sl_no INTEGER PRIMARY KEY, website TEXT, username TEXT, password TEXT) """)
            self.insert_values(sl_no, website, username, password)
        conn.commit()
        conn.close()


    def insert_values(self, sl_no, website, username, password):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" INSERT INTO password_manager VALUES (:num, :web, :user, :pass) """,
                 {'num': sl_no, 'web': website, 'user': username, 'pass': password})  # SQL statement to insert entries into a table
        conn.commit()
        conn.close()


    def return_serial_number(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT * FROM password_manager """)
        t_entries = c.fetchall()
        num = len(t_entries)
        conn.commit()
        conn.close()
        return num+1


    def update_username(self, inp_arg):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" UPDATE password_manager SET :column = REPLACE(username, :old_user, :new_user ) """, {'old_user': old_user, 'new_user': inp_arg})
        conn.commit()
        conn.close()
        return True


    def update_password(self, inp_args, new_args):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()

        for i_arg, n_arg in zip(inp_args, new_args):
            c.execute(""" UPDATE password_manager SET :column = REPLACE(:column, :val) """, {'column': i_arg, 'val': n_arg})
        conn.commit()
        conn.close()
        return True


    def update_website(self, inp_args, new_args):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()

        for i_arg, n_arg in zip(inp_args, new_args):
            c.execute(""" UPDATE password_manager SET :column = REPLACE(:column, :val) """, {'column': i_arg, 'val': n_arg})
        conn.commit()
        conn.close()
        return True


    def update_credentials(self, inp_args, new_args):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()

        # for i_arg, n_arg in zip(inp_args, new_args):
        #     c.execute(""" UPDATE password_manager SET :column = REPLACE(:column, :val) """, {'column': i_arg, 'val': n_arg})
        # conn.commit()
        # conn.close()
        return True


    def print_value(self, inp_arg):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if inp_arg is None:
            raise TypeError("Please provide a field to remove")
        else:
            if '.com' in inp_arg:
                c.execute(""" SELECT * FROM password_manager WHERE website=:web """, {'web': inp_arg})
            else:
                c.execute(""" SELECT * FROM password_manager WHERE username=:user """, {'user': inp_arg})
            values = c.fetchall()
            conn.commit()
            conn.close()

            return values


    def print_all_values(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT * FROM password_manager """)  # SQL command to select all entries in a table
        values = c.fetchall()
        conn.commit()
        conn.close()
        return values


    def remove_values(self, inp_arg):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        if inp_arg is None:
            raise TypeError(" Please provide a field to remove ")
        else:
            c.execute(""" SELECT * FROM password_manager """)

            c.execute(""" SELECT * FROM password_manager """)
            len_table = len(c.fetchall())

            c.execute(""" SELECT * FROM password_manager WHERE sl_no BETWEEN :start AND :end """,
                      {'start': inp_arg + 1, 'end': len_table})
            conn.commit()
            next_entries = c.fetchall()
            c.execute(""" DELETE FROM password_manager WHERE sl_no=:num """, {'num': inp_arg})
            conn.commit()
            for entry in next_entries:
                c.execute(""" UPDATE password_manager SET sl_no = sl_no -1 WHERE sl_no = :num """, {'num': entry[0]})
            conn.commit()
            conn.close()


    def remove_all_values(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" DELETE FROM password_manager """)  # SQL command to delete all entries from a table
        conn.commit()
        conn.close()
        # c.close()


    # CHECK FUNCTIONS
    def is_table_present(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        try:
            c.execute(""" SELECT name FROM sqlite_master WHERE type='table' and name='password_manager' """)
            pwd_table_name = c.fetchall()
            conn.commit()
            conn.close()
            if len(pwd_table_name) != 0:
                return True
            else:
                return False
        except sqlite3.OperationalError:
            return False


    def is_master_table(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        try:
            c.execute(""" SELECT name FROM sqlite_master WHERE type='table' and name='master_pwd_table' """)
            # c.execute(""" SELECT * FROM master_pwd_table """)
            table_name = c.fetchall()
            print(table_name)
            conn.commit()
            conn.close()
            if len(table_name) != 0:
                return True
            else:
                return False
        except sqlite3.OperationalError:
            return False


    def is_master_data(self):
        if self.is_master_table():
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute(""" SELECT * FROM master_pwd_table """)
            table_data = c.fetchall()
            print(table_data)
            conn.commit()
            conn.close()
            if len(table_data) != 0:
                return True
            else:
                return False
        else:
            return False




# if __name__ == '__main__':
    # connect_database()
