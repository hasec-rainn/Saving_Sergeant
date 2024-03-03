# Overview
This repository acts as a proof-of-concept for a receipt-scanning and receipt-analyzing software whose aim is to provide financial insights into users' spending habits.
This is done by preprocessing images of receipts, scanning them with Tesseract OCR, and storing them in a csv file that can then be read into a SQL database. Analysis is then performed with an SQL database to provide insights into the user's spending habits

# The Need
At first glance, Saving Sergeant appears to mimic services such as Rocket Money or the built-in spending analysis your bank provides. These services analyze *whole transactions* and provide insights.

This is contrasted with Saving Sergeant, which analyzes whole transactions *and the individual items that compose each transaction*. Thus, Saving Sergeant can provide more (detailed) insights than alternative services.

A good example of this difference is grocery shopping. Rocket Money and your bank can show you how much money you spent on groceries over the last 6 months; it can't, however, tell you which items were contributing the most to your grocery cost over this time period. It also can't compare the price of the same item from different stores. Nor can it show you the cost you spent on individual items.

# Running the Program

### Dependencies
Some dependancies are needed to run this program. ImageMagik and Google's tesseract should be installed and accessable in your enviornment variables. Additionally, a database system such as MySQL is also necessary for running the SQL scripts and storing receipt data. You will also need Python 3.xx installed and in your path to execute `scanner.py`.

## Executing scanner.py
The command line syntax for running the scanner portion of the program is `py scanner.py -i IMAGE_PATH [-d DEBUG_VALUE]`.

`IMAGE_PATH` is the name (including the file type) of the receipt contained within the `Receipt/` directory you want to scan. 

`DEBUG_VALUE` can either be 0 or 1. 

If 0, the program will run in normal mode, producing a csv output of the scanned receipt.

If 1, the program will run in debug mode. Everything done in normal mode will be done in addition to the following: the results of image preprocessing will be shown; bounding boxes where tesseract detected text in the image will be shown; a file `out.txt` will be created to show the exact text tesseract detected; the preprocess image will not be deleted after the program completes (this image will have `_border` at the end of its file name).

### SQL Setup
To set up the SQL portion of the program, download MySQl (or another database system), set up a server, and create a database. Run `initialize_tables.sql` to create primary table, `transactions`, and all of its dependency tables.

Next, add the following to `populate_dependency_tables.sql`: `INSERT INTO people VALUES (DEFAULT, <prompted_name>);`, where `<prompted_name>` is the name you entered when prompted by `scanner.py`. This allows the database to recognize the purchaser and accept the csv.

### SQL for Data Analysis
To get the csv file into the database, change the path in the `LOAD DATA LOCAL INFILE` statement in `pull_csv.sql` to match the path of your csv. Then, execute `pull_csv.sql`.

Statements begining with the prefix `calc_` can be used to analyze data in the database. The variable `@d` represents the date of a transaction, and the variable `@v` represents the vendor of a transaction. In conjuction, `@d` and `@v` can pinpoint any particular transaction, and they can be set in each of the `calc_` scripts in order to select a specific transaction to analyze.