import tkinter as tk
from tkinter import ttk, messagebox

class UIManager:
    def __init__(self, root, db_manager):
        """Initialize the UIManager with the root Tkinter window and a DBManager instance."""
        self.root = root
        self.db_manager = db_manager

        # Setup UI elements
        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface components like buttons, tabs, forms, etc."""
        # Create the main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a Notebook (tabbed interface)
        self.tab_control = ttk.Notebook(self.main_frame)
        
        # Create Summary tab
        self.tab_summary = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_summary, text="Summary")
        self.create_summary_tab()

        # Create Sales tab
        self.tab_sales = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_sales, text="   Sales  ")
        self.create_sales_tab()

        # Create Purchase tab
        self.tab_purchase = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_purchase, text="Purchase")
        self.create_purchase_tab()

        # Create Add Fabrics tab
        self.tab_add_fabric = ttk.Frame(self.tab_control)
        self.tab_control.add(self.tab_add_fabric, text="Add Fabrics")
        self.create_add_fabric_tab()

        # Display tabs
        self.tab_control.pack(expand=1, fill="both")

    def create_summary_tab(self):
        """Create the summary tab that shows an overview of stock and profit/loss."""
        # Configure grid to center elements and distribute them equally
        self.tab_summary.grid_columnconfigure(0, weight=1)
        self.tab_summary.grid_columnconfigure(1, weight=1)
        self.tab_summary.grid_rowconfigure(0, weight=1)
        self.tab_summary.grid_rowconfigure(1, weight=1)

        # Create labels for displaying total stock information
        self.label_total_stock = tk.Label(self.tab_summary, text="Stock Information", font=("Arial", 14))
        self.label_total_stock.grid(row=0, column=0, padx=20, pady=10, sticky="e")

        self.label_stock_value = tk.Label(self.tab_summary, text="", font=("Arial", 14))
        self.label_stock_value.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # Dropdown (combobox) to select fabric or "All"
        self.label_select_fabric = tk.Label(self.tab_summary, text="Select Fabric:", font=("Arial", 12))
        self.label_select_fabric.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        self.combo_fabrics_summary = ttk.Combobox(self.tab_summary, values=["All"] + self.get_fabrics_list(), state="readonly")
        self.combo_fabrics_summary.grid(row=1, column=1, padx=10, pady=10, sticky="w")
        self.combo_fabrics_summary.current(0)  # Default to "All"
        self.combo_fabrics_summary.bind("<<ComboboxSelected>>", self.update_fabric_stock)

        # Create a table for displaying individual fabric stocks (when "All" is selected)
        self.tree_fabric_stock = ttk.Treeview(self.tab_summary, columns=("Fabric", "Stock"), show="headings", height=5)
        self.tree_fabric_stock.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Define the headings for the stock table
        self.tree_fabric_stock.heading("Fabric", text="Fabric")
        self.tree_fabric_stock.heading("Stock", text="Stock (units)")
        
        # Adjust column widths
        self.tree_fabric_stock.column("Fabric", width=150)
        self.tree_fabric_stock.column("Stock", width=100)

        # Create labels for displaying profit loss information
        self.label_profit_loss = tk.Label(self.tab_summary, text="Profit/Loss Information", font=("Arial", 14))
        self.label_profit_loss.grid(row=3, column=0, padx=20, pady=10, sticky="e")

        # Create a table for displaying profit/loss information
        self.tree_profit_loss = ttk.Treeview(self.tab_summary, columns=("Fabric", "Revenue", "Profit/Loss"), show="headings", height=5)
        self.tree_profit_loss.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Define the headings for the profit/loss table
        self.tree_profit_loss.heading("Fabric", text="Fabric")
        self.tree_profit_loss.heading("Revenue", text="Revenue")
        self.tree_profit_loss.heading("Profit/Loss", text="Profit/Loss (₹)")
        
        # Adjust column widths
        self.tree_profit_loss.column("Fabric", width=250)
        self.tree_profit_loss.column("Revenue", width=150)
        self.tree_profit_loss.column("Profit/Loss", width=100)

        # Add date range inputs for selecting the start and end dates
        self.label_start_date = tk.Label(self.tab_summary, text="Start Date (YYYY-MM-DD):", font=("Arial", 12))
        self.label_start_date.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.entry_start_date = tk.Entry(self.tab_summary)
        self.entry_start_date.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.label_end_date = tk.Label(self.tab_summary, text="End Date (YYYY-MM-DD):", font=("Arial", 12))
        self.label_end_date.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.entry_end_date = tk.Entry(self.tab_summary)
        self.entry_end_date.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Button to refresh summary data
        self.btn_refresh_summary = tk.Button(self.tab_summary, text="Refresh", command=self.update_summary)
        self.btn_refresh_summary.grid(row=7, column=0, columnspan=2, pady=20, sticky="nsew")

        # Configure grid to stretch components when the window is resized
        self.tab_summary.grid_rowconfigure(2, weight=1)
        self.tab_summary.grid_rowconfigure(3, weight=1)
        self.tab_summary.grid_rowconfigure(6, weight=1)
        self.tab_summary.grid_columnconfigure(0, weight=1)
        self.tab_summary.grid_columnconfigure(1, weight=1)


    def create_sales_tab(self):
        """Create the sales tab for adding new sales transactions."""
        # Configure grid to center elements and distribute them equally
        self.tab_sales.grid_columnconfigure(0, weight=1)
        self.tab_sales.grid_columnconfigure(1, weight=1)
        self.tab_sales.grid_rowconfigure(0, weight=1)
        self.tab_sales.grid_rowconfigure(1, weight=1)
        tk.Label(self.tab_sales, text="Select Fabric:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.combo_fabrics_sales = ttk.Combobox(self.tab_sales, values=self.get_fabrics_list())
        self.combo_fabrics_sales.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.tab_sales, text="Quantity Sold:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_quantity_sales = tk.Entry(self.tab_sales)
        self.entry_quantity_sales.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.tab_sales, text="Selling Price:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_selling_price = tk.Entry(self.tab_sales)
        self.entry_selling_price.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.btn_add_sale = tk.Button(self.tab_sales, text="Add Sale", command=self.add_sale)
        self.btn_add_sale.grid(row=3, column=0, columnspan=2, pady=20)

        # Create a table for displaying sales information
        self.sales_record_tree = ttk.Treeview(self.tab_sales, columns=("Date", "Fabric", "Quantity","Selling price", "Revenue"), show="headings", height=5)
        self.sales_record_tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Define the headings for the profit/loss table
        self.sales_record_tree.heading("Date", text="Date")
        self.sales_record_tree.heading("Fabric", text="Fabric")
        self.sales_record_tree.heading("Quantity", text="Quantity")
        self.sales_record_tree.heading("Selling price", text="Selling price")
        self.sales_record_tree.heading("Revenue", text="Revenue")
        
        # Adjust column widths
        # self.sales_record_tree.column("Fabric", width=250)
        # self.sales_record_tree.column("Revenue", width=150)
        # self.sales_record_tree.column("Profit/Loss", width=100)

        # Add date range inputs for selecting the start and end dates
        self.label_start_date_sales = tk.Label(self.tab_sales, text="Start Date (YYYY-MM-DD):", font=("Arial", 12))
        self.label_start_date_sales.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.entry_start_date_sales = tk.Entry(self.tab_sales)
        self.entry_start_date_sales.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.label_end_date_sales = tk.Label(self.tab_sales, text="End Date (YYYY-MM-DD):", font=("Arial", 12))
        self.label_end_date_sales.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.entry_end_date_sales = tk.Entry(self.tab_sales)
        self.entry_end_date_sales.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Button to fetch sales data
        self.btn_fetch_sales = tk.Button(self.tab_sales, text="fetch sales", command=self.fetch_sales)
        self.btn_fetch_sales.grid(row=7, column=0, columnspan=2, pady=20, sticky="nsew")


        # Configure grid to stretch components when the window is resized
        self.tab_sales.grid_rowconfigure(2, weight=1)
        self.tab_sales.grid_rowconfigure(3, weight=1)
        self.tab_sales.grid_rowconfigure(6, weight=1)
        self.tab_sales.grid_columnconfigure(0, weight=1)
        self.tab_sales.grid_columnconfigure(1, weight=1)

    def create_purchase_tab(self):
        """Create the purchase tab for adding new purchases."""
        self.tab_purchase.grid_columnconfigure(0, weight=1)
        self.tab_purchase.grid_columnconfigure(1, weight=1)
        self.tab_purchase.grid_rowconfigure(0, weight=1)
        self.tab_purchase.grid_rowconfigure(1, weight=1)
        tk.Label(self.tab_purchase, text="Select Fabric:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="e")

        self.combo_fabrics_purchase = ttk.Combobox(self.tab_purchase, values=self.get_fabrics_list())
        self.combo_fabrics_purchase.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.tab_purchase, text="Quantity Purchased:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_quantity_purchase = tk.Entry(self.tab_purchase)
        self.entry_quantity_purchase.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.tab_purchase, text="Cost Price:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_cost_price = tk.Entry(self.tab_purchase)
        self.entry_cost_price.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.btn_add_purchase = tk.Button(self.tab_purchase, text="Add Purchase", command=self.add_purchase)
        self.btn_add_purchase.grid(row=3, column=0, columnspan=2, pady=20)

        # Create a table for displaying sales information
        self.purchases_record_tree = ttk.Treeview(self.tab_purchase, columns=("Date", "Fabric", "Quantity","Cost price", "Expenditure"), show="headings", height=5)
        self.purchases_record_tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Define the headings for the profit/loss table
        self.purchases_record_tree.heading("Date", text="Date")
        self.purchases_record_tree.heading("Fabric", text="Fabric")
        self.purchases_record_tree.heading("Quantity", text="Quantity")
        self.purchases_record_tree.heading("Cost price", text="Cost price")
        self.purchases_record_tree.heading("Expenditure", text="Expenditure")
        
        # Adjust column widths
        # self.sales_record_tree.column("Fabric", width=250)
        # self.sales_record_tree.column("Revenue", width=150)
        # self.sales_record_tree.column("Profit/Loss", width=100)

        # Add date range inputs for selecting the start and end dates
        self.label_start_date_purchase = tk.Label(self.tab_purchase, text="Start Date (YYYY-MM-DD):", font=("Arial", 12))
        self.label_start_date_purchase.grid(row=5, column=0, padx=10, pady=10, sticky="e")

        self.entry_start_date_purchase = tk.Entry(self.tab_purchase)
        self.entry_start_date_purchase.grid(row=5, column=1, padx=10, pady=10, sticky="w")

        self.label_end_date_purchase = tk.Label(self.tab_purchase, text="End Date (YYYY-MM-DD):", font=("Arial", 12))
        self.label_end_date_purchase.grid(row=6, column=0, padx=10, pady=10, sticky="e")

        self.entry_end_date_purchase = tk.Entry(self.tab_purchase)
        self.entry_end_date_purchase.grid(row=6, column=1, padx=10, pady=10, sticky="w")

        # Button to fetch sales data
        self.btn_fetch_purchases = tk.Button(self.tab_purchase, text="fetch sales", command=self.fetch_purchases)
        self.btn_fetch_purchases.grid(row=7, column=0, columnspan=2, pady=20, sticky="nsew")



        # Configure grid to stretch components when the window is resized
        self.tab_purchase.grid_rowconfigure(2, weight=1)
        self.tab_purchase.grid_rowconfigure(3, weight=1)
        self.tab_purchase.grid_rowconfigure(6, weight=1)
        self.tab_purchase.grid_columnconfigure(0, weight=1)
        self.tab_purchase.grid_columnconfigure(1, weight=1)

    def create_add_fabric_tab(self):
        """Create the tab for adding new fabrics."""
        tk.Label(self.tab_add_fabric, text="Fabric Name:", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.entry_fabric_name = tk.Entry(self.tab_add_fabric)
        self.entry_fabric_name.grid(row=0, column=1, padx=10, pady=10)

        # tk.Label(self.tab_add_fabric, text="stock", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        # self.entry_cost_price_add = tk.Entry(self.tab_add_fabric)
        # self.entry_cost_price_add.grid(row=1, column=1, padx=10, pady=10)

        self.btn_add_fabric = tk.Button(self.tab_add_fabric, text="Add Fabric", command=self.add_fabric)
        self.btn_add_fabric.grid(row=2, column=0, columnspan=2, pady=20)

    def add_fabric(self):
        """Add a new fabric to the database."""
        fabric_name = self.entry_fabric_name.get().strip()
        stock = self.entry_cost_price_add.get().strip()

        if not fabric_name or not stock:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        try:
            stock = float(stock)
            response = self.db_manager.add_fabric(fabric_name, stock)
            print(response)
            if "success" in response:
                messagebox.showinfo("Success", response["success"])
                self.entry_fabric_name.delete(0, tk.END)
                self.entry_cost_price_add.delete(0, tk.END)
            else:
                messagebox.showerror("Error", response["error"])
        except ValueError:
            messagebox.showerror("Error", "Cost Price must be a valid number.")

    # ---- Helper Methods for Sales and Purchases ----
    def get_fabrics_list(self):
        """Get a list of fabrics from the database to populate the combo boxes."""
        self.db_manager.cursor.execute("SELECT fabric_name FROM fabrics")
        fabrics = self.db_manager.cursor.fetchall()
        return [fabric[0] for fabric in fabrics]

    def add_sale(self):
        """Add a new sale to the database and update the stock."""
        fabric_name = self.combo_fabrics_sales.get()
        quantity = float(self.entry_quantity_sales.get())
        selling_price = float(self.entry_selling_price.get())

        try:
            fabric_id = self.db_manager.get_fabric_id(fabric_name)
            if fabric_id is not None:
                self.db_manager.add_sale(fabric_id, quantity, selling_price)
                messagebox.showinfo("Success", "Sale recorded successfully!")
                self.update_summary()
            else:
                messagebox.showerror("Error", "Fabric not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def add_purchase(self):
        """Add a new purchase to the database and update the stock."""
        fabric_name = self.combo_fabrics_purchase.get()
        quantity = float(self.entry_quantity_purchase.get())
        cost_price = float(self.entry_cost_price.get())

        try:
            fabric_id = self.db_manager.get_fabric_id(fabric_name)
            if fabric_id is not None:
                self.db_manager.add_purchase(fabric_id, quantity, cost_price)
                messagebox.showinfo("Success", "Purchase recorded successfully!")
                self.update_summary()
            else:
                messagebox.showerror("Error", "Fabric not found.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---- Update Summary Tab ----
    def update_summary(self):
        """Update the summary information (total stock, profit/loss)."""
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        try:
            selected_fabric = self.combo_fabrics_summary.get()

            if selected_fabric == "All":
                # Show total stock of all fabrics
                total_stock = self.db_manager.get_total_stock()
                profit_loss = self.db_manager.get_total_profit_loss(start_date,end_date)

                # Clear total stock label as individual fabric stocks will be shown
                self.label_stock_value.config(text="")

                # Clear the stock table before inserting new data
                for row in self.tree_fabric_stock.get_children():
                    self.tree_fabric_stock.delete(row)

                # Insert stock data for all fabrics
                all_fabrics_stock = self.db_manager.get_all_fabrics_stock()
                for fabric, stock in all_fabrics_stock:
                    self.tree_fabric_stock.insert("", "end", values=(fabric, stock))

                # Clear the profit/loss table before inserting new data
                for row in self.tree_profit_loss.get_children():
                    self.tree_profit_loss.delete(row)

                # Insert profit/loss data into the table
                total_revenue=0
                total_profit_loss=0
                for pf in profit_loss:
                    total_revenue+=pf[1]
                    total_profit_loss+=pf[2]
                    fabric_name = self.db_manager.get_fabric_name_by_id(pf[0])
                    self.tree_profit_loss.insert("", "end", values=(fabric_name,f'₹{pf[1]:.2f}', f"₹{pf[2]:.2f}"))
                if total_profit_loss!=0 and total_revenue!=0:
                    self.tree_profit_loss.insert("", "end", values=("Total",f'₹{total_revenue:.2f}', f"₹{total_profit_loss:.2f}"))
            else:
                # Get stock and profit/loss for the selected fabric
                fabric_id = self.db_manager.get_fabric_id(selected_fabric)
                fabric_stock = self.db_manager.get_fabric_stock(fabric_id)
                fabric_profit_loss = self.db_manager.get_fabric_profit_loss(fabric_id)

                self.label_stock_value.config(text=f"{fabric_stock} units")

                # Clear the stock and profit/loss tables
                for row in self.tree_fabric_stock.get_children():
                    self.tree_fabric_stock.delete(row)

                for row in self.tree_profit_loss.get_children():
                    self.tree_profit_loss.delete(row)

                # Insert selected fabric's stock and profit/loss into the tables
                self.tree_fabric_stock.insert("", "end", values=(selected_fabric, fabric_stock))
                self.tree_profit_loss.insert("", "end", values=(selected_fabric, f"${fabric_profit_loss:.2f}"))

        except Exception as e:
            messagebox.showerror("Error", str(e))

    def update_fabric_stock(self, event=None):
        """Update the displayed stock based on the selected fabric from the dropdown."""
        selected_fabric = self.combo_fabrics_summary.get()

        try:
            if selected_fabric == "All":
                # Show individual stock for all fabrics
                all_fabrics_stock = self.db_manager.get_all_fabrics_stock()
                self.label_stock_value.config(text="")  # Clear total stock label when showing individual fabrics

                # Clear the table before inserting new data
                for row in self.tree_fabric_stock.get_children():
                    self.tree_fabric_stock.delete(row)

                # Insert stock data for all fabrics into the table
                for fabric, stock in all_fabrics_stock:
                    self.tree_fabric_stock.insert("", "end", values=(fabric, stock))

            else:
                # Get stock for the selected fabric only
                fabric_stock = self.db_manager.get_fabric_stock(selected_fabric)
                self.label_stock_value.config(text=f"{selected_fabric}  :  {fabric_stock} units")

                # Clear the table since only one fabric is selected
                for row in self.tree_fabric_stock.get_children():
                    self.tree_fabric_stock.delete(row)

                # Insert the selected fabric's stock into the table
                self.tree_fabric_stock.insert("", "end", values=(selected_fabric, fabric_stock))

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def fetch_sales(self):
        start_date = self.entry_start_date_sales.get()
        end_date = self.entry_end_date_sales.get()
        try:
                sales_data = self.db_manager.get_sales_data(start_date,end_date)
                # Clear the sales table before inserting new data
                for row in self.sales_record_tree.get_children():
                    self.sales_record_tree.delete(row)

                # Insert profit/loss data into the table
                for sales in sales_data:
                    self.sales_record_tree.insert("", "end", values=(sales[0], sales[1], sales[2], f'₹{sales[3]:.2f}', f"₹{sales[4]:.2f}"))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def fetch_purchases(self):
        start_date = self.entry_start_date_purchase.get()
        end_date = self.entry_end_date_purchase.get()
        try:
                purchase_data = self.db_manager.get_purchase_data(start_date,end_date)
                # Clear the sales table before inserting new data
                for row in self.purchases_record_tree.get_children():
                    self.purchases_record_tree.delete(row)

                # Insert profit/loss data into the table
                for purchases in purchase_data:
                    self.purchases_record_tree.insert("", "end", values=(purchases[0], purchases[1], purchases[2], f'₹{purchases[3]:.2f}', f"₹{purchases[4]:.2f}"))
        except Exception as e:
            messagebox.showerror("Error", str(e))