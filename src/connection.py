import psycopg2

def conn():
    return psycopg2.connect("postgresql://localhost/himani")

