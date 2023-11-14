# references: https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/
import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
import argparse
import imutils
import cv2
import re
from imutils.perspective import four_point_transform
import sys



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="name of the input receipt image. Image should be located in Receipts folder.")
ap.add_argument("-d", "--debug", type=int, default=-1,
	help="whether or not we are visualizing each step of the pipeline")
args = vars(ap.parse_args())

# load the input image from disk
receipt_folder = "C:/Users/moono/OneDrive/Desktop/My_Stuff/Projects/Projects/Saving_Sergeant/Receipts/"
orig = cv2.imread(receipt_folder + args["image"])

# do some image processing so that the OCR can be more accurate
receipt = cv2.cvtColor(orig,cv2.COLOR_BGR2GRAY)
# show transformed image
cv2.imshow("Receipt Transform", imutils.resize(receipt, width=500))
cv2.waitKey(0)

# apply OCR to the receipt image by assuming column data, ensuring
# the text is *concatenated across the row* (additionally, for your
# own images you may need to apply additional processing to cleanup
# the image, including resizing, thresholding, etc.)
options = "--psm 4"
text = pytesseract.image_to_string(
	cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
	config=options)
# show the raw output of the OCR process
print("[INFO] raw output:")
print("==================")
print(text)
print("\n")