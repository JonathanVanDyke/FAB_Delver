
import psycopg2
import config

class FabCardController:
  def __init__(self):
    pass

  def list_all(self):
    params = config()
    conn = psycopg2.connect(**params)

    cur = conn.cursor()
    q = '''
      SELECT * 
      FROM fab_scraped_cards 
      LIMIT 1000;
    '''
    cur.execute(q)
    results = cur.fetchall()
    print(results)
    cur.close()
    conn.close()
    
    return results

  def create_record(self, rec):

    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    q = '''INSERT INTO fab_scraped_cards (card_name, rarity, num, price, source_url) VALUES (%s,%s,%s,%s,%s)'''

    res = cur.execute(q, rec)
    
    conn.commit()
    
    

    cur.close()
    conn.close()
    # return results
    # TODO: look into UPSERT for postgresql, ON CONFLICT UPDATE
    return

  def delete_record_by_id(self, id):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    q = '''DELETE FROM fab_scraped_cards WHERE scrape_id=%s'''
    # id = str(id)
    cur.execute(q, (id,))
    conn.commit()
    # self.list_all()
    cur.close()
    conn.close()
    # return results
    return

  def delete_record_by_card_name(self, name):
    params = config()
    conn = psycopg2.connect(**params)
    cur = conn.cursor()
    q = '''DELETE FROM fab_scraped_cards WHERE card_name=%s'''
    # id = str(id)
    cur.execute(q, (name,))
    conn.commit()
    # self.list_all()
    cur.close()
    conn.close()
    # return results
    return


  

# # list_all()
# fb_controller = FabCardController()
# # fb_controller.list_all()
# record = ('test', 'test', 'test', 'test', '-',)
# fb_controller.create_record(record)

# # fb_controller.delete_record_by_card_name('test')
# # fb_controller.delete_record_by_id(32)
# fb_controller.list_all()
