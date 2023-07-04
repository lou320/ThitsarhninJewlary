import os
import mysql.connector
from datetime import datetime, date
# Replace the placeholders with your actual database details
host = 'Wongmingfu999.mysql.pythonanywhere-services.com'
user = 'Wongmingfu999'
password = 'tor123Browser'
database = 'Wongmingfu999$default'
port = '3306'

# Create a connection
connection = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
    port=port
)
cursor = connection.cursor()
def create_tables():
    # Use the connection for database operations
    
    # Execute SQL queries or perform other database operations
    create_table_query = """
    CREATE TABLE items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        image_url TEXT,
        item_name TEXT,
        bought_value DOUBLE,
        item_gram DOUBLE,
        bought_ayottwat TEXT,
        sell_ayottwat TEXT,
        is_sold BOOLEAN DEFAULT 0,
        posted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        sold_date TIMESTAMP DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP)"""

    try:
        cursor.execute(create_table_query)
        return True
    except mysql.connector.Error as e:
        return False

    # Close the connection when done
    

def add_item_to_database(image,item_name,item_bought_value,item_item_gram,item_bought_ayottwat,item_sell_ayottwat):
    insert_query = """
            INSERT INTO items (image_url, item_name, bought_value, item_gram, bought_ayottwat, sell_ayottwat)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
    select_query = "SELECT LAST_INSERT_ID()"
    values = (image, item_name, item_bought_value, item_item_gram, item_bought_ayottwat, item_sell_ayottwat)
    
    try:
        cursor.execute(insert_query, values)
        connection.commit()
        cursor.execute(select_query)
        item_id = cursor.fetchone()[0]
        return item_id
    except Exception as error:
        return False


def fetch_items_from_database():
    select_query = """
        SELECT * FROM items ORDER BY posted_date DESC
    """

    try:
        cursor.execute(select_query)
        rows = cursor.fetchall()
        items = []
        if len(rows) > 0:
            for row in rows:
                item = {
                    'id': row[0],
                    'image_url': row[1],
                    'item_name': row[2],
                    'bought_value': row[3],
                    'item_gram': row[4],
                    'bought_ayottwat': row[5],
                    'sell_ayottwat': row[6],
                    'is_sold': row[7],
                    'posted_date': row[8],
                    'sold_date': row[9]
                }
                items.append(item)
            return items
        else:
            return 'There are no items'
    except mysql.connector.Error as e:
        print("Error:", e)
        return []

    
def search_by_name(search_query):
    search_query = f"%{search_query}%"
    query = """
    SELECT * FROM items WHERE item_name LIKE %s
    """
    try:
        cursor.execute(query, (search_query,))
        rows = cursor.fetchall()
        print(rows)
        items = []
        if len(rows) > 0:
                for row in rows:
                    item = {
                        'id': row[0],
                        'image_url': row[1],
                        'item_name': row[2],
                        'bought_value': row[3],
                        'item_gram': row[4],
                        'bought_ayottwat': row[5],
                        'sell_ayottwat': row[6],
                        'is_sold': row[7],
                        'posted_date': row[8],
                        'sold_date': row[9]
                    }
                    items.append(item)
                return items
        else:
            return 'ပစ္စည်းမရှိပါ'
    except mysql.connector.Error as e:
        return 'ပစ္စည်းမရှိပါ'


def search_by_id(item_id):
    query = """
    SELECT * FROM items WHERE id = %s
    """
    try:
        cursor.execute(query, (item_id,))
        rows = cursor.fetchall()
        items = []
        if len(rows) > 0:
                for row in rows:
                    item = {
                        'id': row[0],
                        'image_url': row[1],
                        'item_name': row[2],
                        'bought_value': row[3],
                        'item_gram': row[4],
                        'bought_ayottwat': row[5],
                        'sell_ayottwat': row[6],
                        'is_sold': row[7],
                        'posted_date': row[8],
                        'sold_date': row[9]
                    }
                    items.append(item)
                return items
        else:
            return 'ပစ္စည်းမရှိပါ'
    except mysql.connector.Error as e:
        return 'ပစ္စည်းမရှိပါ'


def search_items_by_sold_date(sold_date):
    select_query = """
        SELECT * FROM items WHERE DATE(sold_date) = %s
    """

    try:
        cursor.execute(select_query, (sold_date,))
        rows = cursor.fetchall()
        items = []
        if len(rows) > 0:
            for row in rows:
                item = {
                    'id': row[0],
                    'image_url': row[1],
                    'item_name': row[2],
                    'bought_value': row[3],
                    'item_gram': row[4],
                    'bought_ayottwat': row[5],
                    'sell_ayottwat': row[6],
                    'is_sold': row[7],
                    'posted_date': row[8],
                    'sold_date': row[9]
                }
                items.append(item)
            return items
        else:
            return 'No items found for the specified sold date.'
    except mysql.connector.Error as e:
        return 'An error occurred while searching for items.'



def search_items_by_year_and_month(year, month):
    select_query = """
        SELECT * FROM items WHERE YEAR(sold_date) = %s AND MONTH(sold_date) = %s
    """

    try:
        cursor.execute(select_query, (year, month))
        rows = cursor.fetchall()
        items = []
        if len(rows) > 0:
            for row in rows:
                item = {
                    'id': row[0],
                    'image_url': row[1],
                    'item_name': row[2],
                    'bought_value': row[3],
                    'item_gram': row[4],
                    'bought_ayottwat': row[5],
                    'sell_ayottwat': row[6],
                    'is_sold': row[7],
                    'posted_date': row[8],
                    'sold_date': row[9]
                }
                items.append(item)
            return items
        else:
            return 'No items found for the specified year and month.'
    except mysql.connector.Error as e:
        return 'An error occurred while searching for items.'



def remove_item_from_database(item_id):
    select_query = "SELECT image_url FROM items WHERE id = %s"
    delete_query = "DELETE FROM items WHERE id = %s"

    try:
        # Get the image URL before deleting the item
        cursor.execute(select_query, (item_id,))
        result = cursor.fetchone()
        if result:
            image_url = result[0]
            # Delete the item image file from storage
            if image_url:
                os.remove(image_url)

        # Delete the item from the database
        cursor.execute(delete_query, (item_id,))
        connection.commit()
        return True
    except Exception as error:
        print("Error:", error)
        return False
    
def get_sold_items_from_database():
    select_query = """
        SELECT * FROM items WHERE is_sold = TRUE
    """

    try:
        cursor.execute(select_query)
        rows = cursor.fetchall()
        items = []
        if len(rows) > 0:
            for row in rows:
                item = {
                    'id': row[0],
                    'image_url': row[1],
                    'item_name': row[2],
                    'bought_value': row[3],
                    'item_gram': row[4],
                    'bought_ayottwat': row[5],
                    'sell_ayottwat': row[6],
                    'is_sold': row[7],
                    'posted_date': row[8],
                    'sold_date': row[9]
                }
                items.append(item)
            return items
        else:
            return 'No sold items found'
    except mysql.connector.Error as e:
        print("Error:", e)
        return []


def get_items_sold_today_from_database():
    today = date.today()
    select_query = """
        SELECT * FROM items WHERE DATE(sold_date) = %s
    """

    try:
        cursor.execute(select_query, (today,))
        rows = cursor.fetchall()
        items = []
        if len(rows) > 0:
            for row in rows:
                item = {
                    'id': row[0],
                    'image_url': row[1],
                    'item_name': row[2],
                    'bought_value': row[3],
                    'item_gram': row[4],
                    'bought_ayottwat': row[5],
                    'sell_ayottwat': row[6],
                    'is_sold': row[7],
                    'posted_date': row[8],
                    'sold_date': row[9]
                }
                items.append(item)
            return items
        else:
            return 'No items sold today'
    except mysql.connector.Error as e:
        print("Error:", e)
        return []



def mark_item_as_sold(item_id):
    update_query = """
        UPDATE items SET is_sold = True, sold_date = %s WHERE id = %s
    """
    sold_date = datetime.now()

    try:
        cursor.execute(update_query, (sold_date, item_id))
        connection.commit()
        return True
    except Exception as error:
        print("Error:", error)
        return False
