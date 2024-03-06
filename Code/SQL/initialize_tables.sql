-- Creates the main data storing table, `transactions`, in addition
-- to all the other tables which support it.
-- **All tables will be(come) void of data upon executing this file.

-- Avoid error of trying to create an already-existing table
DROP TABLE IF EXISTS transactions;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS vendors;
DROP TABLE IF EXISTS brands;
DROP TABLE IF EXISTS people;
DROP TABLE IF EXISTS locations;

CREATE TABLE categories (
	category_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (category_id)
);


CREATE TABLE vendors (
	vendor_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    vendor_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (vendor_id)
);


CREATE TABLE brands (
	brand_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    brand_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (brand_id)
);


CREATE TABLE people (
	person_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    person_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (person_id)
);

CREATE TABLE locations (
	location_id INT UNSIGNED NOT NULL AUTO_INCREMENT,
    location_name VARCHAR(45) NOT NULL UNIQUE,
    PRIMARY KEY (location_id)
);

--
CREATE TABLE transactions (
    vendor INT UNSIGNED NULL,
    brand INT UNSIGNED NULL,
    whose_transaction INT UNSIGNED NOT NULL,
    category INT UNSIGNED NOT NULL,
    transaction_date DATE NOT NULL,
    location INT UNSIGNED NULL,
	
    quantity INT UNSIGNED NOT NULL DEFAULT 1,
    dollars FLOAT NOT NULL, -- per item cost
    item_name VARCHAR(45) NOT NULL,
    
    PRIMARY KEY transaction_id(transaction_date, whose_transaction, dollars, category, item_name),
    FOREIGN KEY (vendor) REFERENCES vendors(vendor_id),
    FOREIGN KEY (brand) REFERENCES brands(brand_id),
    FOREIGN KEY (whose_transaction) REFERENCES people(person_id),
    FOREIGN KEY (category) REFERENCES categories(category_id),
    FOREIGN KEY (location) REFERENCES locations(location_id)
);

describe transactions;
SELECT * FROM transactions;