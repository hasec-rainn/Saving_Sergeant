-- Together, these two things should specify items that are a
-- part of a single transaction
SET @d = '2023-10-21'; -- Desired transaction date
SET @v = 14; -- Vendor of the transaction

-- Finds the cheapest item in the transaction
SELECT ROUND(MIN(dollars),2) as "Cheapest Item"
FROM transactions
WHERE transaction_date = @d
AND vendor = @v;