# references: https://pyimagesearch.com/2021/10/27/automatically-ocring-receipts-and-scans/
# https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html

import pytesseract
options = r'--tessdata-dir "C:\Program Files\Tesseract-OCR\tessdata_best"'
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

# create and use new image with a border (tesseract works better with bordered images)
receipt_folder = "C:/Users/moono/OneDrive/Desktop/My_Stuff/Projects/Projects/Saving_Sergeant/Receipts/"
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

#resize the image for better accuracy
#cv2.INTER_AREA is used since we are downsizing
new_width = int(receipt.shape[1] * 0.5) #typecast as int to floor
receipt = imutils.resize(receipt, width=new_width, inter=cv2.INTER_AREA)
cv2.imwrite(image_path,receipt)


# show transformed image (if in debug mode)
if args["debug"]:
	debug_receipt = receipt.copy()
	cv2.imshow("Receipt Transform", imutils.resize(debug_receipt, width=500))
	image_data = pytesseract.image_to_data(debug_receipt, output_type=pytesseract.Output.DICT)
	cv2.waitKey(0)

	#draw and display bounding boxes
	n_boxes = len(image_data['level'])
	for b in range(n_boxes):
		(x, y, w, h) = (image_data['left'][b], image_data['top'][b], image_data['width'][b], image_data['height'][b])
		cv2.rectangle(debug_receipt, (x,y), (x+w,y+h), (150,0,150), 5)
	cv2.imshow("Receipt BB", imutils.resize(debug_receipt, width=500))
	cv2.waitKey(0)

# apply OCR to the receipt image by assuming column data
options += " " + "--psm 4"
options += " " + "-c tessedit_char_whitelist= @0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
text = pytesseract.image_to_string(
	cv2.cvtColor(receipt, cv2.COLOR_BGR2RGB),
	config=options)
# show the raw output of the OCR process
print("[INFO] raw output:")
print("==================")
with open("out.txt", "w") as f:
	f.write(text)
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
	t["transaction_date"] = re.search("((January)|(Febuary)|(March)|(April)|(May)|(June)|(July)|(August)|(September)|(October)|(November)|(December)) [1-3][0-9] [0-9]{4}", text)
	if t["transaction_date"]:
		#if a date was found, then format it as string
		t["transaction_date"] = t["transaction_date"].group()

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


if "WinCo" in text or "Winco" in text:
	#fill in some blanks about our transactions
	t["vendor"] = "WinCo Foods"
	t["category"] = "Groceries"
	t["location"] = "Eugene"
	t["transaction_date"] = re.search("[0-9]{1,2}/[0-9]{1,2}/[0-9]{2}", text)
	if t["transaction_date"]:
		#if a date was found, then format it
		t["transaction_date"] = t["transaction_date"].group()

	lines = text.split("\n")
	for l in range(0, len(lines)):
		#use RE to find transaction items in the text
		re_str = re.search("[A-Z]+", lines[l])
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


#create new csv file from transactions and place in Data folder with unique name
csv_path = "Data/" + t["whose_transaction"].replace(" ","_") \
	+ "_" + t["vendor"].replace(" ","_") \
	+ "_" + t["transaction_date"].replace(" ","_") + ".csv"
with open(csv_path,"w") as output_csv:
	for item in transactions:
		output_csv.write(item["vendor"] + ",")
		output_csv.write(item["whose_transaction"] + ",")
		output_csv.write(item["category"] + ",")
		output_csv.write(item["transaction_date"] + ",")
		output_csv.write(item["location"] + ",")
		output_csv.write(item["item_key"] + ",")
		output_csv.write(str(item["quantity"]) + ",")
		output_csv.write(str(item["dollars"]) + "\n")

print(transactions)