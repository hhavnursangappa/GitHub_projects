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
void Inventory::RemoveBook(std::string title)
{
	std::vector<Book>::iterator pos = std::find(Inventory::Books.begin(), Inventory::Books.end(), Book(0, title, ""));
	if (pos != Inventory::Books.end())
	{
		Inventory::Books.erase(pos);
	}
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
int Inventory::FindBookByTitle(std::string title)
{
	/* This is an iterator in C++. The begin() method points to the first element 
	of the vector and the end() method pints to the last element of the vector. This means iterate through the vector from first to last and find the object Book(0, title, ""). This avoids the use 
	of another for loop for the same purpose */
	std::vector<Book>::iterator it = std::find(Inventory::Books.begin(), Inventory::Books.end(), Book(0, title, "")); // str::find returns the position of the element
	if (it == Inventory::Books.end())																				  // == Books.end() means the element was not found
	{
		return -1;
	}
	int index = it - Inventory::Books.begin(); // Try without Books.begin()
	return index;
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void Inventory::CheckOutBook(Book *book)
{
	book->CheckedOut = true; // '->' has to be used to acces the properties of the pointer
}
//-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
void Inventory::CheckInBook(Book *book)
{
	book->CheckedOut = false; // '->' has to be used to acces the properties of the pointer
}
