import sqlite3

def setup_database():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # Create fabrics table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fabrics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            current_stock REAL DEFAULT 0,
            cost_price REAL
        )
    ''')

    # Create sales table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fabric_id INTEGER,
            quantity_sold REAL,
            selling_price REAL,
            total_value REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (fabric_id) REFERENCES fabrics (id)
        )
    ''')

    # Create purchases table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS purchases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fabric_id INTEGER,
            quantity_purchased REAL,
            cost_price REAL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (fabric_id) REFERENCES fabrics (id)
        )
    ''')

    connection.commit()
    connection.close()

if __name__ == '__main__':
    setup_database()
