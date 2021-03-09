#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <algorithm>
#include "Inventory.h"
#include "Book.h"

using namespace std;

void Inventory::AddBook(Book book)
{
	int nextBookId = 0;

	if (Inventory::Books.size() > 0)
		nextBookId = Inventory::Books.back().Id + 1;

	book.Id = nextBookId;
	Inventory::Books.push_back(book);

	// Write Books into a file
	ofstream oFile("book.txt", ios_base::app);
	oFile << book.GetBookFileData() << endl;
	oFile.close();
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
	/* Every time 'foundBook' is created it creates a copy of the  Book object and even though we edit the attribute of the object, when we run it again, a copy of it will be generated. Therefore in order to edit the attributes of the object we create a pointer to the memory of this object. This will allow us to edit the properties of the same 'foundBook' object that was created and not a copy of it.*/

	int foundBookIndex = FindBookByTitle(title);

	if (foundBookIndex < 0)
	{
		return CheckInOrOutResult::BookNotFound;
	}

	else if (checkOut == Books[foundBookIndex].IsCheckedOut())
	{
		if (checkOut)
		{
			return CheckInOrOutResult::AlreadyCheckedOut;
		}
		else
		{
			return CheckInOrOutResult::AlreadyCheckedIn;
		}
	}

	Inventory::Books[foundBookIndex].CheckInOrOut(checkOut);
	ofstream oFile("book.txt");
	for (int ii=0; ii < Inventory::Books.size(); ii++) 
	{
		oFile << Inventory::Books[ii].GetBookFileData() << endl;
	}

	oFile.close();
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

void Inventory::LoadBooks()
{
	Inventory::Books.clear();
	ifstream iFile("book.txt");

	string BookData[7];
	string BookLine;

	while (getline(iFile, BookLine))
{		
		// Extract Id
		size_t index = BookLine.find("|");
		BookData[0] = BookLine.substr(0, index);

		// Extract Title
		size_t prevIndex = index;
		size_t nextIndex = BookLine.find("|", index+1);
		BookData[1] = BookLine.substr(prevIndex + 1, nextIndex - prevIndex - 1);

		// Extract Author
		size_t newIndex = nextIndex;
		size_t newNextIndex = BookLine.find("|", newIndex + 1);
		BookData[2] = BookLine.substr(newIndex + 1, newNextIndex - newIndex - 1);

		// Extract Checckout status
		size_t newNewIndex = BookLine.find("|", newNextIndex + 1);
		BookData[3] = BookLine.substr(newNextIndex + 1, newNewIndex - newNextIndex - 1);

		Book loadedBook(BookData[1], BookData[2]);
		loadedBook.Id = stoi(BookData[0]);		

		loadedBook.CheckInOrOut(stoi(BookData[3]));

		Inventory::Books.push_back(loadedBook);
	}
}
//-------------------------------------------------------------------------------------------------------