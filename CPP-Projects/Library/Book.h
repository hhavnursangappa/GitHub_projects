#ifndef BOOK
#define BOOK
#include <iostream>
#include <string>

//using namespace std;

class Book
{
public:
	int Id;
	std::string Title;
	std::string Author;
	bool CheckedOut = false;
	//---------------------------------------------------------------------------------------------------------------------------
	Book();
	Book(int id, std::string title, std::string author);
	//---------------------------------------------------------------------------------------------------------------------------
	bool operator==(const Book &book)
	{
		if (Title.compare(book.Title) == 0)
			return true;
		else
			return false;
	}
};
#endif