import psycopg2
import config

def create_tables():
  """ create tables in the PostgreSQL database"""
  commands = ["CREATE TABLE fab_scraped_cards ( scrape_id SERIAL PRIMARY KEY, card_name VARCHAR(255) NOT NULL, rarity VARCHAR(255), num VARCHAR(255), price VARCHAR(255), source_url VARCHAR(255) NOT NULL)"]
  conn = None
  try:
    # read the connection parameters
    params = config()
    # connect to the PostgreSQL server
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    # create table one by one

    for command in commands:
      print(command)
      cur.execute(command)
    
    # close communication with the PostgreSQL database server
    cur.close()
    # commit the changes
    conn.commit()
  except (Exception, psycopg2.DatabaseError) as error:
    print(error)
  finally:
    if conn is not None:
        conn.close()


if __name__ == '__main__':
    create_tables()
