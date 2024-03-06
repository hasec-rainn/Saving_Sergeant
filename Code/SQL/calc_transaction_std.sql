-- Together, these two things should specify items that are a
-- part of a single transaction
SET @d = '2023-10-21'; -- Desired transaction date
SET @v = 14; -- Vendor of the transaction

-- Calculates the standard deviation of prices for a particular transaction
SELECT ROUND(STD(dollars),2) as "Standard Deviation of Price ($)"
FROM transactions
WHERE transaction_date = @d
AND vendor = @v;