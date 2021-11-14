from config import config
import psycopg2

def alter_tables1():
  """ alter tables in the PostgreSQL database"""
  commands = [
      "ALTER TABLE fab_scraped_cards ADD UNIQUE(card_name)"]
  conn = None
  try:
    params = config()

    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.close()
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
        conn.close()


def alter_tables2():
  """ alter tables in the PostgreSQL database"""
  commands = [
      "ALTER TABLE fab_scraped_cards ADD UNIQUE(source_url)"]
  conn = None
  try:
    params = config()

    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.close()
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
        conn.close()

if __name__ == '__main__':
    alter_tables1()
    alter_tables2()
