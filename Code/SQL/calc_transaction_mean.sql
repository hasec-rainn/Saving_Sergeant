-- Together, these two things should specify items that are a
-- part of a single transaction
SET @d = '2023-10-21'; -- Desired transaction date
SET @v = 14; -- Vendor of the transaction


SELECT ROUND(SUM(quantity * dollars) / SUM(quantity),2) as "Average Price ($)"
FROM transactions
WHERE transaction_date = @d
AND vendor = @v;