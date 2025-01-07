import sqlite3
from datetime import datetime

import sys
import os

if getattr(sys, 'frozen', False):  # Check if it's running as an executable
    base_path = os.getcwd()
else:
    base_path = os.path.abspath(".")

db_path = os.path.join(base_path, 'fabric_management.db')
print("Database Path:", db_path)


class DBManager:
    def __init__(self, db_name="fabric_management.db"):
        """Initialize and connect to the database."""
        self.conn = sqlite3.connect(db_path)
        if self.conn:
            print("Connection is established")
        else:
            print("connection is  not established")
        self.cursor = self.conn.cursor()
        self.create_tables()
    def test_connection(self):
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = self.cursor.fetchall()
            print("Tables:", tables)
        except Exception as e:
            print("Error:", e)
    def create_tables(self):
        """Create necessary tables if they don't exist."""
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS fabrics (
                                fabric_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                fabric_name TEXT UNIQUE NOT NULL,
                                stock REAL NOT NULL DEFAULT 0)''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS purchases (
                                purchase_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                fabric_id INTEGER,
                                quantity REAL NOT NULL,
                                cost_price REAL NOT NULL,
                                purchase_date TEXT NOT NULL,
                                FOREIGN KEY (fabric_id) REFERENCES fabrics(fabric_id))''')

        self.cursor.execute('''CREATE TABLE IF NOT EXISTS sales (
                                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                fabric_id INTEGER,
                                quantity REAL NOT NULL,
                                selling_price REAL NOT NULL,
                                sale_date TEXT NOT NULL,
                                FOREIGN KEY (fabric_id) REFERENCES fabrics(fabric_id))''')

        self.conn.commit()

    # ---- CRUD Operations for Stock Management ----
    def add_fabric(self, fabric_name, stock):
        """Add a new fabric to the database."""
        try:
            self.cursor.execute("INSERT INTO fabrics (fabric_name, stock) VALUES (?, ?)", (fabric_name,stock))
            self.conn.commit()
            return {"success":f"Successfully added the {fabric_name}"}
        except sqlite3.IntegrityError:
            raise ValueError(f"Fabric '{fabric_name}' already exists.")

    def update_stock(self, fabric_id, quantity, operation="add"):
        """Update fabric stock by adding or subtracting the quantity."""
        if operation == "add":
            res=self.cursor.execute("UPDATE fabrics SET stock = stock + ? WHERE fabric_id = ?", (quantity, fabric_id))
        elif operation == "subtract":
            res=self.cursor.execute("UPDATE fabrics SET stock = stock - ? WHERE fabric_id = ?", (quantity, fabric_id))
        self.conn.commit()
        return res

    def get_fabric_stock(self, fabric_name):
        """Get the stock of a particular fabric."""
        self.cursor.execute("SELECT stock FROM fabrics WHERE fabric_name = ?", (fabric_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        else:
            raise ValueError(f"Fabric '{fabric_name}' not found.")

    def get_total_stock(self):
        """Get the total available stock across all fabrics."""
        self.cursor.execute("SELECT SUM(stock) FROM fabrics")
        total_stock = self.cursor.fetchone()[0]
        return total_stock if total_stock else 0

    # ---- Purchase Operations ----
    def add_purchase(self, fabric_id, quantity, cost_price):
        """Record a purchase transaction and update the stock."""
        purchase_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("INSERT INTO purchases (fabric_id, quantity, cost_price, purchase_date) VALUES (?, ?, ?, ?)",
                            (fabric_id, quantity, cost_price, purchase_date))
        self.update_stock(fabric_id, quantity, operation="add")
        self.conn.commit()

    # ---- Sales Operations ----
    def add_sale(self, fabric_id, quantity, selling_price):
        """Record a sale transaction and update the stock."""
        sale_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute("INSERT INTO sales (fabric_id, quantity, selling_price, sale_date) VALUES (?, ?, ?, ?)",
                            (fabric_id, quantity, selling_price, sale_date))
        self.update_stock(fabric_id, quantity, operation="subtract")
        self.conn.commit()

    def get_total_sales(self, fabric_id):
        """Get the total sales for a specific fabric."""
        self.cursor.execute("SELECT SUM(quantity) FROM sales WHERE fabric_id = ?", (fabric_id,))
        total_sales = self.cursor.fetchone()[0]
        return total_sales if total_sales else 0

    # ---- Profit/Loss Operations ----
    def get_total_profit_loss(self, start_date, end_date):
        """Calculate the total profit or loss based on sales and purchases between two dates."""
        self.cursor.execute(f'''
            WITH latest_cost AS (
                SELECT fabric_id, SUM(quantity*cost_price)/SUM(quantity) AS cost_price 
                FROM purchases 
                GROUP BY fabric_id
            ),
            sales_record AS (
                SELECT fabric_id, SUM(quantity) AS total_sales, 
                SUM(quantity*selling_price)/SUM(quantity) AS selling_price 
                FROM sales 
                WHERE sale_date BETWEEN ? AND ? 
                GROUP BY fabric_id
            )
            SELECT sales_record.fabric_id,
                sales_record.total_sales,
                latest_cost.cost_price,
                sales_record.selling_price,
                sales_record.total_sales * sales_record.selling_price as revenue,
                sales_record.total_sales * latest_cost.cost_price as cost,
                sales_record.total_sales * sales_record.selling_price - 
                sales_record.total_sales * latest_cost.cost_price AS profit
            FROM latest_cost 
            JOIN sales_record 
            ON latest_cost.fabric_id = sales_record.fabric_id;
        ''', (start_date, end_date))

        return self.cursor.fetchall()


    # ---- Utility Operations ----
    def get_fabric_id(self, fabric_name):
        """Get the fabric ID from the fabric name."""
        self.cursor.execute("SELECT fabric_id FROM fabrics WHERE fabric_name = ?", (fabric_name,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    def search_fabrics(self, search_term):
        # Query to search for fabrics that match the input text
        query = "SELECT fabric_name FROM fabrics WHERE fabric_name LIKE ?"
        self.cursor.execute(query, ('%' + search_term + '%',))
        result = self.cursor.fetchall()
        return [row[0] for row in result]  # Assuming fabric_name is the first column
    def get_fabric_name_by_id(self,  fabric_id):
        """Get the fabric name from the fabric ID."""
        self.cursor.execute("SELECT fabric_name FROM fabrics WHERE fabric_id = ?", (fabric_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    def get_fabrics_list(self):
        """Get a list of fabrics from the database to populate the combo boxes."""
        self.cursor.execute("SELECT fabric_name FROM fabrics")
        fabrics = self.cursor.fetchall()
        return [fabric[0] for fabric in fabrics]
    def get_fabric_stock(self, fabric_name):
        """Get stock for a specific fabric."""
        self.cursor.execute("SELECT stock FROM fabrics WHERE fabric_name = ?", (fabric_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
    def get_fabric_stock_by_id(self, fabric_id):
        """Get stock for a specific fabric."""
        self.cursor.execute("SELECT stock FROM fabrics WHERE fabric_id = ?", (fabric_id,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
    def get_all_fabrics(self):
        """Get stock for a specific fabric."""
        self.cursor.execute("SELECT fabric_id, fabric_name, stock from fabrics")
        result = self.cursor.fetchall()
        if result:
            return result
    def get_all_fabrics_stock(self):
        """Get stock levels for all fabrics."""
        self.cursor.execute("""
                                WITH latest_cost AS (
                                SELECT fabric_id, SUM(quantity*cost_price)/SUM(quantity) AS cost_price 
                                FROM purchases 
                                GROUP BY fabric_id
                                )
                                select fabrics.fabric_id, fabrics.fabric_name, fabrics.stock, COALESCE(latest_cost.cost_price,0) as cost_price, COALESCE(latest_cost.cost_price*stock,0) as total_cost 
                                from fabrics left join latest_cost on fabrics.fabric_id = latest_cost.fabric_id
                            """)
        return self.cursor.fetchall()
    
    def get_purchase_cost(self, fabric_id):
        self.cursor.execute("""
                                SELECT fabric_id, SUM(quantity*cost_price)/SUM(quantity) AS cost_price 
                                FROM purchases 
                                where fabric_id=?
                            """,(fabric_id,))
        return self.cursor.fetchone()[1]
        

    def get_sales_data(self, start_date, end_date):
        """ Get the sales data from start_date to end_date"""
        self.cursor.execute("select sales.sale_id, sales.sale_date, fabrics.fabric_name, sales.quantity, sales.selling_price, sales.quantity*sales.selling_price as revenue from sales join fabrics on sales.fabric_id = fabrics.fabric_id where sales.sale_date BETWEEN ? and ? order by sales.sale_date desc",(start_date,end_date))
        return self.cursor.fetchall()

    def get_purchase_data(self, start_date, end_date):
        """ Get the purchase  data of stocks from start_date to end_date"""
        self.cursor.execute('''select purchases.purchase_id, purchases.purchase_date, fabrics.fabric_name, purchases.quantity, purchases.cost_price, purchases.quantity*purchases.cost_price as expendicture 
                            from purchases join fabrics on purchases.fabric_id = fabrics.fabric_id 
                            where purchases.purchase_date BETWEEN ? and ? order by purchases.purchase_date desc''',(start_date,end_date))
        return self.cursor.fetchall()
    
    def get_sale_by_id(self,id):
        """Get sales by sales_id"""
        self.cursor.execute('''SELECT * from sales where sale_id=?''',(id,))
        return self.cursor.fetchone()
    
    def get_purchase_by_id(self, id):
        """Get purchase by purchase_id"""
        self.cursor.execute('''SELECT * from purchases where purchase_id=?''',(id,))
        return self.cursor.fetchone()
    def update_sale_data(self, sale_id, quantity, selling_price, sale_date):
        query = """
            UPDATE sales
            SET quantity = ?, selling_price = ?, sale_date = ?
            WHERE sale_id = ?
        """
        res=self.cursor.execute(query, (quantity, selling_price, sale_date, sale_id))
        self.conn.commit()
        return res

    def update_purchase_data(self,purchase_id, quantity, cost_price, purchase_date):
        query = """
            UPDATE purchases
            SET quantity = ?, cost_price = ?, purchase_date = ?
            WHERE purchase_id = ?
        """
        res=self.cursor.execute(query, (quantity, cost_price, purchase_date, purchase_id))
        self.conn.commit()
        return res
    def update_fabric_name(self, fabric_id,fabric_name):
        query = """
            UPDATE fabrics
            SET fabric_name = ?
            WHERE fabric_id = ?
        """
        res=self.cursor.execute(query, (fabric_name,fabric_id))
        self.conn.commit()
        return  res
    def close(self):
        """Close the database connection."""
        self.conn.close()
