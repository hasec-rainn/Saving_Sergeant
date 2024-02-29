# Overview
The intent of saving sergeant is to take images of receipts, scan them, store them in an SQL database, and then perform statistical analysis to provide insights into the user's spending habits.

# The Need
At first glance, Saving Sergeant appears to mimic the services such as Rocket Money or the built-in spending analysis your bank provides. These services analyze *whole transactions* and provide insights.

This is contrasted with Saving Sergeant, which analyzes whole transactions *and the individual items that compose each transaction*. Thus, Saving Sergeant can provide more (detailed) insights than alternative services.

A good example of this difference is grocery shopping. Rocket Money and your bank can show you how much money you spent on groceries over the last 6 months; it can't, however, tell you which items were contributing the most to your grocery cost over this time period. It also can't compare the price of the same item from different stores. Nor can it show you the cost you spent on individual items.

# Running the Program
Some dependancies are needed to run this program. ImageMagik and Google's tesseract should be installed and accessable in your enviornment variables. Additionally, a database system such as MySQL is also necessary for running the SQL scripts and storing receipt data.

The command line syntax for the program is `py scanner -i IMAGE_PATH [-d DEBUG_VALUE]`. 
`IMAGE_PATH` is the name (including the file type) of the receipt contained within the `Receipt/` directory you want to scan. 

`DEBUG_VALUE` can either be 0 or 1. 
If 0, the program will run in normal mode, producing a csv output of the scanned receipt.
If 1, the program will run in debug mode. Everything done in normal mode will be done in addition to the following: the results of image preprocessing will be shown; bounding boxes where tesseract detected text in the image will be shown; a file `out.txt` will be created to show the exact text tesseract detected; the preprocess image will not be deleted after the program completes (this image will have a `_border` at the end of its file name). 

# Tasks 

| Task Name | Target Completion Date | Completion Date | Hours Invested |
| -- | -- | -- | -- | -- |
| [[Data Format]] | 11/13/2023 | 11/8/2023 | 11
| [[Scanner Research]] | 11/20/2023 | 11/15/2023  | 6.5
| [[Scanner Implementation]] | 11/27/2023 | | 0 |
| [[Data Storage]] | 12/4/2023 |  | 0 |
