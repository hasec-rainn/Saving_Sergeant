# Data Format
The consideration of how to format, and store in the database, the data garnered from receipts. This should be one of the first undertaking of the project, as the scanner needs to know how to format the data it gets from the receipt into the csv.

# Planned Format

### Transactions Table

| Field Name | Foreign Key | Attributes | Description | 
| -- | -- | -- | -- | 
| vendor | FK to vendors table. | INT UNSIGNED NOT NULL | The entity (store, person, or employer) whom sold the item. |
| whose_transaction | FK to people table. | INT UNSIGNED NOT NULL | the person whom interacted with the vendor to receive the purchased item. |
| category | FK to Category table. | INT UNSIGNED NOT NULL | The over-arching category the purchased item belongs to. |
| transaction_date | None | DATE NOT NULL | The date upon which the transaction took place. |
| location | FK to locations. | INT UNSIGNED NULL | The location the transaction took place, specifically in regards to the vendor. |
| item_key | FK to items. | VARCHAR(45) NOT NULL | The name of the item, as specified on the receipt. User friendly name in items table. |
| quantity | None. | INT UNSIGNED NOT NULL DEFAULT 1 | The quantity of `item_key` purchased in the transaction |
| dollars | None. | FLOAT NOT NULL | The total cost of transaction: `total = quantity * cost_per_item` |
