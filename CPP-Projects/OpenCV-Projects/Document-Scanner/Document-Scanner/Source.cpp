#include "stdafx.h"
#include <iostream>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>


using namespace cv;
using namespace std;


int main()
{
	Mat img;
	imread("doc_scanner_cropped.jpg");
	imshow("Original", img);



}