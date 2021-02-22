#ifndef BOOK_H // Avoids inclusind this header file if it is already included
#define BOOK_H
#include <iostream>
#include <string>

//using namespace std;

class Book
{
public:
	int Id;
	std::string Title;
	std::string Author;
	bool CheckedOut;
	//---------------------------------------------------------------------------------------------------------------------------
	Book(); // Declaration of the default constructor for the class 'Book'
	Book(int id, std::string title, std::string author); // Declaration of the custom constructor for the class 'Book'
	//---------------------------------------------------------------------------------------------------------------------------
	/* Syntax for operator overloading:
	<return_data_type> operator <operand>(const <name of the user defined class> &input_argument)
	{
		code block;
	}

	If the overloading is done outside the class then specify 2 operands as input arguments */
	
	bool operator==(const Book &book)
	{
		if (Title.compare(book.Title) == 0)
			return true;
		else
			return false;
	}
};
#endif