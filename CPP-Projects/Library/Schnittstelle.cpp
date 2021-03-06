#include <iostream>
#include <string>
#include <vector>
#include <algorithm>
#include "Book.h"
#include "Inventory.h"
#include "User.h"

// #include "CheckInOrOutResult.h"

using namespace std;

Inventory _inventory; // underscore to denote that it is a global variable
vector<User> _users; 
User _loggedInUser;
//-------------------------------------------------------------------------------------------------------

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
}
//-------------------------------------------------------------------------------------------------------

void Login()
{
    cout << "\nEnter your choice: " << endl;
    cout << "1. Login" << endl;
    cout << "2. Create Account" << endl;

    int choice;
    cin >> choice;

    // if (choice == 1)
        // EnterLogin();
    if (choice == 2)
        CreateAccount();
    
    string username;
    cout << "Enter username: " << endl;
    cin >> username;

    // Create a user object with the above username
    User user;
    user.Username = username;

    vector<User>::iterator it = find(_users.begin(), _users.end(), user);

    if (it != _users.end())
    {
        _loggedInUser = _users[it - _users.begin()];
    }    
}
//-------------------------------------------------------------------------------------------------------

void DisplayMainMenu()
{
    cout << "\nChoose an option: \n";

    if (_loggedInUser.Role == Role::Employee || _loggedInUser.Role == Role::Admin)
    {
        cout << "1 = Add Book\n";
        cout << "5 = Remove book from library\n";
        cout << "6 = List all checked out books\n";
    }
    
    cout << "2 = List all Books\n";
    cout << "3 = Checkout a Book\n";
    cout << "4 = Checkin a Book\n";
    cout << "0 = Exit\n";
}
//-------------------------------------------------------------------------------------------------------

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
//-------------------------------------------------------------------------------------------------------

void ListAllBooks()
{
    _inventory.DisplayAllBooks();
}
//-------------------------------------------------------------------------------------------------------

void RemoveBook()
{
    string title;

    cout << "Enter the title of the book you wish to remove: ";
    getline(cin, title);

    _inventory.RemoveBook(title);

    cout << "The book has been successfully removed\n";
}
//-------------------------------------------------------------------------------------------------------

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
//-------------------------------------------------------------------------------------------------------

void DisplayCheckedOutBooks()
{
    _inventory.DisplayCheckedOutBooks();
}
//-------------------------------------------------------------------------------------------------------

int main()
{
    Login();

    while (true)
    {
        int choice;

        DisplayMainMenu();

        cin >> choice;
        cin.ignore(); // When 'cin' and 'getline' are used together, it may cause some problems. So adding this will resolve it

        switch (choice)
        {
        case 0:
            cout << "Thank you. Goodbye !\n"
                 << endl;
            return 0;

        case 1:
            AddNewbook();
            break;

        case 2:
            ListAllBooks();
            break;

        case 3:
            CheckInOrOutBook(true);
            break;

        case 4:
            CheckInOrOutBook(false);
            break;

        case 5:
            RemoveBook();
            break;

        case 6:
            DisplayCheckedOutBooks();
            break;

        default:
            cout << "Invalid Selection. Try again!\n"
                 << endl;
            break;
        }
    }
}