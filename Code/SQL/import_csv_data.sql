-- Takes formatted data from a csv file and imports it into the database
-- in the "Transactions" table
SELECT * FROM vendors;

-- SHOW VARIABLES LIKE "secure_file_priv";
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.1/Uploads/financial_data.csv'
INTO TABLE transactions
FIELDS TERMINATED BY ',' ENCLOSED BY '' ESCAPED BY '\\'
LINES TERMINATED BY '\n' STARTING BY '';

SELECT * 
FROM transactions;