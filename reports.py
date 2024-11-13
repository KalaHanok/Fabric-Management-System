import csv
import os
import matplotlib.pyplot as plt
import datetime

class Reports:
    def __init__(self, ui_mmanager,db_manager, output_dir='./reports'):
        """Initialize with a DBManager instance and define the output directory for reports."""
        self.ui_manager=ui_mmanager
        self.db_manager = db_manager
        self.output_dir = os.path.join(os.getcwd(),'reports')

        # Create the reports directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        print(self.output_dir)

    def generate_sales_report(self):
        """
        Generate a sales report for the specified time period.

        Parameters:
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - end_date (str, optional): End date in 'YYYY-MM-DD' format.
        - export_to_csv (bool, optional): If True, export the report to a CSV file.

        Returns:
        - report_data (list): List of tuples containing fabric name, quantity sold, and total sales value.
        """
        try:
            report_data = []
            cols=self.ui_manager.sales_record_tree["columns"]
            if len(cols)>0:
                cols=cols[:len(cols)-1]
            if len(cols)>0:
                cols=cols[:len(cols)-1]
            for row in self.ui_manager.sales_record_tree.get_children():
                values=self.ui_manager.sales_record_tree.item(row,"values")
                report_data.append(values[:len(values)-1])
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            report_name=f"sales_report_from_{self.ui_manager.entry_start_date_sales.get()}_to_{self.ui_manager.entry_end_date_sales.get()}_on_{current_date}"
            self.export_to_csv(report_data,cols,report_name)

        except Exception as e:
            print(f"Error generating sales report: {e}")
            return []

    def generate_stock_report(self, export_to_csv=True):
        """
        Generate a report on current stock levels for all fabrics.

        Parameters:
        - export_to_csv (bool, optional): If True, export the report to a CSV file.

        Returns:
        - report_data (list): List of tuples containing fabric name and current stock.
        """
        try:
            report_data = []
            cols=self.ui_manager.tree_fabric_stock["columns"]
            if len(cols)>0:
                cols=cols[:len(cols)-1]
            for row in self.ui_manager.tree_fabric_stock.get_children():
                values=self.ui_manager.tree_fabric_stock.item(row,"values")
                report_data.append(values[:len(values)-1])
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            report_name="stock_report_" + current_date
            self.export_to_csv(report_data,cols,report_name)
        except Exception as e:
            print(f"Error generating stock report: {e}")
    def generate_purchases_report(self):
        try:
            report_data = []
            cols=self.ui_manager.purchases_record_tree["columns"]
            if len(cols)>0:
                cols=cols[:len(cols)-1]
            if len(cols)>0:
                cols=cols[:len(cols)-1]
            for row in self.ui_manager.purchases_record_tree.get_children():
                values=self.ui_manager.purchases_record_tree.item(row,"values")
                report_data.append(values[:len(values)-1])
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            report_name=f"purchases_report_from_{self.ui_manager.entry_start_date_purchase.get()}_to_{self.ui_manager.entry_end_date_purchase.get()}_on_{current_date}"
            self.export_to_csv(report_data,cols,report_name)

        except Exception as e:
            print(f"Error generating sales report: {e}")
            return []

    def generate_profit_loss_report(self, start_date=None, end_date=None, export_to_csv=False):
        """
        Generate a profit/loss report for the specified time period.

        Parameters:
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - end_date (str, optional): End date in 'YYYY-MM-DD' format.
        - export_to_csv (bool, optional): If True, export the report to a CSV file.

        Returns:
        - report_data (list): List of tuples containing fabric name and profit/loss.
        """
        try:
            report_data = []
            cols=self.ui_manager.tree_profit_loss["columns"]
            for row in self.ui_manager.tree_profit_loss.get_children():
                values=self.ui_manager.tree_profit_loss.item(row,"values")
                report_data.append([values[0],values[1],float(values[2][1:]),float(values[3][1:])])
            current_date = datetime.datetime.now().strftime("%Y-%m-%d")
            report_name=f"profit_loss_report_from_{self.ui_manager.entry_start_date.get()}_to_{self.ui_manager.entry_end_date.get()}_on_{current_date}"
            self.export_to_csv(report_data,cols,report_name)

        except Exception as e:
            print(f"Error generating profit/loss report: {e}")
            return []

    def export_to_csv(self, report_data, col_names, report_name, start_date=None, end_date=None):
        """
        Export report data to a CSV file.

        Parameters:
        - report_data (list): Data to export.
        - report_name (str): The base name of the report file.
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - end_date (str, optional): End date in 'YYYY-MM-DD' format.
        """
        try:
            date_range = f"_{start_date}_to_{end_date}" if start_date and end_date else ""
            file_path = os.path.join(self.output_dir, f"{report_name}{date_range}.csv")
            with open(file_path, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(col_names)
                writer.writerows(report_data)

            print(f"Report exported to {file_path}")

        except Exception as e:
            print(f"Error exporting report to CSV: {e}")

    def generate_sales_chart(self, start_date=None, end_date=None):
        """
        Generate a bar chart for sales during the specified time period.

        Parameters:
        - start_date (str, optional): Start date in 'YYYY-MM-DD' format.
        - end_date (str, optional): End date in 'YYYY-MM-DD' format.
        """
        try:
            report_data = self.generate_sales_report(start_date, end_date)
            fabric_names = [data[0] for data in report_data]
            sales_values = [data[2] for data in report_data]

            plt.figure(figsize=(10, 6))
            plt.bar(fabric_names, sales_values, color='blue')
            plt.xlabel('Fabric')
            plt.ylabel('Total Sales Value')
            plt.title(f'Sales from {start_date} to {end_date}' if start_date and end_date else 'Total Sales')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

            # Save and display the chart
            chart_path = os.path.join(self.output_dir, f"sales_chart_{start_date}_to_{end_date}.png")
            plt.savefig(chart_path)
            plt.show()

            print(f"Sales chart saved at {chart_path}")

        except Exception as e:
            print(f"Error generating sales chart: {e}")
