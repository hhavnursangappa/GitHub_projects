from sql_setup import Database
import sys

db = Database()  # Instantiate the database object


def manager():

    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    print("Welcome to your password manager.")
    print("1. Login to your password vault\n"
          "2. Create a password vault")
    print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    choice = int(input("Enter what you wish to do: "))
    if choice == 1:
        m_user = str(input("Enter the master username: "))
        user_exists = db.is_present_user(m_user)
        if user_exists:
            login_password_vault(m_user)
        else:
            create_password_vault()

    elif choice == 2:
        create_password_vault()


def create_password_vault():
    print("You have not yet created a vault. Create one by entering the master username and a master password")
    master_user = str(input("Master Username: "))
    master_pass = str(input("Master Password: "))
    db.create_master_password_table(master_user, master_pass)
    # db.update_master_password_table(master_user, master_pass)
    print("\nA Vault has been successfully created for you. Now you can do the following: ")
    menu()


def login_password_vault(m_user):
    m_pwd = db.return_master_password(m_user)
    pass_key = str(input("Enter the master passkey: "))
    attempt = 0
    while pass_key != m_pwd[0][1]:
        if attempt <= 3:
            pass_key = str(input(f"Wrong password. You have {3 - attempt} attempts left. Please try again: "))
            attempt += 1
        else:
            print("You have exhausted your atttempts. Try again after 24 hrs")
            quit()

    print("Horray! You have successfully logged in")
    print('\n')
    menu()


def print_entries(entries):
    print("*************************************************************************************")
    print("|\tWEBSITE\t|\tUSERNAME\t|\tPASSWORD\t|")
    for entry in entries:
        row = []
        row.append(entry[0])
        row.append(entry[1])
        row.append(entry[2])

        print('|\t' + '\t|\t'.join(row) + '\t|')
    print("*************************************************************************************")


def menu():
    sel = None
    while sel != 6:
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("1. Create a new entry\n"
              "2. View all entries\n"
              "3. Filter entry\n"
              "4. Delete an existing entry\n"
              "5. Delete all entries\n"
              "6. Logout")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

        sel = int(input("Enter your selection: "))

        if sel == 1:
            web = str(input("Enter the website: "))
            username = str(input("Enter the username: "))
            password = str(input("Enter the password: "))
            db.insert_values(web, username, password)
            print(f"The password has been successfully added to the vault")
            print('\n')

        elif sel == 2:
            print("The entries in the database are as follows: ")
            values = db.print_all_values()
            if len(values) == 0:
                print("The vault is empty. Start adding some passwords\n")
            else:
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
            inp_arg = str(input("Enter the username or the website for which you would like to delete the password for: "))
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

    db.conn.close()
    print("You have successfully logged out of the vault. Have a nice day ahead!")
    sys.exit()


if __name__ == '__main__':
    manager()