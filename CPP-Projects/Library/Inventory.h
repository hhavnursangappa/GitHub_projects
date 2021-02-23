#include <iostream>
#include <string>
#include <vector>
#include "Book.h"

class Inventory
{
public:
	std::vector<Book> Books;

	void AddBook(Book book);
	void RemoveBook(std::string title);
	int FindBookByTitle(std::string title);
	void CheckOutBook(Book *book);
	void CheckInBook(Book *book);
};