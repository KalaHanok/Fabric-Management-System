class SalesManager:
    def __init__(self, db_manager, calculations):
        """Initialize with a DBManager instance and Calculations instance to manage sales."""
        self.db_manager = db_manager
        self.calculations = calculations

    def record_sale(self, fabric_id, quantity_sold, selling_price_per_unit):
        """
        Record a sale transaction, update stock, and calculate profit or loss.

        Parameters:
        - fabric_id (int): The ID of the fabric being sold.
        - quantity_sold (float): The quantity of fabric sold.
        - selling_price_per_unit (float): The price at which the fabric is sold per unit.

        Returns:
        - dict: Contains success message or error and calculated profit/loss for the transaction.
        """
        try:
            # Get current stock for the fabric
            current_stock = self.db_manager.get_current_stock(fabric_id)
            
            if current_stock is None:
                return {"error": f"Fabric ID {fabric_id} does not exist."}

            # Check if there's enough stock for the sale
            if quantity_sold > current_stock:
                return {"error": "Not enough stock to complete the sale."}

            # Get the average cost price of the fabric
            avg_cost_price_per_unit = self.db_manager.get_avg_cost_price(fabric_id)

            # Calculate total cost and total sales
            total_cost_value = avg_cost_price_per_unit * quantity_sold
            total_sales_value = selling_price_per_unit * quantity_sold

            # Calculate profit or loss for this transaction
            profit_or_loss = total_sales_value - total_cost_value

            # Update stock after the sale
            self.db_manager.update_stock(fabric_id, current_stock - quantity_sold)

            # Record the sale in the sales table
            self.db_manager.record_sale(fabric_id, quantity_sold, selling_price_per_unit, total_sales_value)

            return {
                "success": f"Sale of {quantity_sold} units of fabric ID {fabric_id} recorded successfully.",
                "profit_loss": profit_or_loss
            }

        except Exception as e:
            return {"error": f"Error recording sale: {e}"}

    def get_sales_summary(self, start_date=None, end_date=None):
        """
        Get a summary of all sales within a specified time range.

        Parameters:
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - end_date (str, optional): End date in 'YYYY-MM-DD' format.

        Returns:
        - list: Contains tuples with fabric name, quantity sold, total sales value, and profit/loss.
        """
        try:
            sales_summary = []
            fabrics = self.db_manager.get_all_fabrics()

            for fabric_id, fabric_name in fabrics:
                total_sold, total_sales_value = self.db_manager.get_total_sales(fabric_id, start_date, end_date)
                total_profit_loss = self.calculations.calculate_profit_loss(fabric_id, start_date, end_date)
                sales_summary.append((fabric_name, total_sold, total_sales_value, total_profit_loss))

            return sales_summary

        except Exception as e:
            print(f"Error fetching sales summary: {e}")
            return []

    def get_fabric_sales(self, fabric_id, start_date=None, end_date=None):
        """
        Get sales details for a specific fabric over a given time range.

        Parameters:
        - fabric_id (int): The ID of the fabric.
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - end_date (str, optional): End date in 'YYYY-MM-DD' format.

        Returns:
        - dict: Contains fabric name, total quantity sold, total sales value, and profit/loss.
        """
        try:
            fabric_name = self.db_manager.get_fabric_name(fabric_id)
            total_sold, total_sales_value = self.db_manager.get_total_sales(fabric_id, start_date, end_date)
            total_profit_loss = self.calculations.calculate_profit_loss(fabric_id, start_date, end_date)

            return {
                "fabric_name": fabric_name,
                "total_sold": total_sold,
                "total_sales_value": total_sales_value,
                "profit_loss": total_profit_loss
            }

        except Exception as e:
            return {"error": f"Error fetching fabric sales: {e}"}
