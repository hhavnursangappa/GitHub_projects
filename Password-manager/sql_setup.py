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


    def create_master_password_table(self, user, pwd):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT name FROM sqlite_master WHERE type='table' and name='master_pwd_table' """)
        table_list = c.fetchone()
        if len(table_list) == 1:
            self.insert_master_credentials(user, pwd)
        else:
            c.execute(""" CREATE TABLE master_pwd_table (master_user text, master_password text) """)
        conn.commit()
        conn.close()


    def insert_master_credentials(self, user, pwd):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" INSERT INTO master_pwd_table VALUES (:user, :password) """,
                       {'user': user, 'password': pwd})
        # conn.commit()
        # conn.close()
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
            c.execute(""" UPDATE master_pwd_table SET master_password = REPLACE(master_password, :new_val) """, {'new_val': new_pwd})
            conn.commit()
            conn.close()
            return True
        except sqlite3.OperationalError:
            return False


    def is_present_user(self, user):
        try:
            conn = sqlite3.connect(self.filename)
            c = conn.cursor()
            c.execute(""" SELECT * FROM master_pwd_table WHERE master_user=:user """, {'user': user})
            data = c.fetchall()
            conn.commit()
            conn.close()
            if len(data) == 0:
                return False
            elif user in data[0][0]:
                return True
        except sqlite3.OperationalError:
            return False


    def return_master_password(self, user):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT * FROM master_pwd_table WHERE master_user=:user """, {'user': user})
        mas_pwd = c.fetchall()
        conn.commit()
        conn.close()
        return mas_pwd[0][1]


    def create_pwd_table(self, sl_no, website, username, password):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT name FROM sqlite_master WHERE type='table' and name='password_manager' """)
        table_list = c.fetchall()
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


    def return_serial_number(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" SELECT * FROM password_manager """)
        num = len(c.fetchall())
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
                conn.commit()
                conn.close()
            values = c.fetchall()

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
        c.execute(""" SELECT * FROM password_manager """)
        len_table = len(c.fetchall())
        if inp_arg is None:
            raise TypeError(" Please provide a field to remove ")
        else:
            if '.com' in inp_arg:
                c.execute(""" SELECT * FROM password_manager WHERE website=:web """, {'web': inp_arg})
                start = c.fetchall()[0][0]
                end = len_table
                c.execute(""" SELECT * FROM password_manager WHERE sl_no BETWEEN :start AND :end """, {'start': start+1, 'end': end})
                next_entries = c.fetchall()
                # c.execute(""" DELETE FROM password_manager WHERE website=:web """, {'web': inp_arg})
                # conn.commit()
                for entry in next_entries:
                    c.execute(""" REPLACE INTO password_manager (sl_no, website, username, password) VALUES (:sl_no, :new_website, :new_username, :new_password) """,
                              {'sl_no': entry[0] - 1, 'new_website': entry[1], 'new_username': entry[2], 'new_password': entry[3]})

                # for ii in range(int(sl_no)+1, len_table+1):
                #     c.execute(""" REPLACE INTO password_manager (sl_no, website, username, password) VALUES (:sl_no, :new_sl_no) """, {'sl_no': ii, 'new_sl_no': ii-1})

                # c.execute(""" DELETE FROM password_manager WHERE website=:web """, {'web': inp_arg})  # Delete passwords for the mentioned website.
            else:
                c.execute(""" DELETE FROM password_manager WHERE username=:user """, {'user': inp_arg})  # Delete password for the given username.
        conn.commit()
        conn.close()


    def remove_all_values(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        c.execute(""" DELETE FROM password_manager """)  # SQL command to delete all entries from a table
        conn.commit()
        conn.close()
        # c.close()


    def is_table_present(self):
        conn = sqlite3.connect(self.filename)
        c = conn.cursor()
        try:
            c.execute(""" SELECT name FROM sqlite_master WHERE type='table' and name='password_manager' """)
            if len(c.fetchall()) != 0:
                return True
            else:
                return False
        except sqlite3.OperationalError:
            return False
# if __name__ == '__main__':
    # connect_database()
