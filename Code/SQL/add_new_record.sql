-- Adds new records into the database, specifically
-- by adding them to the "Transactions" table
SET @v_name = "Rifes", -- name of the product's vendor
@b_name = NULL, -- name of the brand of the product
@p_name = "Chase Nairn-Howard", -- name of the person making the purchase
@c_name = "Furnishing", -- name of the category of the purchased product
@t_date = "2023-09-10", -- date of when item was purchase in YYYY-MM-DD format
@l_name = "Eugene", -- location where the transaction took place 
@q = 1, -- number of purchased items (default is 1)
@d = 351.49, -- price of the item (single) in US $
@purchased_item_name = "Coffee Table", -- name of the purchased item
@notes = NULL;


INSERT INTO transactions VALUES
( (SELECT vendor_id FROM vendors WHERE vendor_name=@v_name),
  (SELECT brand_id FROM brands WHERE brand_name=@b_name),
  (SELECT person_id FROM people WHERE person_name=@p_name),
  (SELECT category_id FROM categories WHERE category_name=@c_name),
  @t_date,
  (SELECT location_id FROM locations WHERE location_name=@l_name),
  @d,
  @purchased_item_name,
  @notes,
  @q
);

SELECT * FROM transactions;