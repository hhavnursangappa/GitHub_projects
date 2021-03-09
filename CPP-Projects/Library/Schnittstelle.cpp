#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include <fstream>
#include "Book.h"
#include "Inventory.h"
#include "User.h" 

// #include "CheckInOrOutResult.h"

using namespace std;

Inventory _inventory; // Underscore to denote that it is a global variable
vector<User> _users; 
User _loggedInUser;

//------------------------------------------------------------------------------------------------------

Role GetRoleFromIntVal(int roleVal)
{
    Role outRole;

    if (roleVal == 0)
        outRole = Role::Admin;
    else if (roleVal == 1)
        outRole = Role::Employee;
    else if (roleVal == 2)
        outRole = Role::Member;
    return outRole;
}
//------------------------------------------------------------------------------------------------------

void LoadUsers()
{
    ifstream inFile("users.txt");
    string listData[2];

    string userLine;
    while(getline(inFile, userLine))
    {
        size_t index = userLine.find("|");

        listData[0] = userLine.substr(0, index);
        listData[1] = userLine.substr(index + 1);

        User loadedUser;
        loadedUser.Username = listData[0];
        loadedUser.Role = GetRoleFromIntVal(stoi(listData[1])); // 'stoi' is a function to vonvert from string to integer

        _users.push_back(loadedUser);        
    }    
}
//------------------------------------------------------------------------------------------------------

int GetIntValFromRole(Role role)
{
    int rolVal = -1;
    if (role == Role::Admin)
        rolVal = 0;
    else if (role == Role::Employee)
        rolVal = 1;
    else if (role == Role::Member)
        rolVal = 2;
    return rolVal;
}
//------------------------------------------------------------------------------------------------------

void CreateAccount()
{
    User newUser;

    /* cout << "\nEnter FirstName: ";
    getline(cin, newUser.FirstName);

    cout << "Enter LastName: ";
    getline(cin, newUser.LastName); */

    cout << "Enter Username: ";
    cin >> newUser.Username;

    cout << "\nEnter a choice for the role: \n";
    cout << "1: Admin \n";
    cout << "2: Employee \n";
    cout << "3: Member \n" << endl; 

    int roleChoice;
    cin >> roleChoice;
    cin.ignore();

    if (roleChoice == 1)
        newUser.Role = Role::Admin;
    else if (roleChoice == 2)
        newUser.Role == Role::Employee;
    else if (roleChoice == 3)
        newUser.Role = Role::Member;
        
    _users.push_back(newUser);

    ofstream oFile("users.txt", ios_base::app);
    oFile << newUser.Username << "|" << GetIntValFromRole(newUser.Role) << endl;
    oFile.close(); 
}
//------------------------------------------------------------------------------------------------------

void Login()
{
    while (true)
    {    
        cout << "\nEnter your choice: " << endl;
        cout << "1. Login" << endl;
        cout << "2. Create Account" << endl;

        int choice;
        cin >> choice;
        cin.ignore();

        if (choice == 1)
        {
            while (true)
            {
                string username;
                cout << "Enter username: ";
                cin >> username;

                // Create a user object with the above username
                User user;
                user.Username = username;

                vector<User>::iterator it = find(_users.begin(), _users.end(), user);

                if (it != _users.end())
                {
                    _loggedInUser = _users[it - _users.begin()];
                    break;
                }
            }
        }

        else if (choice == 2)
        {
            CreateAccount();
        }

        else
            cout << "Invalid choice. Please choose from the menu\n";
            // delete choice;            
    }
}
//------------------------------------------------------------------------------------------------------

void DisplayMainMenu()
{
    cout << "\nChoose an option: \n";
    cout << "1 = List all Books\n";
    cout << "2 = Checkout a Book\n";
    cout << "3 = Checkin a Book\n";

    if (_loggedInUser.Role == Role::Employee || _loggedInUser.Role == Role::Admin)
    {
        cout << "4 = Add Book\n";
        cout << "5 = Remove book from library\n";
        cout << "6 = List all checked out books\n";
        cout << "7 = Logout user\n";
    }
    
    cout << "0 = Exit\n";
}
//------------------------------------------------------------------------------------------------------

void AddNewbook()
{
    string title, author;
    int id;

    cout << "Title: ";
    getline(cin, title);

    cout << "Author: ";
    getline(cin, author);

    // id = _inventory.GetNextBookId();

    Book newBook(title, author);
    _inventory.AddBook(newBook);

    cout << "The book has been successfully added\n";
}
//------------------------------------------------------------------------------------------------------

void ListAllBooks()
{
    _inventory.DisplayAllBooks();
}
//------------------------------------------------------------------------------------------------------

void RemoveBook()
{
    string title;

    cout << "Enter the title of the book you wish to remove: ";
    getline(cin, title);

    _inventory.RemoveBook(title);

    cout << "The book has been successfully removed\n";
}
//------------------------------------------------------------------------------------------------------

void CheckInOrOutBook(bool checkOut)
{
    string title;
    string inOrOut;

    if (checkOut)
    {
        inOrOut = "out";
    }
    else
    {
        inOrOut = "in";
    }

    cout << "Enter the title of the book to check " + inOrOut + ": ";
    getline(cin, title);

    CheckInOrOutResult result = _inventory.CheckInOrOutBook(title, checkOut);

    if (result == CheckInOrOutResult::BookNotFound)
    {
        cout << "Book not found" << endl;
    }

    else if (result == CheckInOrOutResult::Success)
    {
        cout << "Book checked " << inOrOut + "!" << endl;
    }
    else if (result == CheckInOrOutResult::AlreadyCheckedOut || result == CheckInOrOutResult::AlreadyCheckedIn)
    {
        cout << "Book already checked " + inOrOut << endl;
    }    
    else 
    {
        cout << "Book failed checcking " << inOrOut << endl;
    }
}
//------------------------------------------------------------------------------------------------------

void DisplayCheckedOutBooks()
{
    _inventory.DisplayCheckedOutBooks();
}
//------------------------------------------------------------------------------------------------------

int main()
{
    LoadUsers();

    while (true)
    {
        Login();
        _inventory.LoadBooks();
        bool isLoggedIn =true;

        while (isLoggedIn)
        {
            DisplayMainMenu();

            int choice;
            cin >> choice;
            cin.ignore(); // When 'cin' and 'getline' are used together, it may cause some problems. So adding this will resolve it

            switch (choice)
            {
            case 0:
                cout << "Thank you. Goodbye !\n" << endl;
                return 0;

            case 1:
                ListAllBooks();            
                break;

            case 2:
                CheckInOrOutBook(true);
                break;

            case 3:
                CheckInOrOutBook(false);
                break;

            case 4:
                AddNewbook();
                break;

            case 5:
                RemoveBook();
                break;

            case 6:
                DisplayCheckedOutBooks();
                break;

            case 7:
                isLoggedIn = false;
                break;

            default:
                cout << "Invalid Selection. Try again!\n"
                    << endl;
                break;
            }
        }
    }
}