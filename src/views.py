def create_top_ten_refunded_view():
    with conn.cursor() as cur:
        cur.execute(CREATE_TOP_TEN_REFUNDED_ITEMS_VIEW.format(datetime.date.today(), datetime.datetime.now() - datetime.timedelta(days=365)))
        conn.commit()
        cur.execute("select * from RefundedItem;")
        res = cur.fetchall()

def create_monthly_sales_report():
    DATE_GROUP = "select count(id), date_trunc('month', date) m from transaction_details group by m;"
    ANOTHER_QUERY="""
                select p.id, sum(p.price) from transaction_details td join products p on td.product_id = p.id
                where td.transaction_type = 'Sales' and td.date between '{}' and '{}' group by p.id;
            """
    VIEW_QUERY = f"CREATE VIEW MONTHLY_SALES as {ANOTHER_QUERY}"
    INSERT_VIEW = "insert into MONTHLY_SALES values ({}, {})"
    connection = conn()
    global prev_date
    with connection.cursor() as cur:
        cur.execute(DATE_GROUP)
        [first_date_group, *date_groups] = cur.fetchall()
        m = first_date_group[1]
        cur.execute(VIEW_QUERY.format(m.date(), prev_date))
        prev_date = m.date()
        for _count, m in date_groups:
            cur.execute(ANOTHER_QUERY.format(m.date(), prev_date))
            res = cur.fetchall()
            for pid, psum in res:
                cur.execute(INSERT_VIEW.format(pid,psum))
            prev_date = m.date()