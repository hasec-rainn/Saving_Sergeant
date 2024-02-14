SELECT vendor, brand, whose_transaction, category, transaction_date, location, 
quantity, dollars, item_name, comments
FROM transactions
INTO OUTFILE 'C:\ProgramData\MySQL\MySQL Server 8.1\Uploads\backup1.csv'
FIELDS TERMINATED BY ','
LINES TERMINATED BY '\n';

SHOW VARIABLES LIKE "secure_file_priv";