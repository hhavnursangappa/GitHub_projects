# Import necessary modules
import sys
import random
import pyperclip
import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
from functools import partial
from sql_setup import Database

db = Database()  # Instantiate the database object

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Hello User")
        self.root.protocol("WM_DELETE_WINDOW", self.close_all_windows)
        self.all_entries = []
        self.checkbox_list = []
        self.chk_var_list = []

        top_frame = tk.Frame(self.root)
        top_frame.pack(side='top')

        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side='top')

        welcome_label = tk.Label(top_frame, text="Welcome to your Password manager")
        welcome_label.pack(side='top', padx=5, pady=5)

        login_btn = tk.Button(bottom_frame, text="Login", width=10, command=self.login_window)
        login_btn.pack(side='left', padx=5, pady=5)

        # create_btn = tk.Button(bottom_frame, text="Create Vault", width=10, command=self.create_password_window)
        # create_btn.pack(side='left', padx=5, pady=5)

        self.center_position_window(self.root)

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


    def login_password_vault(self):
        m_data = db.is_master_data()
        if m_data:
            m_pwd = db.return_master_password()
            pass_key = str(self.pass_field.get())
            attempt = 0
            while pass_key != m_pwd:
                if attempt < 3:
                    pass_key = simpledialog.askstring(title="Login Failed", prompt=f"Wrong password. Attempts left: {3 - attempt}. \nPlease try again: ", show='*')
                    attempt += 1
                else:
                    messagebox.showinfo("Login Failed", "You have exhausted your attempts. \nThe application is going to terminate now.")
                    self.close_all_windows()

            self.login_win.withdraw()
            self.root.withdraw()
            messagebox.showinfo("Login Successful", "You have successfully logged in")
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
        messagebox.showinfo("Vault creation successful", "A Vault has been successfully created for you")
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
        top_left_frame.pack(side='left', pady=0)

        top_right_frame = tk.Frame(master=top_frame, bg='white')
        top_right_frame.pack(side='left', anchor='n', fill='both', pady=0)

        top_right_label_frame = tk.Frame(master=top_right_frame, bg='white')
        top_right_label_frame.pack(side='top', anchor='n', fill='both', pady=0)

        top_right_canvas_frame = tk.Frame(master=top_right_frame, bg='white')
        top_right_canvas_frame.pack(side='top', anchor='n', fill='both', pady=0)

        self.canvas = tk.Canvas(master=top_right_canvas_frame, bg='white', bd=0, highlightthickness=0)  # TODO: Define canvas in top_right_canvas_frame
        self.canvas.pack(side='top', anchor='nw', fill='both', expand=True, pady=0)

        bottom_frame = tk.Frame(self.pass_table_win)
        bottom_frame.pack(side='top')

        # Create scrollbar
        pass_table_scroll = tk.Scrollbar(master=top_frame, orient=tk.VERTICAL, command=self.view_all)
        pass_table_scroll.pack(side='right', fill='y')

        # Create tree view
        cols = ('SL.NO.', 'WEBSITE', 'USERNAME', 'PASSWORD')
        self.password_table = ttk.Treeview(master=top_left_frame, columns=cols, padding=0, show='headings', selectmode='browse',
                                           yscrollcommand=pass_table_scroll.set, height=3)
        self.password_table.pack(side='top', anchor='nw')
        self.password_table.column("SL.NO.", width=45, anchor='center')
        self.password_table.column("WEBSITE", anchor='center')
        self.password_table.column("USERNAME", anchor='center')
        self.password_table.column("PASSWORD", anchor='center')
        self.password_table.update()

        # Configure the canvas
        self.canvas.configure(yscrollcommand=pass_table_scroll.set)
        self.password_table.configure(yscrollcommand=pass_table_scroll.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all')))

        # Create another frame inside the canvas
        self.frame_in_canvas = tk.Frame(self.canvas, bg='white')
        self.canvas.create_window((0, 0), window=self.frame_in_canvas, anchor='nw')

        l1 = tk.Label(master=top_right_label_frame, text='Make Visible', bg='white')  # TODO: Define label in top_right_label frame
        l1.pack(side='top', anchor='n', pady=1)
        self.pass_table_win.update()

        # Bind the left and right click actions to functions
        self.password_table.bind('<ButtonRelease-1>', self.return_entry_id)
        self.password_table.bind('<Button-3>', self.create_right_click_menu)

        # Insert headings in to the tree view widget
        for col in cols:
            self.password_table.heading(col, text=col)

        # Adjust the row height tree view widget
        style = ttk.Style(top_left_frame)
        style.configure('Treeview', rowheight=25)

        self.update_password_table()
        self.pass_table_win.update()

        # Adjust the width and height of the canvas
        canvasWidth = l1.winfo_width()
        canvasHeight = self.password_table.winfo_height()
        self.canvas.configure(width=canvasWidth, height=canvasHeight - top_right_label_frame.winfo_height())

        self.pass_table_win.update()

        # Assign alternating colors to rows of the table
        self.password_table.tag_configure('odd_row', background='#cfd1d4')
        self.password_table.tag_configure('even_row', background='white')

        # Add the buttons
        self.show_pass_btn = tk.Button(master=bottom_frame, text="Show passwords",  width=15, command=self.show_or_hide_passwords)
        self.show_pass_btn.grid(row=0, column=0, padx=5, pady=5)

        add_entry_btn = tk.Button(bottom_frame, text="Add credentials", width=15, command=self.add_credentials_window)
        add_entry_btn.grid(row=0, column=1, padx=5, pady=5)

        change_mas_pwd_btn = tk.Button(bottom_frame, text="Change master key", width=15, command=self.change_master_password_window)
        change_mas_pwd_btn.grid(row=0, column=2, padx=5, pady=5)

        delete_all_btn = tk.Button(bottom_frame, text="Delete all", width=15, command=self.delete_all_credentials)
        delete_all_btn.grid(row=1, column=0, padx=5, pady=5)

        logout_btn = tk.Button(bottom_frame, text="Logout", width=15, command=self.logout)
        logout_btn.grid(row=1, column=1, padx=5, pady=5)

        self.pass_table_win.update()
        self.center_position_window(self.pass_table_win)


    def view_all(self, *args):
        self.password_table.yview(*args)
        self.canvas.yview(*args)


    def update_password_table(self, mask=None):
        values_to_insert = db.return_all_values()
        self.all_entries = values_to_insert
        tags = 'odd_row'
        color = '#cfd1d4'
        iid = 0

        for idx, val in enumerate(values_to_insert):
            iid += 1
            if mask or (mask is None):
                self.password_table.insert("", "end", iid=str(iid), values=(val[0], val[1], val[2], '*' * len(val[3])), tags=(tags, ))
            else:
                self.password_table.insert("", "end", iid=str(iid), values=(val[0], val[1], val[2], val[3]), tags=(tags, ))
            tags = 'even_row' if tags == 'odd_row' else 'odd_row'
            self.pass_table_win.update()

            # TODO: Delete if checkboxes doesn't work
            # Insert checkboxes color=
            var = tk.IntVar()
            ch_box = tk.Checkbutton(master=self.frame_in_canvas, text="", height=1, variable=var, bg=color, command=partial(self.check_box_callback, idx))
            ch_box.pack(side='top', fill='x', pady=0)
            self.checkbox_list.append(ch_box)
            self.chk_var_list.append(var)
            color = 'white' if color == '#cfd1d4'  else '#cfd1d4'


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


    # TODO: Delete if checkboxes doesn't work
    def check_box_callback(self, row):
        # row = self.password_table.identify_row(event.y)
        row_to_insert = self.all_entries[int(row)]
        if self.chk_var_list[row].get() == 1:
            self.password_table.item(str(row + 1), values=row_to_insert)
        else:
            self.password_table.item(str(row + 1), values=(row_to_insert[0], row_to_insert[1], row_to_insert[2], ('*' * len(row_to_insert[3]))))


    def copy_data(self, row, column):
        column = int(column[-1]) - 1
        row = int(row[-1]) - 1
        text_to_copy = self.all_entries[int(row)][column]
        pyperclip.copy(str(text_to_copy))


    def return_entry_id(self, event):
        self.password_table.focus()
        # print(type(self.password_table.focus()))
        # focus = self.password_table.focus()
        # self.update_or_delete = self.password_table.item(focus, 'values')


    def update_credentials_window(self, row):
        idx = int(row[-1]) - 1
        entry = self.all_entries[idx]

        self.update_cred_win = tk.Toplevel()
        self.update_cred_win.bind('<Return>', lambda: self.update_btn_command(idx))

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
            self.refresh_password_table()
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
                self.refresh_password_table()
                self.pass_table_win.wait_window()
            else:
                messagebox.showwarning("Credential Delete Failed", "The entry " + ', '.join(entry_to_delete[1:]) + " couldn't be deleted.")
                self.pass_table_win.wait_window()
        else:
            self.pass_table_win.wait_window()


    def add_credentials_window(self):
        self.cred_win = tk.Toplevel()
        self.cred_win.title("Add Credentials")
        self.cred_win.title = 'Add a new entry'
        self.cred_win.bind('<Return>', self.add_btn_command)

        web_label = tk.Label(self.cred_win, text="Enter the website")
        web_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

        self.web_field = tk.Entry(self.cred_win)
        self.web_field.grid(row=0, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

        user_label = tk.Label(self.cred_win, text="Enter the username")
        user_label.grid(row=1, column=0, padx=5, pady=5, sticky='w')

        self.user_field = tk.Entry(self.cred_win)
        self.user_field.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

        pass_label = tk.Label(self.cred_win, text="Enter the passsword")  # TODO: Insert the parameter show='*'
        pass_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

        self.pass_field = tk.Entry(self.cred_win)
        self.pass_field.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky='ew')

        add_btn = tk.Button(self.cred_win, text='Add', command=self.add_credentials)
        add_btn.grid(row=3, column=0, padx=5, pady=5, sticky='ew')

        gen_pass_btn = tk.Button(self.cred_win, text='Generate Password', command=self.generate_password)
        gen_pass_btn.grid(row=3, column=1, padx=5, pady=5, sticky='ew')

        cancel_btn = tk.Button(self.cred_win, text='Cancel', command=lambda: self.cred_win.destroy())
        cancel_btn.grid(row=3, column=2, padx=5, pady=5, sticky='ew')

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
        # values = db.return_all_values()
        # val_to_add = values[-1]
        # iid = len(values) + 1

        # var = tk.IntVar()
        # self.password_table.insert("", "end", iid=str(iid), values=(val_to_add[0], val_to_add[1], val_to_add[2], ('*' * len(val_to_add[3]))))
        # ch_box = tk.Checkbutton(master=self.top_right_frame, text="", variable=var, command=partial(self.check_box_callback, len(values)))
        messagebox.showinfo("Added Credentials", "The password has been successfully added to the vault")
        self.refresh_password_table()
        self.pass_table_win.wait_window()


    def generate_password(self):
        lower_case = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        upper_case = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        spl_char = ['!', '§', '$', '%', '&', '/', '(', ')', '=', '?']

        # password_length = 14
        num_lower_case = 4
        num_upper_case = 4
        num_numbers = 3
        num_spl_char = 3

        password = []

        # Random selection of lower case letters
        for ii in range(num_lower_case + 1):
            char = random.choice(lower_case)
            password.append(char)

        # Random selection of upper case letters
        for ii in range(num_upper_case + 1):
            char = random.choice(upper_case)
            password.append(char)

        # Random selection of numbers
        for ii in range(num_numbers + 1):
            char = random.choice(numbers)
            password.append(char)

        # Random selection of special characters
        for ii in range(num_spl_char + 1):
            char = random.choice(spl_char)
            password.append(char)

        # Shuffle the password
        random.shuffle(password)
        password = ''.join(password)

        self.pass_field.delete('0', tk.END)
        self.pass_field.insert('0', string=password)


    def delete_all_credentials(self):
        ans = messagebox.askyesnocancel("Delete all credentials", "Are you sure you want to delete all credentials and clear the vault?")
        if ans:
            db.remove_all_values()
            self.refresh_password_table()
        else:
            self.pass_table_win.wait_window()


    def refresh_password_table(self):
        self.password_table.delete(*self.password_table.get_children())
        self.delete_checkboxes()
        self.update_password_table()


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


    def show_or_hide_passwords(self):
        text = self.show_pass_btn.cget("text")
        self.password_table.delete(*self.password_table.get_children())
        self.delete_checkboxes()

        if text == "Show passwords":
            self.update_password_table(mask=False)
            # TODO: set all intvar to 1 and select all checkboxes
            self.show_pass_btn.configure(text="Hide passwords")
        elif text == "Hide passwords":
            self.update_password_table(mask=True)
            # TODO: set all intvar to 0 and deselect all checkboxes
            self.show_pass_btn.configure(text="Show passwords")


    def delete_checkboxes(self):
        for widget in self.canvas.winfo_children():
            if isinstance(widget, tk.Checkbutton):
                widget.destroy()
        self.checkbox_list = []
        self.chk_var_list = []


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


    def update_btn_command(self, event, idx):
        self.update_credentials(idx)


    def add_btn_command(self, event):
        self.add_credentials()


    def change_pass_btn_command(self, event):
        self.change_master_password()


if __name__ == '__main__':
    ui = UserInterface()
