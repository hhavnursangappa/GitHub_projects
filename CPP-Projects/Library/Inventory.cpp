#include <iostream>
#include <vector>
#include <string>
#include "Inventory.h"
#include "Book.h"
#include <algorithm>

using namespace std;

Inventory::Inventory()
{
	Inventory::MaxBookId = 0;
}
//-------------------------------------------------------------------------------------------------------

void Inventory::AddBook(Book book)
{
	Inventory::MaxBookId++;
	book.SetBookId(MaxBookId);
	Inventory::Books.push_back(book);
}
//-------------------------------------------------------------------------------------------------------

Book Inventory::GetBookByIndex(int index)
{
	return Inventory::Books[index];
}
//-------------------------------------------------------------------------------------------------------

int Inventory::NumberOfBooks()
{
	return Inventory::Books.size();
}
//-------------------------------------------------------------------------------------------------------

void Inventory::RemoveBook(std::string title)
{
	//TODO: Handle MaxBookId when the entry with the MaxBookId is deleted

	std::vector<Book>::iterator pos = std::find(Inventory::Books.begin(), Inventory::Books.end(), Book(title, ""));
	if (pos != Inventory::Books.end())
	{
		Inventory::Books.erase(pos);
	}
}
//-------------------------------------------------------------------------------------------------------

int Inventory::FindBookByTitle(std::string title)
{
	/* This is an iterator in C++. The begin() method points to the first element 
	of the vector and the end() method pints to the last element of the vector. This means iterate through the vector from first to last and find the object Book(0, title, ""). This avoids the use 
	of another for loop for the same purpose */

	std::vector<Book>::iterator it = std::find(Inventory::Books.begin(), Inventory::Books.end(), Book(title, "")); // str::find returns the position of the element

	if (it == Inventory::Books.end()) // "== Books.end()" means the element was not found
	{
		return -1;
	}
	int index = it - Inventory::Books.begin();
	return index;
}
//-------------------------------------------------------------------------------------------------------

CheckInOrOutResult Inventory::CheckInOrOutBook(std::string title, bool checkOut)
{
	int foundBookIndex = FindBookByTitle(title);

	if (foundBookIndex < 0)
	{
		return CheckInOrOutResult::BookNotFound;
	}

	Books[foundBookIndex].CheckInOrOut(checkOut);
	return CheckInOrOutResult::Success;
}
//-------------------------------------------------------------------------------------------------------

void Inventory::DisplayAllBooks()
{
	cout << "ID"
		 << "\t"
		 << "TITLE"
		 << "\t"
		 << "AUTHOR" << endl;
	for (int ii = 0; ii < NumberOfBooks(); ii++)
	{
		Books[ii].DisplayBook();
	}
}
//-------------------------------------------------------------------------------------------------------

void Inventory::DisplayCheckedOutBooks()
{
	cout << "ID"
		 << "\t"
		 << "TITLE"
		 << "\t"
		 << "AUTHOR" << endl;
	for (int ii = 0; ii < NumberOfBooks(); ii++)
	{
		if (GetBookByIndex(ii).IsCheckedOut())
		{
			Books[ii].DisplayBook();
		}
	}
}
//-------------------------------------------------------------------------------------------------------
