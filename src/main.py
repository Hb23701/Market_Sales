import psycopg2
import csv
import glob
from .s3 import download_files_from_s3
from .tables import create_tables, populate_customer_table, populate_product_table, populate_transaction_details_table, populate_transaction_table
from .views import create_monthly_sales_report, create_top_ten_refunded_view

def read_from_csv(file_path):
    global product_list
    global customer_list
    global transaction_list
    global transaction_details_list

    with open(file_path, mode = 'r') as mycsvfile:
        x = csv.DictReader(mycsvfile)
        date = file_path.split("/")[-2]
        for row in x:
            product_list.append({
                'id': row['product_id'],
                'item': row['Item'],
                'price': row['product_price']
            })
            customer_list.append({
                'id': int(row['member_id'][4:]) if(row['member_id'] != '') else '',
                'name': row['customer_name']
            })
            transaction_list.append({
                'transaction_ref': row['Transaction_id'],
                'date': date,
                'price': 'total_price',
                'type': row['transaction_type'],
                'customer_id': int(row['member_id'][4:]) if(row['member_id'] != '') else ''
                })
            transaction_details_list.append({
                'transaction_ref': row['Transaction_id'],
                'date': date,
                'type': row['transaction_type'],
                'product_id': row['product_id']
                })


if __name__ == "__main__":
    create_tables()

    product_list = []
    customer_list = []
    transaction_list = []
    transaction_details_list = []

    date_format = ""
    current_date = datetime.strptime('2016-01-01', "%Y-%m-%d")

    while current_date < datetime.now().date():
        download_files_from_s3(date)
        my_path=f"tmp/{date_format}"
        files = glob.glob(my_path + '/**/*.csv', recursive=True)
        for file_path in files:
            read_from_csv(file_path)

        populate_customer_table(customer_list)
        populate_product_table(product_list)
        populate_transaction_table(transaction_list)
        populate_transaction_details_table(transaction_details_list)
        
        current_date = current_date + timedelta(days=1)

    # Create Top Ten Refunded View
    create_top_ten_refunded_view()
    create_monthly_sales_report()