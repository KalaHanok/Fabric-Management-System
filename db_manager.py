import sqlite3
from datetime import datetime

class DBManager:
    def __init__(self, db_name="fabric_management.db"):
        """Initialize and connect to the database."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

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
            self.cursor.execute("UPDATE fabrics SET stock = stock + ? WHERE fabric_id = ?", (quantity, fabric_id))
        elif operation == "subtract":
            self.cursor.execute("UPDATE fabrics SET stock = stock - ? WHERE fabric_id = ?", (quantity, fabric_id))
        self.conn.commit()

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
                sales_record.total_sales * sales_record.selling_price as revenue,
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
    def get_fabric_name_by_id(self,  fabric_id):
        """Get the fabric name from the fabric ID."""
        self.cursor.execute("SELECT fabric_name FROM fabrics WHERE fabric_id = ?", (fabric_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None
    def get_fabrics_list(self):
        """Get a list of fabrics from the database to populate the combo boxes."""
        self.db_manager.cursor.execute("SELECT fabric_name FROM fabrics")
        fabrics = self.db_manager.cursor.fetchall()
        return [fabric[1] for fabric in fabrics]
    def get_fabric_stock(self, fabric_name):
        """Get stock for a specific fabric."""
        self.cursor.execute("SELECT stock FROM fabrics WHERE fabric_name = ?", (fabric_name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
    def get_all_fabrics_stock(self):
        """Get stock levels for all fabrics."""
        self.cursor.execute("SELECT fabric_name, stock FROM fabrics")
        return self.cursor.fetchall()
    
    def get_sales_data(self, start_date, end_date):
        """ Get the sales data from start_date to end_date"""
        self.cursor.execute("select sales.sale_date, fabrics.fabric_name, sales.quantity, sales.selling_price, sales.quantity*sales.selling_price as revenue from sales join fabrics on sales.fabric_id = fabrics.fabric_id where sales.sale_date BETWEEN ? and ? order by sales.sale_date desc",(start_date,end_date))
        return self.cursor.fetchall()

    def get_purchase_data(self, start_date, end_date):
        """ Get the purchase  data of stocks from start_date to end_date"""
        self.cursor.execute('''select purchases.purchase_date, fabrics.fabric_name, purchases.quantity, purchases.cost_price, purchases.quantity*purchases.cost_price as expendicture 
                            from purchases join fabrics on purchases.fabric_id = fabrics.fabric_id 
                            where purchases.purchase_date BETWEEN ? and ? order by purchases.purchase_date desc''',(start_date,end_date))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection."""
        self.conn.close()
