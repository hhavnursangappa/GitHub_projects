#include <iostream>
#include <string>
#include "Book.h"
#include "Inventory.h"

using namespace std;

Inventory _inventory; // underscore to denote that it is a global variable

int main()
{
    while (true)
    {
        int choice;

        cout << "\nChoose an option: \n";
        cout << "1 = Add Book\n";
        cout << "2 = List all Books\n";
        cout << "3 = Checkout a Book\n";
        cout << "4 = Checkin a Book\n";
        cout << "0 = Exit\n";

        cin >> choice;
        cin.ignore(); // When 'cin' and 'getline' are used together, it may cause some problems. So adding this will resolve it

        switch (choice)
        {
            case 0:
            {
                cout << "Thank you. Goodbye !";
                return 0;
            }

            case 1:
            {
                string title, author;
                int id;

                cout << "Title: ";
                getline(cin, title);

                cout << "Author: ";
                getline(cin, author);
                
                id = _inventory.Books.size() + 1;

                Book newBook(id, title, author);
                _inventory.AddBook(newBook);

                cout << "The book has been successfully added\n";
                break;
            }

            case 2:
            {
                // int ii;
                cout << "ID"
                    << "\t"
                    << "TITLE"
                    << "\t"
                    << "AUTHOR" << endl;
                for (int ii = 0; ii < _inventory.Books.size(); ii++)                    
                {
                    cout << _inventory.Books[ii].Id << "\t" << _inventory.Books[ii].Title << "\t" << _inventory.Books[ii].Author << endl;
                }

                break;
            }

            case 3:
            {
                string title;
                bool res;

                cout << ("Enter the title of the book to checkout: ");
                getline(cin, title);
                Book foundBook;

                res = _inventory.FindBookByTitle(title, foundBook);
                if (res)
                {
                    if (foundBook.CheckedOut)
                    {
                        cout << "Book has already been checked out !\n";
                    }
                    else
                    {
                        _inventory.CheckOutBook(foundBook);
                        cout << "Book is successfully checked out !\n";
                    }
                }
                break;
            }

            case 4:
            {
                string title;
                bool res;

                cout << ("Enter the title of the book to checkin: ");
                getline(cin, title);
                Book foundBook;

                res = _inventory.FindBookByTitle(title, foundBook);
                if (!res)
                {
                    if (!foundBook.CheckedOut)
                    {
                        cout << "Book already checked in\n";
                    }

                    else
                    {
                        _inventory.CheckInBook(foundBook);
                        cout << "Book successfully checked in!\n";
                    }
                }
                break;
            }

        }
    }
}