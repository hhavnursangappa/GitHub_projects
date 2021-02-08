import tkinter as tk
from tkinter import ttk
import sys
import Pmw
from tkinter import simpledialog
from tkinter import messagebox
from sql_setup import Database

db = Database()  # Instantiate the database object

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hello User")

        top_frame = tk.Frame(self.root)
        top_frame.pack(side='top')

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side='top')

        welcome_label = tk.Label(top_frame, text="Welcome to your Password manager")
        welcome_label.pack(side='top', padx=5, pady=5)

        login_btn = tk.Button(bottom_frame, text="Login", width=10, command=self.login_window)
        login_btn.pack(side='left', padx=5, pady=5)

        create_btn = tk.Button(bottom_frame, text="Create Vault", width=10, command=self.create_password_window)
        create_btn.pack(side='left', padx=5, pady=5)

        self.root.mainloop()


    def login_window(self):
        self.login_win = tk.Toplevel()
        self.login_win.title("Vault Login")
        self.login_win.grab_set()


        frame = tk.Frame(self.login_win)
        frame.pack(side='top')

        prompt_label = tk.Label(frame, text="Enter master password to login")
        prompt_label.pack(side='top', padx=5, pady=5)

        self.pass_field = tk.Entry(frame, show='*', width=15)
        self.pass_field.pack(side='top', padx=5, pady=5)

        login_btn = tk.Button(frame, text="Login", width=10, command=self.login_password_vault)
        login_btn.pack(side='top', padx=5, pady=5)

        self.login_win.bind('<Return>', self.login_password_vault)


    # def hit_enter_to_login(self, event):
    #     self.login_password_vault()


    def login_password_vault(self, event):
        m_data = db.is_master_data()
        if m_data:
            m_pwd = db.return_master_password()
            pass_key = str(self.pass_field.get())
            attempt = 0
            while pass_key != m_pwd:
                if attempt <= 3:
                    pass_key = simpledialog.askstring(title="Login Failed", prompt=f"Wrong password. You have {3 - attempt} attempts left. Please try again: ")
                    attempt += 1
                    self.login_win.wait_window()
                else:
                    print("You have exhausted your attempts. Try again after 24 hrs")
                    sys.exit()

            messagebox.showinfo("Login Successfull", "You have successfully logged in")
            self.root.withdraw()
            self.password_table()

        else:
            messagebox.showwarning("Login Failed", "You have not yet created a vault. Create one by entering the master password")
            self.login_win.destroy()


    def create_password_window(self):
        self.pass_win = tk.Toplevel()
        self.pass_win.title("Create Vault")
        self.pass_win.grab_set()

        frame = tk.Frame(self.pass_win)
        frame.pack(side='top')

        prompt_label = tk.Label(frame, text="Enter master password")
        prompt_label.pack(side='top', padx=5, pady=5)

        self.pass_field = tk.Entry(frame, show='*', width=15)
        self.pass_field.pack(side='top', padx=5, pady=5)

        create_btn = tk.Button(frame, text="Create", width=10, command=self.create_password_vault)
        create_btn.pack(side='top', padx=5, pady=5)


    def create_password_vault(self):
        db.remove_all_values()
        db.create_master_password_table(self.pass_field.get())
        messagebox.showinfo("Vault creation successfull", "A Vault has been successfully created for you. Now you can do the following: ")
        self.pass_win.destroy()
        self.password_table()


    def password_table(self):
        self.root.withdraw()
        self.login_win.destroy()

        self.pass_table = tk.Toplevel()
        self.pass_table.title("Password Manager")

        top_frame = tk.Frame(self.pass_table)
        top_frame.pack(side='top', fill='both')

        bottom_frame = tk.Frame(self.pass_table)
        bottom_frame.pack(side='top')

        bottom_left_frame = tk.Frame(self.pass_table)
        bottom_left_frame.pack(side='left')

        bottom_right_frame = tk.Frame(self.pass_table)
        bottom_right_frame.pack(side='left')

        # Create the table here
        Pmw.initialise(self.root)

        self.sf = Pmw.ScrolledFrame(top_frame, labelpos='n', label_text='Scrolled Frame', usehullsize=1, hull_width=400, hull_height=220,)
        self.sf.pack(side='top', fill='both')

        cols = ('Sl.No.', 'Website', 'Username', 'Password')
        password_table = ttk.Treeview(master=self.sf.interior(), columns=cols, show='headings')  # Use ScrolledWindow.interior() as the master for any children widgets
        password_table.column("Sl.No.", width=10)
        # tree.column("2", width=50)
        # tree.column("3", width=50)
        # w = self.sf.frame.winfo_width()

        for col in cols:
            password_table.heading(col, text=col)

        values = db.print_all_values()
        for val in values:
            password_table.insert("", "end", values=(val[0], val[1], val[2], val[3]))

        password_table.grid(row=0, column=0, sticky='news')

        w1 = password_table.winfo_width()
        # self.sf.clipper.configure(width=w1)
        # self.sf.xview('moveto', 1)

        add_entry_btn = tk.Button(bottom_left_frame, text="Add credentials", width=15, command=self.add_credentials_window)
        add_entry_btn.pack(side='top', padx=5, pady=5)

        delete_entry_btn = tk.Button(bottom_left_frame, text="Delete a credential", width=15, command=self.delete_credentials_window)
        delete_entry_btn.pack(side='top', padx=5, pady=5)

        delete_all_btn = tk.Button(bottom_left_frame, text="Delete all credentials", width=15, command=self.delete_all_credentials)
        delete_all_btn.pack(side='top', padx=5, pady=5)

        change_mas_pwd_btn = tk.Button(bottom_right_frame, text="Change master password", width=15, command=self.change_master_password_window)
        change_mas_pwd_btn.pack(side='top', padx=5, pady=5)

        logout_btn = tk.Button(bottom_right_frame, text="Logout", width=15, command=self.logout)
        logout_btn.pack(side='top', padx=5, pady=5)


    def add_credentials_window(self):
        cred_win = tk.Toplevel()
        cred_win.title = 'Add a new entry'

        web_label = tk.Label(cred_win, text="Enter the website")
        web_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.web_field = tk.Entry(cred_win)
        self.web_field.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        user_label = tk.Label(cred_win, text="Enter the username")
        user_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.user_field = tk.Entry(cred_win)
        self.user_field.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        pass_label = tk.Label(cred_win, text="Enter the passsword")
        pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.pass_field = tk.Entry(cred_win)
        self.pass_field.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        add_btn = tk.Button(cred_win, text='Add', command=self.add_credentials)
        add_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')


    def add_credentials(self):
        web = str(self.web_field.get())
        username = str(self.user_field.get())
        password = str(self.pass_field.get())

        table_exists = db.is_password_table()
        if table_exists:
            sl_no = db.return_serial_number()
        else:
            sl_no = 1
        db.create_pwd_table(sl_no, web, username, password)
        messagebox.showinfo("The password has been successfully added to the vault")
        self.pass_table.wait_window()


    def delete_credentials_window(self):
        # delete_cred_win = tk.Toplevel()
        # delete_cred_win.title = "Delete existing credential"
        ans = messagebox.askyesnocancel("Delete existing credential", "Are you sure you want to delete these credentials from the vault?")
        if ans == 'yes':
            db.remove_values()
        else:
            self.pass_table.wait_window()


    def delete_all_credentials(self):
        ans = messagebox.askyesnocancel("Delete all credentials", "Are you sure you want to delete all credentials and clear the vault?")
        if ans == 'yes':
            db.remove_all_values()
        else:
            self.pass_table.wait_window()


    def change_master_password_window(self):
        self.chng_master_pwd_win = tk.Toplevel()
        self.chng_master_pwd_win.title = "Change the master password"

        curr_pass_label = tk.Label("Enter the current master password")
        curr_pass_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.curr_pass_field = tk.Entry(self.chng_master_pwd_win)
        self.curr_pass_field.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        new_pass_label = tk.Label("Enter the new master password")
        new_pass_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.new_pass_field = tk.Entry(self.chng_master_pwd_win)
        self.new_pass_field.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        conf_pass_label = tk.Label("Confirm the new master password")
        conf_pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.conf_pass_field = tk.Entry(self.chng_master_pwd_win)
        self.conf_pass_field.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        change_pass_btn = tk.Button(self.chng_master_pwd_win, text='Change Master Password', command=self.change_master_password)
        change_pass_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')


    def change_master_password(self):
        curr_m_pwd = str(self.curr_pass_field.get())
        new_m_pwd = str(self.new_pass_field.get())
        conf_m_pwd = str(self.conf_pass_field.get())
        m_pwd = db.return_master_password()
        if curr_m_pwd == m_pwd:
            if conf_m_pwd == new_m_pwd:
                if new_m_pwd != curr_m_pwd:
                    res = db.update_master_pwd(new_m_pwd)
                    if res:
                        messagebox.showinfo("Change master password", "Master password changed successfully !")
                        self.chng_master_pwd_win.destroy()
                    else:
                        messagebox.showwarning("Change master password", "There was a problem changing the password.")
                        self.chng_master_pwd_win.wait_window()
                else:
                    messagebox.showwarning("Change master password", "The old and the new password cannot be same. Please enter a unique password")
                    self.chng_master_pwd_win.wait_window()
            else:
                messagebox.showwarning("Change master password", "The confirmed password doesnt match the new password. Please check")
                self.chng_master_pwd_win.wait_window()
        else:
            messagebox.showwarning("Change master password", "Please enter the current master password correctly\n")
            self.chng_master_pwd_win.wait_window()


    def logout(self):
        ans = messagebox.askyesnocancel('Logout', 'Are you sure you want to log out of the vault')
        if ans == 'yes':
            # Insert WM_PROTOCOL to destroy all windows
            self.pass_table.destroy()
            messagebox.showinfo('Logout', 'Goodbye! Have a nice day ahead')
        else:
            self.pass_table.wait_window()











# BARE BONES IMPLEMENATION OF THE PASSWORD MANAGER USER INTERFACE
close = False

def manager():
    global close
    while not close:
        print("\n%%%%%%%%%%%%%%%%%%%%%%%%% ---- MAIN MENU ---- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("Welcome to your password manager.")
        print("1. Login to your password vault\n"
              "2. Create a password vault")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        try:
            choice = int(input("Enter what you wish to do (1 or 2): "))
        except ValueError:
            print("Invalid Choice! Please enter 1 or 2\n")
            continue

        if choice == 1:
            m_data = db.is_master_data()
            if m_data:
                login_password_vault()
            else:
                print("You have not yet created a vault. Create one by entering the master password")
                create_password_vault()

        elif choice == 2:
            create_password_vault()

        elif close:
            break

        else:
            print("Invalid choice. Please enter 1 or 2")

    print("Goodbye! Have a nice day ahead !")
    sys.exit()


def create_password_vault():
    db.remove_all_values()
    # master_user = str(input("Master Username: "))
    master_pass = str(input("Enter a Master Password for your vault: "))
    db.create_master_password_table(master_pass)
    print("\nA Vault has been successfully created for you. Now you can do the following: ")
    menu()


def login_password_vault():
    m_pwd = db.return_master_password()
    pass_key = str(input("Enter the master passkey: "))
    attempt = 0
    while pass_key != m_pwd:
        if attempt <= 3:
            pass_key = str(input(f"Wrong password. You have {3 - attempt} attempts left. Please try again: "))
            attempt += 1
        else:
            print("You have exhausted your attempts. Try again after 24 hrs")
            sys.exit()

    print("You have successfully logged in")
    print('\n')
    menu()


def print_entries(entries):
    print("*************************************************************************************")
    print("|\tSL.NO\t|\tWEBSITE\t|\tUSERNAME\t|\tPASSWORD\t|")
    print("-------------------------------------------------------------------------------------")
    for entry in entries:
        row = []
        row.append(str(entry[0]))
        row.append(entry[1])
        row.append(entry[2])
        row.append(entry[3])

        print('|\t' + '\t|\t'.join(row) + '\t|')
    print("*************************************************************************************")


def menu():
    global close
    sel = None
    while sel != 8:
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%% ---- SUB MENU ---- %%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("1. Create a new entry\n"
              "2. View all credentials\n"
              "3. Filter entry\n"
              "4. Delete an existing credential\n"
              "5. Delete all credentials\n"
              "6. Update existing credentials\n"
              "7. Change Master Password\n"
              "8. Logout")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        try:
            sel = int(input("Enter your selection (1-8): "))
        except ValueError:
            print("Invalid Choice!. Please enter a number in the range (1-7)")
            continue

        if sel == 1:
            web = str(input("Enter the website: "))
            username = str(input("Enter the username. Use '_' instead of whitespace: "))
            password = str(input("Enter the password: "))
            table_exists = db.is_password_table()
            if table_exists:
                sl_no = db.return_serial_number()
            else:
                sl_no = 1
            db.create_pwd_table(sl_no, web, username, password)
            print(f"The password has been successfully added to the vault")
            print('\n')

        elif sel == 2:
            values = db.print_all_values()
            if len(values) == 0:
                print("The vault is empty. Start adding some passwords")
            else:
                print("\nThe entries in the database are as follows: ")
                print_entries(values)
            print('\n')

        elif sel == 3:
            inp_arg = str(input("Enter the username or the website for which you would like to view the password for: "))
            print(f"The password for {inp_arg} are as follows:")
            values = db.print_value(inp_arg)
            if len(values) == 0:
                print("The vault is empty. Start adding some passwords\n")
            else:
                print_entries(values)
            print('\n')

        elif sel == 4:
            # inp_arg = str(input("Enter the username or the website for which you would like to delete the password for: "))
            inp_arg = int(input("Enter the Sl. No of the entry, which you would like to delete: "))
            conf = str(input(f"Are you sure you want to delete the password for {inp_arg}? [y/n]: "))
            if conf == 'y' or conf == 'Y':
                db.remove_values(inp_arg)
                print(f"The password for {inp_arg} has been successfully removed from the vault")
                print('\n')

        elif sel == 5:
            conf = str(input(f"Are you sure you want to delete all passwords and clear the vault? [y/n]: "))
            if conf == 'y' or conf == 'Y':
                db.remove_all_values()
            print("All passwords from the vault have been successfully deleted")
            print('\n')

        elif sel == 6:
            num = str(input("Enter the sl_no of the entry you wish to update: "))
            col = str(input("Enter the name of the column you wish to update: "))
            val = str(input("Enter the new credentials for the above mentioned column: "))
            res = db.update_credentials(num, col, val)
            if res:
                print("The credentials have been successfully updated")
            else:
                print("There was an error in updating the credentials!")

        elif sel == 7:
            while True:
                curr_m_pwd = str(input("Enter the current master password: "))
                new_m_pwd = str(input("Enter the new master password: "))
                conf_m_pwd = str(input("Confirm the new master password: "))
                m_pwd = db.return_master_password()
                if curr_m_pwd == m_pwd:
                    if conf_m_pwd == new_m_pwd:
                        if new_m_pwd != curr_m_pwd:
                            res = db.update_master_pwd(new_m_pwd)
                            if res:
                                print("Master password changed successfully !\n")
                                break
                            else:
                                print("There was a problem changing the password.\n")
                        else:
                            print("The old and the new password cannot be same. Please enter a unique password\n")
                    else:
                        print("The confirmed password doesnt match the new password. Please check\n")
                else:
                    print("Please enter the current master password correctly\n")

    print("You have successfully logged out of the vault.")
    close = True


if __name__ == '__main__':
    ui = UserInterface()
