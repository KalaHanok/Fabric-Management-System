class PurchaseManager:
    def __init__(self, db_manager):
        """Initialize with a DBManager instance to manage purchases."""
        self.db_manager = db_manager

    def record_purchase(self, fabric_id, quantity_purchased, cost_price_per_unit):
        """
        Record a purchase transaction and update stock levels.

        Parameters:
        - fabric_id (int): The ID of the fabric being purchased.
        - quantity_purchased (float): The quantity of fabric purchased.
        - cost_price_per_unit (float): The cost price of the fabric per unit.

        Returns:
        - dict: Contains success message or error regarding the purchase transaction.
        """
        try:
            # Check if the fabric exists in the database
            if not self.db_manager.fabric_exists(fabric_id):
                return {"error": f"Fabric ID {fabric_id} does not exist."}

            # Get current stock for the fabric
            current_stock = self.db_manager.get_current_stock(fabric_id)

            # Calculate new stock level
            new_stock_level = current_stock + quantity_purchased

            # Update stock in the database
            self.db_manager.update_stock(fabric_id, new_stock_level)

            # Record the purchase in the database
            self.db_manager.record_purchase(fabric_id, quantity_purchased, cost_price_per_unit)

            return {
                "success": f"Purchase of {quantity_purchased} units of fabric ID {fabric_id} recorded successfully.",
                "new_stock_level": new_stock_level
            }

        except Exception as e:
            return {"error": f"Error recording purchase: {e}"}

    def get_purchase_summary(self, start_date=None, end_date=None):
        """
        Get a summary of all purchases within a specified time range.

        Parameters:
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - end_date (str, optional): End date in 'YYYY-MM-DD' format.

        Returns:
        - list: Contains tuples with fabric name, quantity purchased, and cost price.
        """
        try:
            purchase_summary = []
            fabrics = self.db_manager.get_all_fabrics()

            for fabric_id, fabric_name in fabrics:
                total_purchased, total_cost_value = self.db_manager.get_total_purchases(fabric_id, start_date, end_date)
                purchase_summary.append((fabric_name, total_purchased, total_cost_value))

            return purchase_summary

        except Exception as e:
            print(f"Error fetching purchase summary: {e}")
            return []

    def get_fabric_purchase(self, fabric_id, start_date=None, end_date=None):
        """
        Get purchase details for a specific fabric over a given time range.

        Parameters:
        - fabric_id (int): The ID of the fabric.
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - end_date (str, optional): End date in 'YYYY-MM-DD' format.

        Returns:
        - dict: Contains fabric name, total quantity purchased, and total cost.
        """
        try:
            fabric_name = self.db_manager.get_fabric_name(fabric_id)
            total_purchased, total_cost_value = self.db_manager.get_total_purchases(fabric_id, start_date, end_date)

            return {
                "fabric_name": fabric_name,
                "total_purchased": total_purchased,
                "total_cost": total_cost_value
            }

        except Exception as e:
            return {"error": f"Error fetching fabric purchase: {e}"}
