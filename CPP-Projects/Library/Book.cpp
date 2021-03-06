#include <iostream>
#include <string>
#include "Book.h"

using namespace std;

// Defining the Default constructor
Book::Book(){}
//-------------------------------------------------------------------------------------------------------
// Defining the custom constructor
Book::Book(string title, string author)
{
	Title = title;
	Author = author;
	CheckedOut = false;
}
//-------------------------------------------------------------------------------------------------------
void Book::CheckInOrOut(bool checkOut)
{
	CheckedOut = checkOut;
}
//-------------------------------------------------------------------------------------------------------
void Book::DisplayBook()
{
	cout << Id << "\t" << Title << "\t" << Author << endl;
}
//-------------------------------------------------------------------------------------------------------
bool Book::IsCheckedOut()
{
	return CheckedOut;
}
//-------------------------------------------------------------------------------------------------------
std::string Book::GetBookFileData()
{
	return to_string(Id) + "|" + Title + "|" + Author + "|" + (CheckedOut ? "1" : "0");
}
//-------------------------------------------------------------------------------------------------------
