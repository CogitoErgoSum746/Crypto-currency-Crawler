import mysql.connector
from datetime import datetime

class CryptoPipeline:
    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def open_spider(self, spider):
        # Establish a connection to the MySQL database
        self.db_connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='finavulq_continentl'  # Change this to your actual database name
        )
        self.db_cursor = self.db_connection.cursor()
        
        # No need to create the table here if it already exists

    def process_item(self, item, spider):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Extract values from the item
        code = item['code']
        name = item['name']
        price = item['price']
        volume_24h = item['volume_24h']
        market_cap = item['market_cap']
        ranking = item['rank']

        # Check if the record exists
        self.db_cursor.execute("""
            SELECT id FROM crypto_currency_exchange_rates
            WHERE code = %s
        """, (code,))
        result = self.db_cursor.fetchone()

        if result:
            # Update the existing record
            self.db_cursor.execute("""
                UPDATE crypto_currency_exchange_rates
                SET name = %s, price = %s, 24hr_volume = %s, market_capitalization = %s, ranking = %s, updated_at = %s
                WHERE id = %s
            """, (name, price, volume_24h, market_cap, ranking, now, result[0]))
        else:
            # Insert a new record
            self.db_cursor.execute("""
                INSERT INTO crypto_currency_exchange_rates (code, name, price, 24hr_volume, market_capitalization, ranking, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (code, name, price, volume_24h, market_cap, ranking, now, now))
        
        self.db_connection.commit()
        return item

    def close_spider(self, spider):
        # Close the database connection
        self.db_cursor.close()
        self.db_connection.close()
