# references: https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/
# https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html

import pytesseract
pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
import argparse
import imutils
import cv2
import re
import sys
import subprocess
import copy

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="name of the input receipt image. Image should be located in Receipts folder.")
ap.add_argument("-d", "--debug", type=int, default=-1,
	help="whether or not we are visualizing each step of the pipeline")
args = vars(ap.parse_args())

# get image path and add a border to image (tesseract works better with bordered images)
receipt_folder = "C:/Users/moono/OneDrive/Desktop/My_Stuff/Projects/Projects/Saving_Sergeant/Receipts/"
image_path = receipt_folder + args["image"]
cmd = ["magick", "convert", image_path, "-bordercolor", "Black", "-border", "10x10", image_path + "_border.jpg"]
subprocess.run(cmd)
image_path = image_path + "_border.jpg"

# load the input image from disk
receipt = cv2.imread(image_path)

# do some image processing so that the OCR can be more accurate
#first, let's make the image grayscale
receipt = cv2.cvtColor(receipt,cv2.COLOR_BGR2GRAY)
#then make it binary: only black and white, no gray
_, receipt = cv2.threshold(receipt,0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#receipt_adaptive = cv2.adaptiveThreshold(receipt,255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, 2) 




# show transformed image (if in debug mode)
if args["debug"]:
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

#data to be determined by the vendor
transactions = [] #list used to hold all purchases/transactions
t = {
	"vendor" : None,
	"whose_transaction" : "Chase Nairn-Howard",
	"category" : None,
	"transaction_date" : None,
	"location" : None,
	"item_key" : None,
	"quantity" : None,
	"dollars" : None
}

if "The Book Bin" in text:
	#fill in some blanks about our transactions
	t["vendor"] = "The Book Bin"
	t["category"] = "Entertainment"
	t["location"] = "Corvallis"

	lines = text.split("\n")
	for l in range(0, len(lines)):
		#use RE to find transaction items in the text
		re_str = re.search("[0-9]+@ [0-9]+\.[0-9][0-9]", lines[l])
		#take transaction items and format it, then place into transactions[]
		if re_str:
			new_transaction = copy.deepcopy(t)
			#left side will be the quantity, right side *individual* item cost
			qc = re_str.group().split("@ ")
			new_transaction["quantity"] = int(qc[0])
			new_transaction["dollars"] = float(qc[0]) * float(qc[1])
			#The following line (or line after) will contain the item name (ie item_key)
			if re.search("[A-Z,a-z]+", lines[l+1]):
				new_transaction["item_key"] = lines[l+1]
			else:
				new_transaction["item_key"] = lines[l+2]
			transactions.append(new_transaction)

print(transactions)


			

	