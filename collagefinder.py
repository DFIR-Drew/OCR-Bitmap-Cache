from pytesseract import Output
import pytesseract
import argparse
import cv2
import os
import csv
import math
import sys

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--total", required=False,help="total number of images in bitmap-cache")
ap.add_argument("-x", "--xcoord", required=False,help="X coordinate of left side of bounding box")
ap.add_argument("-y", "--ycoord", required=False,help="Y coordinate of top side of bounding box")
ap.add_argument("-o", "--output", required=True, help="File to output")
ap.add_argument("-n", "--number", required=False,
	help="image #")
ap.add_argument("-b", "--bitmap", required=True,help="bitmap-cache collage image")
args = vars(ap.parse_args())

if args["number"] != None and args["total"] != None:
	onumber = int(args["number"]) + 1
	inumber = int(args["total"]) - int(args["number"])
	row = math.floor(inumber / 64) + 1
	col = 64 - onumber % 64
	x = col * 64
	y = row * 64
	w = 64
	h = 64
	print(inumber)
	print(row)
	print(col)
	print(x)
	print(y)

	image = cv2.imread(args["bitmap"])

	cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
	cv2.imwrite(args["output"], image)
elif args["xcoord"] != None and args["ycoord"] != None:
	image = cv2.imread(args["bitmap"])
	x = int(args["xcoord"])
	y = int(args["ycoord"])
	cv2.rectangle(image, (x,y), (x + 64, y + 64), (0,255,0), 2)
	cv2.imwrite(args["output"], image)

else:
	print("Please specify either the coordinates of the box or the image number of the box...quitting")
	sys.exit(0)