#include <iostream>
#include <string>
#include <vector>
#include "Book.h"
#include "CheckInOrOutResult.h"

class Inventory
{
private:
	int MaxBookId;
	std::vector<Book> Books;

public:
	Inventory();

	//int GetNextBookId();  // Avoided this function as it may be abused by users to simply incerment the Id without adding books
	int NumberOfBooks();
	Book GetBookByIndex(int index);
	void AddBook(Book book);
	void RemoveBook(std::string title);
	int FindBookByTitle(std::string title);
	CheckInOrOutResult CheckInOrOutBook(std::string title, bool checkOut);
	void DisplayAllBooks();
	void DisplayCheckedOutBooks();
};