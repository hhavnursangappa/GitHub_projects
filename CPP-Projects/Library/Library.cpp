// Library.cpp : Defines the entry point for the console application.
//

#include "stdafx.h"
#include "Book.h"
#include "Inventory.h"
#include <string>

using namespace std;

Inventory _inventory;  // Declare a global class object for an inventory '_' to denote it is a global variable

int main()
{
	while (true)
	{
		cout << "Choose an option: " << endl;
		cout << "1. Add Book " << endl;
		cout << "2. List all Books" << endl;
		cout << "3. Check out book" << endl;
		cout << "4. Check in book" << endl;
		cout << "0. Exit" << endl;
		
		int input;
		cin >> input;
		cin.ignore();  // When 'cin' and 'getline' are used together, it may cause some problems. So adding this will resolve it

		switch (input)
		{
			case 0:
				cout << "Thank you. Goodbye" << endl;
				return 0;

			case 1:
			{
				cout << "Title: ";
				string title;
				getline(cin, title);

				cout << "Author: ";
				string author;
				getline(cin, author);

				int id = _inventory.Books.size() + 1;

				Book newBook(id, title, author);
				_inventory.AddBook(newBook);
				break;
			}

			case 2:
				cout << "ID\tTitle\tAuthor" << endl;
				for (int ii = 0; ii < _inventory.Books.size(); ii++)
				{
					cout << _inventory.Books[ii].Id << "\t" << _inventory.Books[ii].Title << "\t" << _inventory.Books[ii].Author << endl;
				}	
				cout << endl;
				break;

			case 3:
			{
				cout << "Enter the title of a book to check out: ";
				string title;
				getline(cin, title);
				Book foundBook;
				if (_inventory.FindBookByTitle(title, foundBook))
				{
					if (foundBook.CheckedOut)
					{
						cout << "Book alreday checked out !\n";
						break;
					}

					_inventory.CheckOutBook(foundBook);
					cout << "Book checked out!\n" << endl;
				}
				else
				{
					cout << "Book not found\n" << endl;
				}
				break;
			}
				

			case 4:
			{
				cout << "Enter the title of a book to check in: ";
				string title;
				getline(cin, title);
				Book foundBook;
				if (_inventory.FindBookByTitle(title, foundBook))
				{
					if (!foundBook.CheckedOut)
					{
						cout << "Book alreday checked in !\n";
						break;
					}
					else
					{
						_inventory.CheckInBook(foundBook);
						cout << "Book checked in!\n" << endl;
					}
					
				}
				else
				{
					cout << "Book not found\n" << endl;
				}
				break;
			}	

			default:
				cout << "Invalid Selection. Try again" << endl;
		}

	}
	return 0;
}

