#include "stdafx.h"
#include "Inventory.h"

void Inventory::AddBook(Book book)
{
	Inventory::Books.push_back(book);
}

bool Inventory::FindBookByTitle(std::string title, Book &book)
{
	std::vector<Book>::iterator it = std::find(Inventory::Books.begin(), Inventory::Books.end(), Book(0, title, "")); /* This is an iterator in C++. The begin() method points to the first element 
	of the vector and the end() method pints to the last element of the vector. This means iterate through the vector from first to last and find the object Book(0, title, ""). This avoids the use 
	of another for loop for the same purpose */

	if (it != Inventory::Books.end())  
	{
		book = *it;
		return true;
	}

	return false;

}

void Inventory::CheckOutBook(Book &book)
{
	book.CheckedOut = true;
}

void Inventory::CheckInBook(Book &book)
{
	book.CheckedOut = false;
}