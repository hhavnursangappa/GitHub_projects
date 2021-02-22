# Import necessary modules
import sys
import pyperclip
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from sql_setup import Database

db = Database()  # Instantiate the database object

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hello User")
        self.root.protocol("WM_DELETE_WINDOW", self.close_all_windows)
        # self.update_or_delete = None
        self.all_entries = []
        self.checkbox_list = []
        self.var_list = []

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

        self.center_position_window(self.root)
        # windowWidth = self.root.winfo_reqwidth()
        # windowHeight = self.root.winfo_reqheight()
        #
        # positionRight = int(self.root.winfo_screenwidth() / 2 - windowWidth / 2)
        # positionDown = int(self.root.winfo_screenheight() / 2 - windowHeight / 2)
        #
        # self.root.geometry("+{}+{}".format(positionRight, positionDown))
        # self.root.resizable(False, False)

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
        self.login_win.bind('<Return>', self.login_btn_command)  # TODO: Bind the return event to all respective button function calls

        self.center_position_window(self.login_win)
        # windowWidth = self.login_win.winfo_reqwidth()
        # windowHeight = self.login_win.winfo_reqheight()
        #
        # positionX = int((self.login_win.winfo_screenwidth() / 2) - (windowWidth / 2))
        # positionY = int((self.login_win.winfo_screenheight() / 2) - (windowHeight / 2))
        #
        # self.login_win.geometry("+{}+{}".format(positionX, positionY))
        # self.login_win.resizable(False, False)


    def login_password_vault(self):
        m_data = db.is_master_data()
        if m_data:
            m_pwd = db.return_master_password()
            pass_key = str(self.pass_field.get())
            attempt = 0
            while pass_key != m_pwd:
                if attempt < 3:
                    pass_key = simpledialog.askstring(title="Login Failed", prompt=f"Wrong password. You have {3 - attempt} attempts left. \nPlease try again: ", show='*')
                    attempt += 1
                else:
                    messagebox.showinfo("Login Failed", "You have exhausted your attempts. \nThe application is going to terminate now.")
                    self.close_all_windows()

            self.login_win.withdraw()
            self.root.withdraw()
            messagebox.showinfo("Login Successfull", "You have successfully logged in")
            self.show_password_table()

        else:
            messagebox.showwarning("Login Failed", "You have not yet created a vault. Create one by entering the master password")
            self.login_win.destroy()
            self.create_password_window()


    def create_password_window(self):
        self.pass_win = tk.Toplevel()
        self.pass_win.title("Create Vault")
        self.pass_win.grab_set()
        self.pass_win.protocol("WM_DELETE_WINDOW", self.close_all_windows)
        self.pass_win.bind('<Return>', self.create_btn_command)

        frame = tk.Frame(self.pass_win)
        frame.pack(side='top')

        prompt_label = tk.Label(frame, text="Enter master password")
        prompt_label.pack(side='top', padx=5, pady=5)

        self.pass_field = tk.Entry(frame, show='*', width=15)
        self.pass_field.pack(side='top', padx=5, pady=5)

        create_btn = tk.Button(frame, text="Create", width=10, command=self.create_password_vault)
        create_btn.pack(side='top', padx=5, pady=5)

        self.pass_win.update()
        windowWidth = self.root.winfo_reqwidth()
        windowHeight = self.pass_win.winfo_reqheight()

        self.pass_win.geometry("{}x{}".format(windowWidth, windowHeight))

        positionX = int((self.root.winfo_screenwidth() / 2) - (windowWidth / 2))
        positionY = int((self.root.winfo_screenheight() / 2) - (windowHeight / 2))

        self.pass_win.geometry("+{}+{}".format(positionX, positionY))
        self.pass_win.resizable(False, False)


    def create_password_vault(self):
        db.remove_all_values()
        db.create_master_password_table(self.pass_field.get())
        messagebox.showinfo("Vault creation successfull", "A Vault has been successfully created for you")
        self.pass_win.destroy()
        self.show_password_table()


    def show_password_table(self):
        self.root.withdraw()
        try:
            self.login_win.destroy()
        except AttributeError:
            self.pass_win.destroy()

        self.pass_table_win = tk.Toplevel()
        self.pass_table_win.title("Password Manager")
        self.pass_table_win.protocol("WM_DELETE_WINDOW", self.close_all_windows)

        top_frame = tk.Frame(self.pass_table_win)
        top_frame.pack(side='top', fill='both')

        top_left_frame = tk.Frame(master=top_frame)
        top_left_frame.pack(side='left')

        self.top_right_frame = tk.Frame(master=top_frame)
        self.top_right_frame.pack(side='left')

        bottom_frame = tk.Frame(self.pass_table_win)
        bottom_frame.pack(side='top')

        # Create scrollbar
        pass_table_scroll = tk.Scrollbar(master=top_frame)
        pass_table_scroll.pack(side='right', fill='y')

        # Create tree view
        cols = ('SL.NO.', 'WEBSITE', 'USERNAME', 'PASSWORD')
        self.password_table = ttk.Treeview(master=top_left_frame, columns=cols, padding=8, show='headings', selectmode='browse',
                                           yscrollcommand=pass_table_scroll.set, height=5)
        self.password_table.pack()
        self.password_table.column("SL.NO.", width=45, anchor='center')
        self.password_table.column("WEBSITE", anchor='center')
        self.password_table.column("USERNAME", anchor='center')
        self.password_table.column("PASSWORD", anchor='center')

        l1 = tk.Label(master=self.top_right_frame, text='Show Passwords')
        l1.pack(side='top', pady=0)

        # Bind the left and right click actions to functions
        self.password_table.bind('<ButtonRelease-1>', self.return_entry_id)
        self.password_table.bind('<Button-3>', self.create_right_click_menu)

        # Insert values in to the tree view
        for col in cols:
            self.password_table.heading(col, text=col)

        self.update_password_table()

        # Assign alternating colors to rows of the table
        self.password_table.tag_configure('odd_row', background='#cfd1d4')
        self.password_table.tag_configure('even_row', background='white')

        # Configure the scroll bar
        pass_table_scroll.configure(command=self.password_table.yview)
        self.pass_table_win.grid()

        # Add the buttons
        add_entry_btn = tk.Button(bottom_frame, text="Add credentials", width=15, command=self.add_credentials_window)
        add_entry_btn.grid(row=0, column=0, padx=5, pady=5)

        change_mas_pwd_btn = tk.Button(bottom_frame, text="Change master key", command=self.change_master_password_window)
        change_mas_pwd_btn.grid(row=0, column=1, padx=5, pady=5)

        delete_all_btn = tk.Button(bottom_frame, text="Delete all credentials", width=15, command=self.delete_all_credentials)
        delete_all_btn.grid(row=1, column=0, padx=5, pady=5)

        logout_btn = tk.Button(bottom_frame, text="Logout", width=15, command=self.logout)
        logout_btn.grid(row=1, column=1, padx=5, pady=5)

        self.pass_table_win.update()
        self.center_position_window(self.pass_table_win)


    def update_password_table(self):
        values_to_insert = db.return_all_values()
        self.all_entries = values_to_insert
        tags = 'odd_row'
        for val in values_to_insert:
            self.password_table.insert("", "end", values=(val[0], val[1], val[2], '*' * len(val[3])), tags=(tags, ))
            tags = 'even_row' if tags == 'odd_row' else 'odd_row'

            # Insert checkboxes
            var = tk.IntVar()
            ch_box = tk.Checkbutton(master=self.top_right_frame, text="", variable=var)
            ch_box.pack(side='top')
            self.checkbox_list.append(ch_box)
            self.var_list.append(var)


    def create_right_click_menu(self, event):
        row = self.password_table.identify_row(event.y)
        self.password_table.selection_set(row)
        column = self.password_table.identify_column(event.x)
        # self.update_or_delete = self.password_table.item(row)['values']
        menu = tk.Menu(self.pass_table_win, tearoff=0)
        menu.add_command(label='Update', command=lambda: self.update_credentials_window(row))
        menu.add_command(label='Delete', command=lambda: self.delete_credentials(row))
        menu.add_command(label='Copy', command=lambda: self.copy_data(row, column))
        menu.tk_popup(event.x_root, event.y_root)


    def copy_data(self, row, column):
        column = int(column[-1]) - 1
        row = int(row[-1]) - 1
        text_to_copy = self.all_entries[int(row)][column]
        pyperclip.copy(str(text_to_copy))


    def return_entry_id(self, event):
        self.password_table.focus()
        # focus = self.password_table.focus()
        # self.update_or_delete = self.password_table.item(focus)['values']


    def update_credentials_window(self, row):
        idx = int(row[-1]) - 1
        entry = self.all_entries[idx]

        self.update_cred_win = tk.Toplevel()
        self.update_cred_win.bind('<Return>', self.update_btn_command)

        update_web_label = tk.Label(self.update_cred_win, text="Updated website")
        update_web_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.update_web_field = tk.Entry(self.update_cred_win)
        self.update_web_field.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        self.update_web_field.insert(0, entry[1])

        update_user_label = tk.Label(self.update_cred_win, text="Updated username")
        update_user_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.update_user_field = tk.Entry(self.update_cred_win)
        self.update_user_field.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        self.update_user_field.insert(0, entry[2])

        update_pass_label = tk.Label(self.update_cred_win, text="Updated password")
        update_pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.update_pass_field = tk.Entry(self.update_cred_win)
        self.update_pass_field.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        self.update_pass_field.insert(0, entry[3])

        update_btn = tk.Button(self.update_cred_win, text='Update', command=lambda: self.update_credentials(idx))
        update_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        cancel_btn = tk.Button(self.update_cred_win, text='Cancel', command=lambda: self.update_cred_win.destroy())
        cancel_btn.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        self.center_position_window(self.update_cred_win)


    def update_credentials(self, idx):
        entry_to_update = self.all_entries[idx]
        res = db.update_credentials(entry_to_update[0], entry_to_update.get(),
                                    entry_to_update.get(), entry_to_update.get())
        if res:
            messagebox.showinfo("Credentials updated", "Your credentials have been updated")
            self.update_cred_win.destroy()
            self.password_table.delete(*self.password_table.get_children())
            self.update_password_table()
        else:
            messagebox.showwarning("Credentials update failed", "Your credentials couldn't be updated")
        self.pass_table_win.wait_window()


    def delete_credentials(self, row):
        idx = int(row[-1]) - 1
        entry_to_delete = self.all_entries[idx]
        ans = messagebox.askyesnocancel("Delete Entry", "Are you sure you want to delete the entry:\n" + ', '.join(entry_to_delete[1:]) + "?")
        if ans:
            sl_no_to_remove = entry_to_delete[0]
            res = db.remove_values(sl_no_to_remove)
            if res:
                messagebox.showinfo("Credential Deleted", "The entry " + ', '.join(entry_to_delete[1:]) + " has been successfully deleted.")
                self.password_table.delete(*self.password_table.get_children())
                self.update_password_table()
                self.pass_table_win.wait_window()
            else:
                messagebox.showwarning("Credential Delete Failed", "The entry " + ', '.join(entry_to_delete[1:]) + " couldn't be deleted.")
                self.pass_table_win.wait_window()
        else:
            self.pass_table_win.wait_window()


    def add_credentials_window(self):
        self.cred_win = tk.Toplevel()
        self.cred_win.title = 'Add a new entry'
        self.cred_win.bind('<Return>', self.add_btn_command)

        web_label = tk.Label(self.cred_win, text="Enter the website")
        web_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.web_field = tk.Entry(self.cred_win)
        self.web_field.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        user_label = tk.Label(self.cred_win, text="Enter the username")
        user_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.user_field = tk.Entry(self.cred_win)
        self.user_field.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        pass_label = tk.Label(self.cred_win, text="Enter the passsword")  # TODO: Insert the parameter show='*'
        pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.pass_field = tk.Entry(self.cred_win)
        self.pass_field.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        add_btn = tk.Button(self.cred_win, text='Add', command=self.add_credentials)
        add_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        cancel_btn = tk.Button(self.cred_win, text='Cancel', command=lambda: self.cred_win.destroy())
        cancel_btn.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        self.center_position_window(self.cred_win)


    def add_credentials(self):
        self.cred_win.withdraw()

        web = str(self.web_field.get())
        username = str(self.user_field.get())
        password = str(self.pass_field.get())

        table_exists = db.is_password_table()
        if table_exists:
            sl_no = db.return_serial_number()
        else:
            sl_no = 1

        db.create_pwd_table(sl_no, web, username, password)
        values = db.return_all_values()
        val_to_add = values[-1]
        self.password_table.insert("", "end", values=(val_to_add[0], val_to_add[1], val_to_add[2], val_to_add[3]))
        messagebox.showinfo("Added Credentials", "The password has been successfully added to the vault")
        self.pass_table_win.wait_window()


    def delete_all_credentials(self):
        ans = messagebox.askyesnocancel("Delete all credentials", "Are you sure you want to delete all credentials and clear the vault?")
        if ans:
            db.remove_all_values()
            self.password_table.delete(*self.password_table.get_children())
            self.update_password_table()
        else:
            self.pass_table_win.wait_window()


    def change_master_password_window(self):
        self.chng_master_pwd_win = tk.Toplevel()
        self.chng_master_pwd_win.title = "Change the master password"
        self.chng_master_pwd_win.bind('<Return>', self.change_pass_btn_command)

        curr_pass_label = tk.Label(master=self.chng_master_pwd_win, text="Enter the current master password")
        curr_pass_label.grid(row=0, column=0, padx=5, pady=5, sticky='e')

        self.curr_pass_field = tk.Entry(self.chng_master_pwd_win)  # TODO: Pass the parameter show='*'
        self.curr_pass_field.grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        new_pass_label = tk.Label(master=self.chng_master_pwd_win, text="Enter the new master password")
        new_pass_label.grid(row=1, column=0, padx=5, pady=5, sticky='e')

        self.new_pass_field = tk.Entry(self.chng_master_pwd_win)  # TODO: Pass the parameter show='*'
        self.new_pass_field.grid(row=1, column=1, padx=5, pady=5, sticky='ew')

        conf_pass_label = tk.Label(master=self.chng_master_pwd_win, text="Confirm the new master password")
        conf_pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='e')

        self.conf_pass_field = tk.Entry(self.chng_master_pwd_win)  # TODO: Pass the parameter show='*'
        self.conf_pass_field.grid(row=2, column=1, padx=5, pady=5, sticky='ew')

        change_pass_btn = tk.Button(self.chng_master_pwd_win, text='Change Master Password', command=self.change_master_password)
        change_pass_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        cancel_btn = tk.Button(self.chng_master_pwd_win, text='Cancel', command=lambda: self.chng_master_pwd_win.destroy())
        cancel_btn.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        self.center_position_window(self.chng_master_pwd_win)
        # windowWidth = self.chng_master_pwd_win.winfo_reqwidth()
        # windowHeight = self.chng_master_pwd_win.winfo_reqheight()
        #
        # positionX = int((self.chng_master_pwd_win.winfo_screenwidth() / 2) - windowWidth / 2)
        # positionY = int((self.chng_master_pwd_win.winfo_screenheight() / 2) - windowHeight / 2)
        #
        # self.chng_master_pwd_win.geometry("+{}+{}".format(positionX, positionY))
        # self.chng_master_pwd_win.resizable(False, False)


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
                    messagebox.showwarning("Change master password", "The old and the new password cannot be same. \nPlease enter a unique password")
                    self.chng_master_pwd_win.wait_window()
            else:
                messagebox.showwarning("Change master password", "The confirmed password doesnt match the new password. Please check")
                self.chng_master_pwd_win.wait_window()
        else:
            messagebox.showwarning("Change master password", "Please enter the current master password correctly\n")
            self.chng_master_pwd_win.wait_window()


    def logout(self):
        ans = messagebox.askyesnocancel('Logout', 'Are you sure you want to log out of the vault')
        if ans:
            # self.pass_table_win.destroy()
            self.close_all_windows()
            messagebox.showinfo('Logout', 'Goodbye! Have a nice day ahead')
        else:
            self.pass_table_win.wait_window()


    def center_position_window(self, window):
        windowWidth = window.winfo_reqwidth()
        windowHeight = window.winfo_reqheight()

        positionX = int((window.winfo_screenwidth() / 2) - (windowWidth / 2))
        positionY = int((window.winfo_screenheight() / 2) - (windowHeight / 2))

        window.geometry("+{}+{}".format(positionX, positionY))
        window.resizable(False, False)


    def close_all_windows(self):
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()
        messagebox.showinfo('Exit', 'Goodbye! Have a nice day ahead')
        self.root.destroy()
        sys.exit()


    # Functions bound to the '<Return>' event
    def login_btn_command(self, event):
        self.login_password_vault()


    def create_btn_command(self, event):
        self.create_password_vault()


    def update_btn_command(self, event):
        self.update_credentials()


    def add_btn_command(self, event):
        self.add_credentials()


    def change_pass_btn_command(self, event):
        self.change_master_password()













# COMMAND LINE VERSION OF THE PASSWORD MANAGER
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