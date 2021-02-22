#include <iostream>
#include <vector>
#include <string>
#include "Inventory.h"
#include "Book.h"
#include <algorithm>

void Inventory::AddBook(Book book)
{
	Inventory::Books.push_back(book);
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
/*void Inventory::RemoveBook(Book book)
{
	std::vector<Book>::iterator pos = std::find(Inventory::Books.begin(), Inventory::Books.end(), book);
	if (pos != Inventory::Books.end())
	{
		Inventory::Books.erase(pos);
	}
}*/
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
bool Inventory::FindBookByTitle(std::string title, Book &book)
{
	/* This is an iterator in C++. The begin() method points to the first element 
	of the vector and the end() method pints to the last element of the vector. This means iterate through the vector from first to last and find the object Book(0, title, ""). This avoids the use 
	of another for loop for the same purpose */
	std::vector<Book>::iterator it = std::find(Inventory::Books.begin(), Inventory::Books.end(), Book(0, title, "")); // str::find returns the position of the element
	if (it != Inventory::Books.end()) // == Books.end() means the element was not found
	{
		book = *it;
		return true;
	}
	return false;
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void Inventory::CheckOutBook(Book &book)
{
	book.CheckedOut = true;
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void Inventory::CheckInBook(Book &book)
{
	book.CheckedOut = false;
}
