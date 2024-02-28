"""
This program 

references: 
https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/
https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html
https://stackoverflow.com/questions/31633403/tesseract-receipt-scanning-advice-needed
https://stackoverflow.com/questions/9480013/image-processing-to-improve-tesseract-ocr-accuracy
"""

import pytesseract
options = r'--tessdata-dir ' + r'"C:\Program Files\Tesseract-OCR\tessdata_best"'
import argparse
import imutils
import cv2
import re
import numpy as np
import subprocess
import copy
import time
import os

#set up the correct directories
cwd = os.getcwd().replace("\\","/")
sys_root = cwd.split("/")[0] + "/"
receipt_folder = cwd + "/" + "Receipts/"
ocr_debug_output = cwd + "/"
csv_data_folder = cwd + "/" + "Data/"


# tess_dir = None
# for root, dirs, _ in os.walk(cwd):
# 	print(root)
# 	time.sleep(0.25)
# 	if "Tesseract-OCR" in dirs:
# 		tess_dir = os.path.join(root, "Tesseract-OCR").replace("\\", "/")
# 		break

# use BFS to find tesseract dir since most users will likely keep it
# in Program Files/ or bin/ (thus shallow BFS will find faster)
# BFS Derived from Watty from
# https://stackoverflow.com/questions/49654234/is-there-a-breadth-first-search-option-available-in-os-walk-or-equivalent-py
tess_dir = None
dirs = [sys_root]
# while we have dirs to scan
while len(dirs) :
	nextDirs = []
	for parent in dirs:
		# attempt to get all the subdirectories in the parent
		subdirs = None
		try:
			subdirs = os.listdir(parent)
		except PermissionError: #skip this dir: don't have read permissions
			subdirs = []
		
		#go through each subdir
		for f in subdirs:
			af = os.path.join(parent, f)
			print(af)
			# if we found the dir, break the loop
			if f == "C:/" and  os.path.isdir(af):
				tess_dir = af
				dirs=[]
				break
			else: #otherwise, if its a directory, add it to the next level we search
				if os.path.isdir(af) :
					nextDirs.append(af)
	# once we've done all the current dirs then
	# we set up the next itter as the child dirs 
	# from the current itter.
	dirs = nextDirs

print(tess_dir)
#who_purchased = input("Enter the full name of who made this transaction: ")



exit(0)

#Optimally resize `img` according to the bounding boxes specified in `boxes` (which is simply the (pruned) results from `pytesseract.image_to_data()`).
#Tesseract performs optimally when capital letters are between [30,33]px tall (https://groups.google.com/g/tesseract-ocr/c/Wdh_JJwnw94/m/24JHDYQbBQAJ).
# function by rinogo, made available under MIT liscense: https://gist.github.com/rinogo/294e723ac9e53c23d131e5852312dfe8
def optimal_resize(img, boxes):
	median_height = np.median(boxes["height"])
	print("median height is:", median_height)
	target_height = 32 #See https://groups.google.com/g/tesseract-ocr/c/Wdh_JJwnw94/m/24JHDYQbBQAJ
	scale_factor = target_height / median_height
	print("Scale factor: " + str(scale_factor))

	#If the image is already within `skip_percentage` percent of the target size, just return the original image (it's better to skip resizing if we can)
	skip_percentage = 0.07
	if(scale_factor > 1 - skip_percentage and scale_factor < 1 + skip_percentage):
		return img

	#Bicubic for enlarging, "pixel area relation" for reduction. (See https://chadrick-kwag.net/cv2-resize-interpolation-methods/)
	if(scale_factor > 1.0):
		interpolation = cv2.INTER_CUBIC
	else:
		interpolation = cv2.INTER_AREA

	return cv2.resize(img, None, fx = scale_factor, fy = scale_factor, interpolation = interpolation)



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="name of the input receipt image. Image should be located in Receipts folder.")
ap.add_argument("-d", "--debug", type=int, default=-1,
	help="whether or not we are visualizing each step of the pipeline")
args = vars(ap.parse_args())

# create and use new image with a border (tesseract works better with bordered images)
image_path = receipt_folder + args["image"]
cmd = ["magick", "convert", image_path, "-bordercolor", "Black", "-border", "30x30", image_path + "_border.jpg"]
subprocess.run(cmd)
image_path = image_path + "_border.jpg"

# load the input image from disk
receipt = cv2.imread(image_path)

# do some image processing so that the OCR can be more accurate
#first, let's make the image grayscale
receipt = cv2.cvtColor(receipt,cv2.COLOR_BGR2GRAY)

#then make it binary: only black and white, no gray
_, receipt = cv2.threshold(receipt,0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)

#dynamically resize the image so characters are 32pt tall
#see
boxes = pytesseract.image_to_data(receipt, output_type=pytesseract.Output.DICT)
receipt = optimal_resize(receipt, boxes)
cv2.imwrite(image_path,receipt)

# show transformed image and bounding boxes (if in debug mode)
if args["debug"]:
	debug_receipt = receipt.copy()
	cv2.imshow("Receipt Transform", imutils.resize(debug_receipt, width=500))
	cv2.waitKey(0)

	#draw and display bounding boxes
	image_data = pytesseract.image_to_data(debug_receipt, output_type=pytesseract.Output.DICT)
	n_boxes = len(image_data['level'])
	for b in range(n_boxes):
		(x, y, w, h) = (image_data['left'][b], image_data['top'][b], image_data['width'][b], image_data['height'][b])
		cv2.rectangle(debug_receipt, (x,y), (x+w,y+h), (150,0,150), 5)
	cv2.imshow("Receipt BB", imutils.resize(debug_receipt, width=500))
	cv2.waitKey(0)

# apply OCR to the receipt image by assuming column data
options += " " + "--psm 4"
options += " " + "-c tessedit_char_whitelist=' .#$@0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'"
text = pytesseract.image_to_string(
	cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
	config=options
)
# write out the raw output of the OCR process
if args["debug"]:
	with open(ocr_debug_output + "ocr_out.txt", "w") as f:
		f.write(text)


#data to be determined by the vendor
transactions = [] #list used to hold all purchases/transactions
t = {
	"vendor" : None,
	"brand" : None,
	"whose_transaction" : who_purchased,
	"category" : None,
	"transaction_date" : None,
	"location" : None,
	"item_key" : None,
	"quantity" : None,
	"dollars" : None
}


if "The Book Bin" in text:
	#one of the cases where no additional preprocessing is required

	#fill in some blanks about our transactions
	t["vendor"] = "The Book Bin"
	t["brand"] = ''
	t["category"] = "Entertainment"
	t["location"] = "Corvallis"
	t["transaction_date"] = re.search("((January)|(Febuary)|(March)|(April)|(May)|(June)|(July)|(August)|(September)|(October)|(November)|(December)) [1-3][0-9] [0-9]{4}", text)
	#if a date was found, then format it as a SQL-readable string
	if t["transaction_date"]:
		t["transaction_date"] = t["transaction_date"].group() #to make into one string
		t["transaction_date"] =\
			time.strftime("%Y-%m-%d",time.strptime(t["transaction_date"], "%B %d %Y"))

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
			new_transaction["dollars"] = float(qc[0]) * float(qc[1]) #multiply to get total cost
			#The following line (or line after) will contain the item name (ie item_key)
			if re.search("[A-Z,a-z]+", lines[l+1]): #check if following line is empty
				new_transaction["item_key"] = lines[l+1]
			else:
				new_transaction["item_key"] = lines[l+2]

			transactions.append(new_transaction)


if "Dona Mercedes Restaurant" in text:
	#one of the cases where no additional preprocessing is required

	#fill in some blanks about our transactions
	t["vendor"] = "Dona Mercedes Restaurant"
	t["brand"] = ''
	t["category"] = "Eating Out"
	t["location"] = "San Faernando"

	#Dona Mercedes doesn't record transaction date. We'll need to get it from user.
	req ="Using format YYYY-MM-DD, please enter the transaction date of this receipt: "
	t["transaction_date"] = input(req)
	while not re.search("[1-3][0-9][0-9][0-9]-[0-1][0-9]-[0-3][0-9]", t["transaction_date"]):
		t["transaction_date"] = input("Error: date not recognized. " + req)

	lines = text.split("\n")
	for l in range(0, len(lines)):
		#use RE to find transaction items in the text
		re_str = re.search("[0-9]+ ([a-z]|[A-Z]|( ))+ \$[0-9]+\.[0-9][0-9]", lines[l])
		#take transaction items and format it, then place into transactions[]
		if re_str:
			new_transaction = copy.deepcopy(t)
			#leftmost is quantity, middle is item name, and right is summed-cost
			re_str = re_str.group().split(" ")
			new_transaction["quantity"] = int(re_str[0]) #very first item before space is quantity
			#Last item after space is summed cost (we want indv so we divide)
			new_transaction["dollars"] = float( float(re_str[len(re_str)-1].replace("$","")) / new_transaction["quantity"])
			#all the other lines, when taken together, are the name of the item
			re_str.pop(len(re_str)-1); re_str.pop(0)
			new_transaction["item_key"] = ' '.join(re_str)
			

			transactions.append(new_transaction)


if "HP Pho Ga" in text:
	#one of the cases where no additional preprocessing is required

	#fill in some blanks about our transactions
	t["vendor"] = "HP Pho Ga"
	t["brand"] = ''
	t["category"] = "Eating Out"
	t["location"] = "Los Angeles"
	t["transaction_date"] = re.search("((Jan)|(Feb)|(Mar)|(Apr)|(May)|(Jun)|(Jul)|(Aug)|(Sep)|(Oct)|(Nov)|(Dec)) [0-3][0-9] [0-9]{4}", text)
	#if a date was found, then format it as a SQL-readable string
	if t["transaction_date"]:
		t["transaction_date"] = t["transaction_date"].group() #to make into one string
		t["transaction_date"] =\
			time.strftime("%Y-%m-%d",time.strptime(t["transaction_date"], "%b %M %Y"))

	lines = text.split("\n")
	for l in range(0, len(lines)):
		#use RE to find transaction items in the text
		re_str = re.search("[0-9]+ (( )|[a-z]|[A-Z])+ [0-9]+\.[0-9][0-9]", lines[l])
		#take transaction items and format it, then place into transactions[]
		if re_str:
			new_transaction = copy.deepcopy(t)
			#left side will be the quantity, right side *individual* item cost
			re_str = re_str.group().split(" ")
			#very first item before space is quantity
			new_transaction["quantity"] = int(re_str[0])
			#Last item after space is summed cost (we want indv so we divide)
			new_transaction["dollars"] = float( float(re_str[len(re_str)-1]) / new_transaction["quantity"])
			#all the other lines, when taken together, are the name of the item
			re_str.pop(len(re_str)-1); re_str.pop(0)
			new_transaction["item_key"] = ' '.join(re_str)
			

			transactions.append(new_transaction)


#create new csv file from transactions and place in Data folder with unique name
csv_path = csv_data_folder + t["whose_transaction"].replace(" ","_") \
	+ "_" + t["vendor"].replace(" ","_") \
	+ "_" + t["transaction_date"].replace(" ","_") + ".csv"
with open(csv_path,"w") as output_csv:
	for item in transactions:
		output_csv.write(item["vendor"] + ",")
		output_csv.write(item["brand"] + ",")
		output_csv.write(item["whose_transaction"] + ",")
		output_csv.write(item["category"] + ",")
		output_csv.write(item["transaction_date"] + ",")
		output_csv.write(item["location"] + ",")
		output_csv.write(str(item["quantity"]) + ",")
		output_csv.write(str(item["dollars"]) + ",")
		output_csv.write(item["item_key"] + "\n")

#if we're not in debug mode, delete the processed image
if not args["debug"]:
	os.remove(image_path)

print(transactions)