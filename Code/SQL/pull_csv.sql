SET GLOBAL local_infile = 1; -- Must be enabled to pull locally (ie, to pull data from client)
SET SQL_SAFE_UPDATES = 0; -- Must be disabled to enable table UPDATEs that don't use PK in WHERE clause

DROP TABLE IF EXISTS temp_tbl;
CREATE TABLE temp_tbl (
	temp_vendor VARCHAR(45),
    temp_brand VARCHAR(45),
    temp_whose_transaction VARCHAR(45),
    temp_category VARCHAR(45),
    temp_transaction_date DATE NOT NULL,
    temp_location VARCHAR(45),
	
    temp_quantity INT UNSIGNED NOT NULL DEFAULT 1,
    temp_dollars FLOAT NOT NULL, -- per item cost
    temp_item_name VARCHAR(45),
    
    PRIMARY KEY (temp_item_name)
);

-- Copy everything into a temporary table.
-- We will compress the strings into their corresponding keys further below.
LOAD DATA LOCAL INFILE 'C:/Users/moono/OneDrive/Desktop/My_Stuff/Projects/Projects/Saving_Sergeant/Data/Chase_Nairn-Howard_The_Book_Bin_2023-10-21.csv'
INTO TABLE temp_tbl
COLUMNS TERMINATED BY ','
LINES TERMINATED BY '\n';

-- compress vendors and turn '' into NULL
UPDATE temp_tbl, vendors
SET temp_vendor = vendors.vendor_id
WHERE temp_vendor = vendors.vendor_name;
UPDATE temp_tbl
SET temp_vendor = NULL
WHERE temp_vendor = '';

-- compress brands and turn '' into NULL
UPDATE temp_tbl, brands
SET temp_brand = brands.brand_id
WHERE temp_brand = brands.brand_name;
UPDATE temp_tbl
SET temp_brand = NULL
WHERE temp_brand = '';

-- compress whose_transaction
UPDATE temp_tbl, people
SET temp_whose_transaction = people.person_id
WHERE temp_whose_transaction = people.person_name;

-- compress categories
UPDATE temp_tbl, categories
SET temp_category = categories.category_id
WHERE temp_category = categories.category_name;

-- compress locations
UPDATE temp_tbl, locations
SET temp_location = locations.location_id
WHERE temp_location = locations.location_name;

-- Alter the field types of this temporary table
-- allowing it to be inserted into the main transactions table
ALTER TABLE temp_tbl MODIFY temp_vendor INT UNSIGNED NULL;
ALTER TABLE temp_tbl MODIFY temp_brand INT UNSIGNED NULL;
ALTER TABLE temp_tbl MODIFY temp_whose_transaction INT UNSIGNED NOT NULL;
ALTER TABLE temp_tbl MODIFY temp_category INT UNSIGNED NOT NULL;
ALTER TABLE temp_tbl MODIFY temp_transaction_date DATE NOT NULL;
ALTER TABLE temp_tbl MODIFY temp_location INT UNSIGNED NULL;

-- Insert into the table
INSERT INTO transactions (vendor,brand,whose_transaction,category,transaction_date,location,quantity,dollars,item_name)
SELECT temp_vendor,temp_brand,temp_whose_transaction,temp_category,temp_transaction_date,temp_location,temp_quantity,temp_dollars,temp_item_name
FROM temp_tbl;

SELECT * FROM transactions;