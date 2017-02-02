import json
import psycopg2
import urllib.request
import pprint

pp = pprint.PrettyPrinter(indent=4)


def connect(user, passwd, db, host='localhost', port=5432):
    try:
        conn_string = "dbname='{}' user='{}' host='{}' password='{}'"
        parsed = conn_string.format(db, user, host, passwd)
        print(parsed)
        conn = psycopg2.connect(parsed)
    except Exception as e:
        print(e)
        raise e
    
    return conn


def fetch_data(query='', url="https://api.zalando.com/articles"):
    x = urllib.request.urlopen(url).read().decode('utf-8')
    json_obj = json.loads(x)
    return json_obj


def add_products_to_db(cur, temp, val):
    cur.execute(temp, val)


def scrap_desired_pair(articles):
    products = articles['content']
    for product in products:
        name = product['name']
        brand = product['brand']['name']
        price = product['units'][0]['price']['value']
        img = product['media']['images'][0]['smallUrl']

        yield img, name, price, brand


def main():
    articles = fetch_data()
    conn = connect('postgres', '', 'test')
    cur = conn.cursor()
    for x in scrap_desired_pair(articles):
        temp = "INSERT INTO products VALUES (%s, %s, %s, %s)"
        add_products_to_db(cur, temp, x)
    conn.commit()


if __name__ == '__main__':
    main()

