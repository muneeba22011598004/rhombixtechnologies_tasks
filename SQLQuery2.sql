USE amazonedb;

CREATE TABLE amazon_products (
    product_id          VARCHAR(20),
    product_name        VARCHAR(500),
    category            VARCHAR(200),
    discounted_price    DECIMAL(10,2),
    actual_price        DECIMAL(10,2),
    discount_percentage DECIMAL(5,2),
    rating              DECIMAL(3,1),
    rating_count        INT NULL,       -- NULL allowed (2 empty values hain)
    about_product       VARCHAR(MAX),
    user_id             VARCHAR(100),
    user_name           VARCHAR(200),
    review_id           VARCHAR(100),
    review_title        VARCHAR(500),
    review_content      VARCHAR(MAX),   -- 18,547 chars tak hai
    img_link            VARCHAR(200),
    product_link        VARCHAR(300)
);