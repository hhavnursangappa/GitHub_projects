#include <iostream>
#include <string>
#include "Book.h"
#include "Inventory.h"
// #include "CheckInOrOutResult.h"

using namespace std;

Inventory _inventory; // underscore to denote that it is a global variable
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void DisplayMainMenu()
{
    cout << "\nChoose an option: \n";
    cout << "1 = Add Book\n";
    cout << "2 = List all Books\n";
    cout << "3 = Checkout a Book\n";
    cout << "4 = Checkin a Book\n";
    cout << "5 = Remove book from library\n";
    cout << "6 = List all checked out books\n";
    cout << "0 = Exit\n";
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void ListAllBooks()
{
    _inventory.DisplayAllBooks();
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void RemoveBook()
{
    string title;

    cout << "Enter the title of the book you wish to remove: ";
    getline(cin, title);

    _inventory.RemoveBook(title);

    cout << "The book has been successfully removed\n";
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
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
    else
    {
        cout << "Book failed checcking " << inOrOut << endl;
    }
}
    /* int foundBookIndex = _inventory.FindBookByTitle(title);
    if (foundBookIndex >= 0)
    {
        Book *foundBook = _inventory.GetBookByIndex(foundBookIndex);
        // Book *foundBook = &bookObj; // Every time 'foundBook' is created it creates a copy of the  Book object and even though we edit the attribute of the object, when we run it again, a copy of it will be generated. Therefore in order to edit the attributes of the object we create a pointer to the memory of this object. This will allow us to edit the properties of the same 'foundBook' object that was created and not a copy of it.
        // bool &value = foundBook->CheckedOut;
        // Book foundBookAddress = &foundBook;
        if (foundBook->CheckedOut == checkOut) // '->' has to be used to acces the properties of the pointer
        {
            cout << "Book has already been checked " + inOrOut + "!\n";
            return;
        }

        if (checkOut)
        {
            _inventory.CheckOutBook(foundBook);
            cout << "Book is successfully checked out !\n";
            
        }

        else
        {
            _inventory.CheckInBook(foundBook);
        }
    } */
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void DisplayCheckedOutBooks()
{
    _inventory.DisplayCheckedOutBooks();
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
int main()
{
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