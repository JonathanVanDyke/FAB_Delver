import psycopg2
from config import config


def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

	# execute a statement
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        postgres_insert_query = """INSERT INTO fab_scraped_cards (card_name, rarity, num, price, source_url) VALUES (%s,%s,%s,%s,%s)"""
        record_to_insert = ('Zealous Belting(Red)', 'Common', 'MON295', '$0.16', '-',)
        cur.execute(postgres_insert_query, record_to_insert)
        # print(record_to_insert)
        conn.commit()

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print('You are connected to: ', db_version)

	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
