
-- project 1...internship
 --Sare columns
SELECT * FROM ['Amazon Data$'];

-- Sirf kuch columns
SELECT product_name, actual_price, discounted_price, rating 
FROM ['Amazon Data$'];

-- Top 10 rows
SELECT TOP 10 product_name, rating, actual_price 
FROM ['Amazon Data$'];

     --WHERE COMMAND
-- 4 se upar rating wale products
SELECT product_name, rating 
FROM ['Amazon Data$'] 
WHERE TRY_CAST(rating AS FLOAT) > 4;

-- 50% se zyada discount wale
SELECT product_name, discount_percentage 
FROM ['Amazon Data$'] 
WHERE TRY_CAST(discount_percentage AS FLOAT) > 50;

-- Price range filter
SELECT product_name, actual_price 
FROM ['Amazon Data$'] 
WHERE TRY_CAST(actual_price AS FLOAT) BETWEEN 500 AND 2000;

  --GROUP BY
-- Sab se zyada rated products pehle
SELECT product_name, rating 
FROM ['Amazon Data$'] 
ORDER BY rating DESC;

-- Sab se sasta product pehle
SELECT product_name, discounted_price 
FROM ['Amazon Data$'] 
ORDER BY discounted_price ASC;

-- Sab se zyada discount
SELECT product_name, discount_percentage 
FROM ['Amazon Data$'] 
ORDER BY discount_percentage DESC;
  --GROUP BY
-- Har category mein kitne products hain
SELECT category, COUNT(*) AS total_products 
FROM ['Amazon Data$'] 
GROUP BY category;

-- Har category ki average rating
SELECT category, AVG(TRY_CAST(rating AS FLOAT)) AS avg_rating 
FROM ['Amazon Data$'] 
GROUP BY category 
ORDER BY avg_rating DESC;

-- Har category ka average discount
SELECT category, AVG(TRY_CAST(discount_percentage AS FLOAT)) AS avg_discount 
FROM ['Amazon Data$'] 
GROUP BY category 
ORDER BY avg_discount DESC;

-- Sirf woh categories jahan average rating 4 se upar ho
SELECT category, AVG(rating) AS avg_rating 
FROM amazon_clean
GROUP BY category 
HAVING AVG(rating) > 4;

-- Sirf woh categories jahan 50 se zyada products hon
SELECT category, COUNT(*) AS total_products 
FROM amazon_clean
GROUP BY category 
HAVING COUNT(*) > 50;

-- Top 10 sab se zyada reviewed products
SELECT TOP 10 product_name, rating_count 
FROM amazon_clean
ORDER BY rating_count DESC;

-- Top 5 best value products (zyada discount + zyada rating)
SELECT TOP 5 product_name, rating, discount_percentage 
FROM amazon_clean
WHERE rating > 4 AND discount_percentage > 50 
ORDER BY discount_percentage DESC;

-- Sab se mehenga product har category mein
SELECT category, MAX(actual_price) AS max_price 
FROM amazon_clean
GROUP BY category 
ORDER BY max_price DESC;



-- extra commands
-- Duplicate product_ids dekhna
SELECT product_id, COUNT(*) AS count 
FROM amazon_clean
GROUP BY product_id 
HAVING COUNT(*) > 1;

-- NULL values check karna
SELECT * FROM amazon_clean
WHERE rating_count IS NULL;

-- Unique categories dekhna
SELECT DISTINCT category 
FROM amazon_clean;

-- Total aur average prices
SELECT 
    COUNT(*) AS total_products,
    AVG(actual_price) AS avg_price,
    MAX(actual_price) AS max_price,
    MIN(actual_price) AS min_price
FROM amazon_clean;


-- Purani table delete karo
DROP TABLE category_info;

-- Nayi table banao
CREATE TABLE category_info (
    category_name VARCHAR(200),
    department    VARCHAR(100)
);

-- Data insert karo
INSERT INTO category_info VALUES 
('Electronics', 'Tech'),
('Computers&Accessories', 'Tech'),
('Home&Kitchen', 'Lifestyle');

-- JOIN query
SELECT a.product_name, a.rating, c.department
FROM amazon_clean a
JOIN category_info c 
ON a.category = c.category_name;



