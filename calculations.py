class Calculations:
    def __init__(self, db_manager):
        """Initialize with a DBManager instance to interact with the database."""
        self.db_manager = db_manager

    def calculate_profit_loss(self, fabric_id, start_date=None, end_date=None):
        """
        Calculate profit or loss for a specific fabric over a given time range.
        If no date range is provided, calculate for all time.

        Parameters:
        - fabric_id (int): The fabric for which the profit/loss is to be calculated.
        - start_date (str, optional): The start of the time range (format: 'YYYY-MM-DD').
        - end_date (str, optional): The end of the time range (format: 'YYYY-MM-DD').

        Returns:
        - float: The total profit or loss for the given fabric in the time range.
        """
        try:
            # Get total quantity sold and total selling price in the given time range
            total_sold, total_sales_value = self.db_manager.get_total_sales(fabric_id, start_date, end_date)
            
            # Get total quantity purchased and total cost price in the given time range
            total_purchased, total_cost_value = self.db_manager.get_total_purchases(fabric_id, start_date, end_date)

            # Calculate the profit or loss
            total_profit_loss = total_sales_value - total_cost_value

            return total_profit_loss

        except Exception as e:
            print(f"Error calculating profit/loss: {e}")
            return 0

    def calculate_total_profit_loss(self, start_date=None, end_date=None):
        """
        Calculate the total profit or loss for all fabrics over a given time range.
        If no date range is provided, calculate for all time.

        Parameters:
        - start_date (str, optional): The start of the time range (format: 'YYYY-MM-DD').
        - end_date (str, optional): The end of the time range (format: 'YYYY-MM-DD').

        Returns:
        - float: The total profit or loss for all fabrics in the time range.
        """
        try:
            total_profit_loss = 0

            # Get a list of all fabric IDs
            fabrics = self.db_manager.get_all_fabrics()

            # Calculate the profit/loss for each fabric
            for fabric_id, fabric_name in fabrics:
                fabric_profit_loss = self.calculate_profit_loss(fabric_id, start_date, end_date)
                total_profit_loss += fabric_profit_loss

            return total_profit_loss

        except Exception as e:
            print(f"Error calculating total profit/loss: {e}")
            return 0

    def calculate_projection(self, fabric_id, projected_sales_quantity):
        """
        Calculate a projected profit or loss based on a given projected sales quantity.

        Parameters:
        - fabric_id (int): The fabric for which the projection is being made.
        - projected_sales_quantity (float): The projected quantity of sales.

        Returns:
        - float: The projected profit or loss based on the projected sales quantity.
        """
        try:
            # Get the average selling price and cost price for the fabric
            avg_selling_price = self.db_manager.get_avg_selling_price(fabric_id)
            avg_cost_price = self.db_manager.get_avg_cost_price(fabric_id)

            # Projected profit/loss
            projected_profit_loss = (avg_selling_price - avg_cost_price) * projected_sales_quantity

            return projected_profit_loss

        except Exception as e:
            print(f"Error calculating projection: {e}")
            return 0
