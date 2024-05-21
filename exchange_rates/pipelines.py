import mysql.connector
from datetime import datetime

class ExchangeRatesPipeline:
    def __init__(self):
        self.db_connection = None
        self.db_cursor = None

    def open_spider(self, spider):
        # Establish a connection to the MySQL database
        self.db_connection = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='finavulq_continentl'
        )
        self.db_cursor = self.db_connection.cursor()
        
        # No need to create the table here if it already exists

    def process_item(self, item, spider):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Convert market_time to a timestamp
        # market_time_str = item['market_time']
        # market_time = datetime.strptime(market_time_str, "%H.%M %Z").strftime("%Y-%m-%d %H:%M:%S")

        market_time = item['market_time']
        
        # Check if the record exists
        self.db_cursor.execute("""
            SELECT id FROM crypto_currency_exchange_rates
            WHERE base_currency = %s AND foreign_currency = %s
        """, (item['base_currency'], item['foreign_currency']))
        result = self.db_cursor.fetchone()

        if result:
            # Update the existing record
            self.db_cursor.execute("""
                UPDATE crypto_currency_exchange_rates
                SET rate = %s, updated_at = %s, market_time = %s
                WHERE id = %s
            """, (item['exchange_rate'], now, market_time, result[0]))
        else:
            # Insert a new record
            self.db_cursor.execute("""
                INSERT INTO crypto_currency_exchange_rates (base_currency, foreign_currency, rate, created_at, updated_at, market_time)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (item['base_currency'], item['foreign_currency'], item['exchange_rate'], now, now, market_time))
        
        self.db_connection.commit()
        return item

    def close_spider(self, spider):
        # Close the database connection
        self.db_cursor.close()
        self.db_connection.close()






# import csv
# from datetime import datetime

# class ExchangeRatesPipeline:
#     def __init__(self):
#         self.exchange_rates_file = 'exchange_rates.csv'
#         self.fields = ['Base-Currency', 'Foreign-Currency', 'Exchange-Rate', 'Updated_at']

#     def open_spider(self, spider):
#         self.csvfile = open(self.exchange_rates_file, 'a', newline='')
#         self.writer = csv.DictWriter(self.csvfile, fieldnames=self.fields)

#         # Write headers only if the file is empty
#         if self.csvfile.tell() == 0:
#             self.writer.writeheader()

#     def process_item(self, item, spider):
#         updated = False
#         rows = []
#         now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#         with open(self.exchange_rates_file, 'r', newline='') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 if row['Base-Currency'] == item['base_currency'] and row['Foreign-Currency'] == item['foreign_currency']:
#                     row['Exchange-Rate'] = item['exchange_rate']
#                     row['Updated_at'] = now
#                     updated = True
#                 rows.append(row)

#         if not updated:
#             new_row = {'Base-Currency': item['base_currency'], 'Foreign-Currency': item['foreign_currency'], 'Exchange-Rate': item['exchange_rate'], 'Updated_at': now}
#             rows.append(new_row)

#         with open(self.exchange_rates_file, 'w', newline='') as csvfile:
#             writer = csv.DictWriter(csvfile, fieldnames=self.fields)
#             writer.writeheader()
#             writer.writerows(rows)

#         return item

#     def close_spider(self, spider):
#         self.csvfile.close()
