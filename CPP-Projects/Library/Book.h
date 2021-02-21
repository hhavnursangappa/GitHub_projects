#pragma once
// 'pragma once' avoids inclusind this header file if it is already included

#include <iostream>

class Book
{
public:
	int Id;
	std::string Title;
	std::string Author;
	bool CheckedOut;
	
	Book(); // Defining another constructor for the class 'Book'
	Book(int id, std::string title, std::string author); // Defining the constructor for the class 'Book'



	/* Syntax for operator overloading:
	<return_data_type> operaotor <operand>(const <name of the user defined class> &input_argument)
	{
		code block;
	}

	If the overloading is done outside the class then specify 2 operands as input arguments
	*/

	bool operator == (const Book &book) const  // Overloading the '==' operator. 
	{
		if (Title.compare(book.Title) == 0)
			return true;
		else
			return false;
	}
};