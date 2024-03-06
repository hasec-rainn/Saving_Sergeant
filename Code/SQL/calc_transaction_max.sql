-- Together, these two things should specify items that are a
-- part of a single transaction
SET @d = '2023-10-21'; -- Desired transaction date
SET @v = 14; -- Vendor of the transaction

-- Find the most expensive item in the transaction
SELECT ROUND(MAX(dollars),2) as "Most expensive Item"
FROM transactions
WHERE transaction_date = @d
AND vendor = @v;