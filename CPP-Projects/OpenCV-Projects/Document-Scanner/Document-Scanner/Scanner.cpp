// Include necessary libraries
#include "stdafx.h"
#include <direct.h>
#include <iostream>
#include <opencv2/imgproc.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>


// Declare the namespaces to be used
using namespace cv;
using namespace std;


// Define the global variables
Mat img, imgCrop;
Mat imgThresh, finalImage;
vector<Point> bigContour;
float imgWidth = 480.0;
float imgHeight = 640.0;


// Define the pre-processing function
Mat preProcessing(Mat img)
{
	Mat imgGray, imgCanny, imgDilate, imgErode;
	resize(img, img, Size(imgWidth, imgHeight));
	cvtColor(img, imgGray, COLOR_BGR2GRAY);
	Canny(imgGray, imgCanny, 200, 200);
	Mat kernel = getStructuringElement(MORPH_RECT, Size(3, 3));
	dilate(imgCanny, imgDilate, kernel);
	erode(imgDilate, imgErode, kernel);

	return imgErode;
}


// Define the getContours function
vector<Point> getContours(Mat imgThresh, double minArea)
{
	vector<vector<Point>> contours;
	vector<Vec4i> hierarchy;  // Vector with 4 integers inside of it
	vector<Point> biggestContour;
	double areaCtr;
	double perimeter;
	int maxArea = 0;

	findContours(imgThresh, contours, hierarchy, RETR_EXTERNAL, CHAIN_APPROX_NONE);

	vector<vector<Point>> approx(contours.size());
	vector<Rect> boundRect(contours.size());

	for (int ii=0; ii < contours.size(); ii++)
	{
		areaCtr = contourArea(contours[ii]);
		if (areaCtr >= minArea)
		{
			perimeter = arcLength(contours[ii], true);
			approxPolyDP(contours[ii], approx[ii], 0.02*perimeter, true);

			if (areaCtr > maxArea && approx[ii].size() == 4)
			{
				biggestContour = { approx[ii][0], approx[ii][1], approx[ii][2], approx[ii][3] };
				maxArea = areaCtr;
			}
			drawContours(img, approx, ii, Scalar(255, 0, 255), 3);
		}
	}
	

	return biggestContour;
}


// Define a funcion to re-arrange the points in the contour
vector<Point> reShape(vector<Point> contour)
{
	vector<Point> newPoints;
	vector <int> sumPoint, subPoint;	

	for (int jj = 0; jj < contour.size(); jj++)
	{
		sumPoint.push_back(contour[jj].x + contour[jj].y);
		subPoint.push_back(contour[jj].x - contour[jj].y);
	}

	Point firstPoint = contour[min_element(sumPoint.begin(), sumPoint.end()) - sumPoint.begin()];  // top-left corner (0)
	Point fourthPoint = contour[max_element(sumPoint.begin(), sumPoint.end()) - sumPoint.begin()]; // bottom-right corner (3)

	Point secondPoint = contour[max_element(subPoint.begin(), subPoint.end()) - subPoint.begin()]; // top-right corner (1)
	Point thirdPoint = contour[min_element(subPoint.begin(), subPoint.end()) - subPoint.begin()];  // bottom-left corner (2)

	newPoints.push_back(firstPoint);
	newPoints.push_back(secondPoint);
	newPoints.push_back(thirdPoint);
	newPoints.push_back(fourthPoint);

	return newPoints;
}


// Define the warp correction function
Mat warpCorrection(Mat img, vector<Point> contour)
{
	Mat imgWarp;
	//Obtain the reshaped points
	vector<Point> cornerPoints = reShape(contour);
	
	// Define the source and destination points for warping
	Point2f pts1[4] = { cornerPoints[0], cornerPoints[1], cornerPoints[2], cornerPoints[3] };
	Point2f pts2[4] = { {0.0f, 0.0f}, {imgWidth, 0.0f}, {0.0f, imgHeight}, {imgWidth, imgHeight} };
	Mat matrix = getPerspectiveTransform(pts1, pts2);

	// Get the corrected image
	warpPerspective(img, imgWarp, matrix, Point(imgWidth, imgHeight));

	return imgWarp;
}


// Define the main function
int main()
{
	VideoCapture vcap(0);
	
	string url = "http://192.168.0.101:8080/shot.jpg"; // url for accessing the video feed from the phone using IP-Webcam

	int count = 1;
	while (true)
	{
		if (vcap.open(url))
			vcap.read(img);
		else
			cout << "Cannot open camera" << endl;		

		// Pre-processing of the image
		imgThresh = preProcessing(img);

		// Detect and draw the contour		
		bigContour = getContours(imgThresh, 1000);

		// Perform Warp correction on the image
		Mat finalImage = warpCorrection(img, bigContour);

		// Crop the image
		Rect roi = Rect(10, 10, imgWidth - (2 * 10), imgHeight - (2 * 10));
		imgCrop = finalImage(roi);

		// Display the results
		imshow("Result", imgCrop);
		imshow("Original", img);

		// Save the image
		if (waitKey(1) == 's')
		{			
			rectangle(img, Point(0, 190), Point(480, 390), Scalar(255, 0, 255), FILLED);
			putText(img, "Saved image", Point(100, 300), FONT_HERSHEY_COMPLEX, 0.7, Scalar(0, 0, 0), 2);			
			if (_mkdir("results") == 0)
				imwrite("results\\Scrshot_" + to_string(count) + ".jpg", imgCrop);
			else
				cout << "File creation failed";
			imshow("Original", img);
			waitKey(500);
			count += 1;
		}

		else if (waitKey(1) == 27)
			break;
	}

}