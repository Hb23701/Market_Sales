from .constants import CREATE_CUSTOMER_TABLE, 
                        CREATE_PRODUCT_TABLE, 
                        CREATE_TRANSACTION_DETAIL_TABLE,
                        CREATE_TRANSACTION_TABLE,
                        INSERT_INTO_TRANSACTION,
                        INSERT_INTO_TRANSACTION_NULL_ID,
                        INSERT_INTO_TRANSACTION_DETAIL,
                        INSERT_INTO_PRODUCT,
                        INSERT_INTO_CUSTOMER,
                        INSERT_INTO_CUSTOMER_NULL_ID
from .connection import conn

def create_tables():
        connection = conn()    
        with connection.cursor() as cur:
                cur.execute(CREATE_PRODUCT_TABLE)
                cur.execute(CREATE_CUSTOMER_TABLE)
                cur.execute(CREATE_TRANSACTION_TABLE)
                cur.execute(CREATE_TRANSACTION_DETAIL_TABLE)
                connection.commit()


def populate_product_table(product_list):
        connection = conn()
        for row in product_list:
                with connection.cursor() as cur:
                        cur.execute('select * from products where id = {}'.format(row['id']))
                        res = cur.fetchall()
                        if res == []:
                                value_string = "{},'{}',{}".format(row['id'],row['item'],row['price'])
                                cur.execute(INSERT_INTO_PRODUCT.format(value_string))
                                connection.commit()

def populate_customer_table(customer_list):
        connection = conn()
        for row in customer_list:
                with connection.cursor() as cur:
                        if row['id'] != '':
                                value_string = "{}, '{}'".format(row['id'], row['name'])
                                execution_string = INSERT_INTO_CUSTOMER.format(value_string)            
                        else:
                                value_string = "'{}'".format(row['name'])
                                execution_string = INSERT_INTO_CUSTOMER_NULL_ID.format(value_string)

                        if row['id'] != '':
                                cur.execute('select * from customers where id = {}'.format(row['id']))
                                res = cur.fetchall()

                        if row['id'] == '' or res == []:
                                cur.execute(execution_string)
                                connection.commit()

def populate_transaction_table(transaction_list):
        connection = conn()
        for row in transaction_list:
                with connection.cursor() as cur:
                        if row['customer_id'] != '':
                                value_string = "'{}','{}','{}', {}".format(row['transaction_ref'],row['date'], row['type'], row['customer_id'])
                                execution_string = INSERT_INTO_TRANSACTION.format(value_string)
                        else:
                                value_string = "'{}','{}','{}'".format(row['transaction_ref'],row['date'], row['type'])
                                execution_string = INSERT_INTO_TRANSACTION_NULL_ID.format(value_string)

                        if row['customer_id'] != '':
                                cur.execute("select * from transactions where customer_id = {} and transaction_type = '{}' and transaction_ref = '{}'".format(row['customer_id'], row['type'], row['transaction_ref']))
                                res = cur.fetchall()

                        if row['customer_id'] == '' or res == []:
                                cur.execute(execution_string)
                                connection.commit()

def populate_transaction_details_table(transaction_details_list):
        connection = conn()
        for row in transaction_details_list:
                with connection.cursor() as cur:
                        cur.execute("select id from transactions where transaction_ref='{}' and transaction_type='{}'".format(row['transaction_ref'],  row['type']))
                        res = cur.fetchall()
                        if res == []:
                                continue
                        else:
                                row['transaction_id'] = res[0][0]

                        value_string = "'{}', '{}', '{}', {}".format(row['transaction_id'], row['date'], row['type'], row['product_id'])
                        cur.execute(INSERT_INTO_TRANSACTION_DETAIL.format(value_string))
                        connection.commit()