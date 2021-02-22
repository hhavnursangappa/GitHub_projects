#include <iostream>
#include <string>
#include "Book.h"

using namespace std;

// Defining the Default constructor
Book::Book()
{
}

// Defining the custom constructor
Book::Book(int id, string title, string author)
{
	Id = id;
	Title = title;
	Author = author;
	CheckedOut = false;
}
