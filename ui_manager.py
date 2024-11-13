import tkinter as tk
from tkinter import ttk, messagebox
from reports import Reports
from search_algo import SearchableComboBox
import  datetime
class UIManager:
    def __init__(self, root, db_manager):
        """Initialize the UIManager with the root Tkinter window and a DBManager instance."""
        self.root = root
        self.db_manager = db_manager
        self.reports = Reports(self,db_manager)
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
        
        self.label_total_stock = tk.Button(self.tab_summary, text="download", font=("Arial", 14), command=self.reports.generate_stock_report)
        self.label_total_stock.grid(row=0, column=1, padx=20, pady=10, sticky="e")

        self.label_stock_value = tk.Label(self.tab_summary, text="", font=("Arial", 14))
        self.label_stock_value.grid(row=0, column=1, padx=20, pady=10, sticky="w")

        # Dropdown (combobox) to select fabric or "All"
        self.label_select_fabric = tk.Label(self.tab_summary, text="Select Fabric:", font=("Arial", 12))
        self.label_select_fabric.grid(row=1, column=0, padx=10, pady=10, sticky="e")

        # Searchable fabric selector instance
        self.fabric_selector_summary = SearchableComboBox(self.tab_summary, self.db_manager,1,1,ALL=True)

        # Create a table for displaying individual fabric stocks (when "All" is selected)
        self.tree_fabric_stock = ttk.Treeview(self.tab_summary, columns=("Id","Fabric", "Stock","Edit"), show="headings", height=5)
        self.tree_fabric_stock.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

        # Define the headings for the stock table
        self.tree_fabric_stock.heading("Id", text="Id")
        self.tree_fabric_stock.heading("Fabric", text="Fabric")
        self.tree_fabric_stock.heading("Stock", text="Stock (units)")
        self.tree_fabric_stock.heading("Edit", text="Edit")
        
        # Adjust column widths
        self.tree_fabric_stock.column("Id", width=150, anchor="center")
        self.tree_fabric_stock.column("Fabric", width=150,anchor="center")
        self.tree_fabric_stock.column("Stock", width=150, anchor="center")
        self.tree_fabric_stock.column("Edit", width=150, anchor="center")

        # Create labels for displaying profit loss information
        self.label_profit_loss = tk.Label(self.tab_summary, text="Profit/Loss Information", font=("Arial", 14))
        self.label_profit_loss.grid(row=3, column=0, padx=20, pady=10, sticky="e")

        self.label_total_stock = tk.Button(self.tab_summary, text="download", font=("Arial", 14), command=self.reports.generate_profit_loss_report)
        self.label_total_stock.grid(row=3, column=1, padx=20, pady=10, sticky="e")

        # Create a table for displaying profit/loss information
        self.tree_profit_loss = ttk.Treeview(self.tab_summary, columns=("Id","Fabric", "Revenue", "Profit/Loss"), show="headings", height=5)
        self.tree_profit_loss.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Define the headings for the profit/loss table
        self.tree_profit_loss.heading("Id", text="Id")
        self.tree_profit_loss.heading("Fabric", text="Fabric")
        self.tree_profit_loss.heading("Revenue", text="Revenue")
        self.tree_profit_loss.heading("Profit/Loss", text="Profit/Loss (₹)")
        
        # Adjust column widths
        self.tree_profit_loss.column("Id", width=150, anchor="center")
        self.tree_profit_loss.column("Fabric", width=150, anchor="center")
        self.tree_profit_loss.column("Revenue", width=150, anchor="center")
        self.tree_profit_loss.column("Profit/Loss", width=150, anchor="center")

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

        # Searchable fabric selector instance
        self.fabric_selector_SALES = SearchableComboBox(self.tab_sales, self.db_manager,0,1)


        tk.Label(self.tab_sales, text="Quantity Sold:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_quantity_sales = tk.Entry(self.tab_sales)
        self.entry_quantity_sales.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.tab_sales, text="Selling Price:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_selling_price = tk.Entry(self.tab_sales)
        self.entry_selling_price.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.btn_add_sale = tk.Button(self.tab_sales, text="Add Sale", command=self.add_sale)
        self.btn_add_sale.grid(row=3, column=0, columnspan=2, pady=20)

        self.label_total_stock = tk.Button(self.tab_sales, text="download", font=("Arial", 14), command=self.reports.generate_sales_report)
        self.label_total_stock.grid(row=3, column=1, padx=20, pady=10, sticky="e")

        # Create a table for displaying sales information
        self.sales_record_tree = ttk.Treeview(self.tab_sales, columns=("Date", "Fabric", "Quantity","Selling price", "Revenue", "Edit"), show="headings", height=5)
        self.sales_record_tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Define the headings for the profit/loss table
        self.sales_record_tree.heading("Date", text="Date")
        self.sales_record_tree.heading("Fabric", text="Fabric")
        self.sales_record_tree.heading("Quantity", text="Quantity")
        self.sales_record_tree.heading("Selling price", text="Selling price")
        self.sales_record_tree.heading("Revenue", text="Revenue")
        self.sales_record_tree.heading("Edit", text="Edit")
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

        self.sales_record_tree.column("Date", anchor="center")
        self.sales_record_tree.column("Fabric", anchor="center")
        self.sales_record_tree.column("Quantity", anchor="center")
        self.sales_record_tree.column("Selling price", anchor="center")
        self.sales_record_tree.column("Revenue", anchor="center")
        self.sales_record_tree.column("Edit", anchor="center")

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

        # Searchable fabric selector instance
        self.fabric_selector_purchase = SearchableComboBox(self.tab_purchase, self.db_manager,0,1)

        tk.Label(self.tab_purchase, text="Quantity Purchased:", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_quantity_purchase = tk.Entry(self.tab_purchase)
        self.entry_quantity_purchase.grid(row=1, column=1, padx=10, pady=10, sticky="w")

        tk.Label(self.tab_purchase, text="Cost Price:", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_cost_price = tk.Entry(self.tab_purchase)
        self.entry_cost_price.grid(row=2, column=1, padx=10, pady=10, sticky="w")

        self.btn_add_purchase = tk.Button(self.tab_purchase, text="Add Purchase", command=self.add_purchase)
        self.btn_add_purchase.grid(row=3, column=0, columnspan=2, pady=20)

        self.label_total_stock = tk.Button(self.tab_purchase, text="download", font=("Arial", 14), command=self.reports.generate_purchases_report)
        self.label_total_stock.grid(row=3, column=1, padx=20, pady=10, sticky="e")

        # Create a table for displaying sales information
        self.purchases_record_tree = ttk.Treeview(self.tab_purchase, columns=("Date", "Fabric", "Quantity","Cost price", "Expenditure","Edit"), show="headings", height=5)
        self.purchases_record_tree.grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

        # Define the headings for the profit/loss table
        self.purchases_record_tree.heading("Date", text="Date")
        self.purchases_record_tree.heading("Fabric", text="Fabric")
        self.purchases_record_tree.heading("Quantity", text="Quantity")
        self.purchases_record_tree.heading("Cost price", text="Cost price")
        self.purchases_record_tree.heading("Expenditure", text="Expenditure")
        self.purchases_record_tree.heading("Edit", text="Edit")

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

        self.purchases_record_tree.column("Date", anchor="center")
        self.purchases_record_tree.column("Fabric", anchor="center")
        self.purchases_record_tree.column("Quantity", anchor="center")
        self.purchases_record_tree.column("Cost price", anchor="center")
        self.purchases_record_tree.column("Expenditure", anchor="center")
        self.purchases_record_tree.column("Edit", anchor="center")

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
        # stock = self.entry_cost_price_add.get().strip()

        if not fabric_name:
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        try:
            stock = float('0')
            response = self.db_manager.add_fabric(fabric_name, stock)
            print(response)
            if "success" in response:
                messagebox.showinfo("Success", response["success"])
                self.fabric_selector_summary.listbox.insert(tk.END,fabric_name)
                self.fabric_selector_SALES.listbox.insert(tk.END,fabric_name)
                self.fabric_selector_purchase.listbox.insert(tk.END,fabric_name)

                self.fabric_selector_summary.options.append(fabric_name)
                self.fabric_selector_SALES.options.append(fabric_name)
                self.fabric_selector_purchase.options.append(fabric_name)

                self.entry_fabric_name.delete(0, tk.END)
                # self.entry_cost_price_add.delete(0, tk.END)
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
        fabric_name = self.fabric_selector_SALES.selected_option
        if fabric_name is None or fabric_name=="":
            messagebox.showerror("Error", "Enter a valid fabric name.")
        try:
            quantity = float(self.entry_quantity_sales.get())
            try:
                selling_price = float(self.entry_selling_price.get())
                try:
                    fabric_id = self.db_manager.get_fabric_id(fabric_name)
                    avl_stock=self.db_manager.get_fabric_stock_by_id(fabric_id)
                    if quantity <= avl_stock:
                        if fabric_id is not None:
                            self.db_manager.add_sale(fabric_id, quantity, selling_price)
                            messagebox.showinfo("Success", "Sale recorded successfully!")
                            self.fabric_selector_SALES.entry.delete(0,tk.END)
                            self.entry_quantity_sales.delete(0,tk.END)
                            self.entry_selling_price.delete(0,tk.END)
                            self.update_summary()
                        else:
                            messagebox.showerror("Error", "Fabric not found.")
                    else:
                        messagebox.showerror("Error", f"Not enough stock to complete the sale.\n available stock:{avl_stock}")
                except Exception as e:
                    messagebox.showerror("Error", str(e)+"raised from here")
            except ValueError:
                messagebox.showerror("Error", "Enter a valid quantity")
        except:
            messagebox.showerror("Error", "Enter a valid selling price")

    def add_purchase(self):
        """Add a new purchase to the database and update the stock."""
        fabric_name = self.fabric_selector_purchase.selected_option
        self.fabric_selector_purchase.selected_option=None
        if fabric_name is None or fabric_name=="":
            messagebox.showinfo("Error", "Enter the fabric name")
            return
        try:
            quantity = float(self.entry_quantity_purchase.get())
            try:
                cost_price = float(self.entry_cost_price.get())
                try:
                    fabric_id = self.db_manager.get_fabric_id(fabric_name)
                    self.fabric_selector_purchase.selected_option=None
                    if fabric_id is not None:
                        self.db_manager.add_purchase(fabric_id, quantity, cost_price)
                        messagebox.showinfo("Success", "Purchase recorded successfully!")
                        self.fabric_selector_purchase.entry.delete(0, tk.END)
                        self.entry_quantity_purchase.delete(0,tk.END)
                        self.entry_cost_price.delete(0,tk.END)
                        self.update_summary()
                    else:
                        messagebox.showerror("Error", "Fabric not found.")
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            except ValueError:
                messagebox.showinfo("Error", "Enter a valid cost price")
        except ValueError:
            messagebox.showinfo("Error", "Enter a valid quantity")

    # ---- Update Summary Tab ----
    def update_summary(self):
        """Update the summary information (total stock, profit/loss)."""
        start_date = self.entry_start_date.get()
        end_date = self.entry_end_date.get()
        try:
            selected_fabric = self.fabric_selector_summary.selected_option
            if selected_fabric == "All":
                # Show total stock of all fabrics
                total_stock = self.db_manager.get_total_stock()
                profit_loss = self.db_manager.get_total_profit_loss(start_date,end_date) if start_date !="" and end_date !="" else []

                # Clear total stock label as individual fabric stocks will be shown
                self.label_stock_value.config(text="")

                # Clear the stock table before inserting new data
                for row in self.tree_fabric_stock.get_children():
                    self.tree_fabric_stock.delete(row)

                # Insert stock data for all fabrics
                all_fabrics_stock = self.db_manager.get_all_fabrics_stock()
                for fabric_id ,fabric_name, stock in all_fabrics_stock:
                    self.tree_fabric_stock.insert("", "end", values=(fabric_id, fabric_name, stock,"Edit"))
                self.tree_fabric_stock.bind("<Button-1>", self.on_treeview_click)
                if len(profit_loss)>0:
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
                        self.tree_profit_loss.insert("", "end", values=(pf[0],fabric_name,f'₹{pf[1]:.2f}', f"₹{pf[2]:.2f}"))
                    if total_profit_loss!=0 and total_revenue!=0:
                        self.tree_profit_loss.insert("", "end", values=("Total","",f'₹{total_revenue:.2f}', f"₹{total_profit_loss:.2f}"))
            else:
                # Get stock and profit/loss for the selected fabric
                selected_fabric = self.fabric_selector_summary.selected_option
                fabric_id = self.db_manager.get_fabric_id(selected_fabric)
                fabric_stock = self.db_manager.get_fabric_stock(selected_fabric)
                profit_loss = self.db_manager.get_total_profit_loss(start_date,end_date) if start_date !="" and end_date !="" else []

                self.label_stock_value.config(text=f"{fabric_stock} units")

                # Clear the stock tables
                for row in self.tree_fabric_stock.get_children():
                    self.tree_fabric_stock.delete(row)
                self.tree_fabric_stock.insert("", "end", values=(fabric_id,selected_fabric, fabric_stock, "Edit"))
                self.tree_fabric_stock.bind("<Button-1>", self.on_treeview_click)

                # Insert selected fabric's stock and profit/loss into the tables
                if len(profit_loss)>0:
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
                        self.tree_profit_loss.insert("", "end", values=(pf[0],fabric_name,f'₹{pf[1]:.2f}', f"₹{pf[2]:.2f}"))
                    if total_profit_loss!=0 and total_revenue!=0:
                        self.tree_profit_loss.insert("", "end", values=("Total","",f'₹{total_revenue:.2f}', f"₹{total_profit_loss:.2f}"))

        except Exception as e:
            messagebox.showerror("Error", str(e)+"raised from summary")
    def on_treeview_click(self, event):
        """Handle the click event on the 'Edit' column."""
        # Get the item under the cursor
        item_id = self.tree_fabric_stock.identify_row(event.y)
        column = self.tree_fabric_stock.identify_column(event.x)

        # Check if the click is on the "Edit" column (adjust column index if needed)
        if column == "#4" and item_id:  # "#4" corresponds to the fourth column (Edit)
            # Extract fabric_id for the selected row and open the edit popup
            fabric_id = self.tree_fabric_stock.item(item_id, "values")[0]  # Assuming 'fabric_id' is the first value
            self.open_edit_popup_fabric(fabric_id)
    def update_fabric_stock(self, event=None):
        """Update the displayed stock based on the selected fabric from the dropdown."""
        selected_fabric = self.fabric_selector_summary.selected_option

        try:
            if selected_fabric == "All":
                # Show individual stock for all fabrics
                all_fabrics_stock = self.db_manager.get_all_fabrics_stock()
                self.label_stock_value.config(text="")  # Clear total stock label when showing individual fabrics

                # Clear the table before inserting new data
                for row in self.tree_fabric_stock.get_children():
                    self.tree_fabric_stock.delete(row)

                # Insert stock data for all fabrics into the table
                for id, fabric, stock in all_fabrics_stock:
                    self.tree_fabric_stock.insert("", "end", values=(id, fabric, stock))

            else:
                # Get stock for the selected fabric only
                fabric_stock = self.db_manager.get_fabric_stock(selected_fabric)
                fabric_id = self.db_manager.get_fabric_id(selected_fabric)
                self.label_stock_value.config(text=f"{selected_fabric}  :  {fabric_stock} meters")

                # Clear the table since only one fabric is selected
                for row in self.tree_fabric_stock.get_children():
                    self.tree_fabric_stock.delete(row)

                # Insert the selected fabric's stock into the table
                self.tree_fabric_stock.insert("", "end", values=(fabric_id ,selected_fabric, fabric_stock))

        except Exception as e:
            messagebox.showerror("Error", str(e))


    def fetch_sales(self):
        start_date = self.entry_start_date_sales.get()
        end_date = self.entry_end_date_sales.get()
        # print(start_date,end_date)
        try:
            # Fetch sales records from the database
            sales_data = self.db_manager.get_sales_data(start_date,end_date)
            # Clear the sales table before inserting new data
            for row in self.sales_record_tree.get_children():
                self.sales_record_tree.delete(row)
            for sale in sales_data:
                sale_id, sale_date, fabric, quantity, selling_price, revenue = sale
                self.sales_record_tree.insert(
                    "", "end", values=(sale_date, fabric, quantity, selling_price, revenue, "Edit"),
                    tags=(sale_id,)
                )
                # Insert "Edit" button directly on row
                self.sales_record_tree.tag_bind(sale_id, '<Button-1>', lambda e, id=sale_id: self.open_edit_popup_sales(id))

        except Exception as e:
            messagebox.showerror("Error", str(e))
    def on_sales_treeview_click(self, event):
        """Handle the click event on the 'Edit' column."""
        # Get the item under the cursor
        print("event has occured")
        print(event)
        item_id = self.tree_fabric_stock.identify_row(event.y)
        column = self.tree_fabric_stock.identify_column(event.x)
        print(item_id,column)

        # Check if the click is on the "Edit" column (adjust column index if needed)
        if column == "#6" and item_id:  # "#4" corresponds to the fourth column (Edit)
            # Extract sale_id for the selected row and open the edit popup
            row_tags = self.sales_record_tree.item(item_id, "tags")  
            self.open_edit_popup_sales(row_tags[0])

    def open_edit_popup_sales(self, sale_id):
        # Create pop-up window
        popup = tk.Toplevel(self.tab_sales)
        popup.title("Edit Sale")
        popup.geometry("400x200")

        # Fetch current data for sale_id
        sale_data = self.db_manager.get_sale_by_id(sale_id)
        _, _, quantity, selling_price, sale_date = sale_data

        # Get the current date as the default
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create fields to edit quantity, selling price, and date
        tk.Label(popup, text="Quantity:").grid(row=0, column=0, padx=10, pady=10)
        entry_quantity = tk.Entry(popup)
        entry_quantity.insert(0, quantity)
        entry_quantity.grid(row=0, column=1)

        tk.Label(popup, text="Selling Price:").grid(row=1, column=0, padx=10, pady=10)
        entry_price = tk.Entry(popup)
        entry_price.insert(0, selling_price)
        entry_price.grid(row=1, column=1)

        tk.Label(popup, text="Sale Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
        entry_date = tk.Entry(popup)

        # Set to current date if sale_date is empty or null
        entry_date.insert(0,current_date)
        entry_date.grid(row=2, column=1)

        # "Save" button to apply updates to the database
        btn_save = tk.Button(popup, text="Save", command=lambda: self.save_sale_edit(sale_id, entry_quantity.get(), entry_price.get(), entry_date.get()))
        btn_save.grid(row=3, column=0, columnspan=2, pady=10)

    def save_sale_edit(self, sale_id, quantity, selling_price, sale_date):
        # Validate and update data in the database
        self.db_manager.update_sale_data(sale_id, quantity, selling_price, sale_date)
        # Refresh the sales table view to reflect updates
        self.fetch_sales()


    def fetch_purchases(self):
        start_date = self.entry_start_date_purchase.get()
        end_date = self.entry_end_date_purchase.get()
        try:
                purchase_data = self.db_manager.get_purchase_data(start_date,end_date)
                # Clear the purchases table before inserting new data
                for row in self.purchases_record_tree.get_children():
                    self.purchases_record_tree.delete(row)
                for purchase in purchase_data :
                    purchase_id, purchase_date, fabric_name, quantity, cost_price, expendicture = purchase
                    self.purchases_record_tree.insert(
                        "", "end", values=(purchase_date,fabric_name, quantity, cost_price, expendicture, "Edit"),
                        tags=(purchase_id,)
                    )
                    # Insert "Edit" button directly on row
                    self.purchases_record_tree.tag_bind(purchase_id, '<Button-1>', lambda e, id=purchase_id: self.open_edit_popup_purchases(id))
        except Exception as e:
            messagebox.showerror("Error", str(e))
    def open_edit_popup_purchases(self, purchase_id):
        # Create pop-up window
        popup = tk.Toplevel(self.tab_purchase)
        popup.title("Edit Purchase")
        popup.geometry("400x200")

        # Fetch current data for purchase_id
        purchase_data = self.db_manager.get_purchase_by_id(purchase_id)
        _, _, quantity, cost_price, purchase_date = purchase_data

        # Get the current date as the default
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Create fields to edit quantity, selling price, and date
        tk.Label(popup, text="Quantity:").grid(row=0, column=0, padx=10, pady=10)
        entry_quantity = tk.Entry(popup)
        entry_quantity.insert(0, quantity)
        entry_quantity.grid(row=0, column=1)

        tk.Label(popup, text="Cost Price:").grid(row=1, column=0, padx=10, pady=10)
        entry_price = tk.Entry(popup)
        entry_price.insert(0, cost_price)
        entry_price.grid(row=1, column=1)

        tk.Label(popup, text="Purchase Date (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=10)
        entry_date = tk.Entry(popup)

        # Set to current date if sale_date is empty or null
        entry_date.insert(0,current_date)
        entry_date.grid(row=2, column=1)
        # "Save" button to apply updates to the database
        btn_save = tk.Button(popup, text="Save", command=lambda: self.save_purchase_edit(purchase_id, entry_quantity.get(), entry_price.get(), entry_date.get(), popup))
        btn_save.grid(row=3, column=0, columnspan=2, pady=10)

    def save_purchase_edit(self, purchase_id, quantity, cost_price, purchase_date,popwin):
        
        # Validate and update data in the database
        res=self.db_manager.update_purchase_data(purchase_id, quantity, cost_price, purchase_date)
        # Refresh the sales table view to reflect updates
        if res:
            messagebox.showinfo("success","updated successfully")
            popwin.destroy()
        else:
            messagebox.showerror("error","error occured while updating")
        self.fetch_purchases()

    def open_edit_popup_fabric(self, fabric_id):

        print("function is called")
        # Create pop-up window
        popup = tk.Toplevel(self.tab_summary)
        popup.title("Edit fabric")
        popup.geometry("400x200")

        # Fetch fabric name for fabric_id
        fabric_name = self.db_manager.get_fabric_name_by_id(fabric_id)

        # Create fields to edit quantity, selling price, and date
        tk.Label(popup, text="Fabric name:").grid(row=0, column=0, padx=10, pady=10)
        entry_fabric_name = tk.Entry(popup)
        entry_fabric_name.insert(0, fabric_name)
        entry_fabric_name.grid(row=0, column=1)

        # "Save" button to apply updates to the database
        btn_save = tk.Button(popup, text="Save", command=lambda: self.save_fabric_name_edit(fabric_id, entry_fabric_name.get(),popup))
        btn_save.grid(row=2, column=0, columnspan=2, pady=10)
    
    def save_fabric_name_edit(self,fabric_id, fabric_name,popwin):
        # Validate and update data in the database
        res=self.db_manager.update_fabric_name(fabric_id, fabric_name)
        # Refresh the sales table view to reflect updates
        if res:
            messagebox.showinfo("success","updated successfully")
            popwin.destroy()
            self.fabric_selector_summary.selected_option=fabric_name
            self.fabric_selector_summary.entry.delete(0,tk.END)
            self.fabric_selector_summary.entry.insert(tk.END,fabric_name)
        else:
            messagebox.showerror("error","error occured while updating")
        self.update_summary()