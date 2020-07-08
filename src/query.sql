CREATE OR REPLACE sadaas() 
RETURNS SETOF transaction_details AS $BODY$
DECLARE
    r transaction_details%rowtype;
BEGIN
    FOR rec in EXECUTE 'select count(id), date_trunc('month', date) m from transaction_details group by m'
    LOOP
        EXECUTE 'select p.id, sum(p.price) from transaction_details td join products p on td.product_id = p.id where td.transaction_type = 'Sales' and td.date between r.m - interval '1 month' and r.m group by p.id;';
    END LOOP;
END;
END;
