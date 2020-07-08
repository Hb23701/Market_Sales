CREATE_PRODUCT_TABLE = "CREATE TABLE IF NOT EXISTS products (id serial PRIMARY KEY, item_name varchar, price decimal);"
CREATE_CUSTOMER_TABLE = "CREATE TABLE IF NOT EXISTS customers (id serial PRIMARY KEY, name varchar);"
CREATE_TRANSACTION_TABLE = """CREATE TABLE IF NOT EXISTS transactions(
        id serial PRIMARY KEY,
        date date,
        total_price decimal,
        transaction_ref varchar,
        transaction_type varchar,
        customer_id integer references customers(id)
    );"""
CREATE_TRANSACTION_DETAIL_TABLE = """CREATE TABLE transaction_details (
        id serial primary key, 
        date date,
        transaction_type varchar,
        product_id integer references products(id),
        transaction_id integer references transactions(id)
    );"""
INSERT_INTO_PRODUCT = "INSERT INTO products (id, item_name, price) VALUES ({})"
INSERT_INTO_CUSTOMER = "INSERT INTO customers VALUES ({})"
INSERT_INTO_CUSTOMER_NULL_ID = "INSERT INTO customers (name) VALUES ({})"
INSERT_INTO_TRANSACTION = "INSERT INTO transactions (transaction_ref, date, transaction_type, customer_id) VALUES ({})"
INSERT_INTO_TRANSACTION_NULL_ID = "INSERT INTO transactions (transaction_ref, date, transaction_type) VALUES ({})"
INSERT_INTO_TRANSACTION_DETAIL = "INSERT INTO transaction_details (transaction_id, date, transaction_type, product_id) VALUES ({})"

CREATE_TOP_TEN_REFUNDED_ITEMS_VIEW = """
create view RefundedItem as select product_id, count(*) from transaction_details 
where transaction_type = 'Refund'
and date <= '{}' and date >= '{}'  group by product_id order by count desc limit 10;
"""
CREATE_MONTHLY_SALE_VIEW = """
create view RefundedItem as select product_id, count(*) from transaction_details 
where transaction_type = 'Refund'
and date <= '{}' and date >= '{}'  group by product_id order by count desc limit 10;
"""
BUCKET_NAME = 'daily_transactions'