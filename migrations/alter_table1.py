from ..config import config
import psycopg2

def alter_tables():
  """ alter tables in the PostgreSQL database"""
  commands = [
      """ALTER TABLE fab_scraped_cards 
      ADD CONSTRAINT constraint_name 
      UNIQUE (card_name, source_url); 
      """]
  conn = None
  try:
    params = config()

    conn = psycopg2.connect(**params)
    cur = conn.cursor()

    cur.execute(commands[0])

    cur.close()
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
        conn.close()

if __name__ == '__main__':
    alter_tables()
