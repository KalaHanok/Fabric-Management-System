import csv
import os
import matplotlib.pyplot as plt
from datetime import datetime

class Reports:
    def __init__(self, db_manager, output_dir='reports'):
        """Initialize with a DBManager instance and define the output directory for reports."""
        self.db_manager = db_manager
        self.output_dir = output_dir

        # Create the reports directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def generate_sales_report(self, start_date=None, end_date=None, export_to_csv=False):
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
            fabrics = self.db_manager.get_all_fabrics()

            for fabric_id, fabric_name in fabrics:
                total_sold, total_sales_value = self.db_manager.get_total_sales(fabric_id, start_date, end_date)
                report_data.append((fabric_name, total_sold, total_sales_value))

            if export_to_csv:
                self.export_to_csv(report_data, 'sales_report', start_date, end_date)

            return report_data

        except Exception as e:
            print(f"Error generating sales report: {e}")
            return []

    def generate_stock_report(self, export_to_csv=False):
        """
        Generate a report on current stock levels for all fabrics.

        Parameters:
        - export_to_csv (bool, optional): If True, export the report to a CSV file.

        Returns:
        - report_data (list): List of tuples containing fabric name and current stock.
        """
        try:
            report_data = []
            fabrics = self.db_manager.get_all_fabrics()

            for fabric_id, fabric_name in fabrics:
                current_stock = self.db_manager.get_current_stock(fabric_id)
                report_data.append((fabric_name, current_stock))

            if export_to_csv:
                self.export_to_csv(report_data, 'stock_report')

            return report_data

        except Exception as e:
            print(f"Error generating stock report: {e}")
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
            fabrics = self.db_manager.get_all_fabrics()

            for fabric_id, fabric_name in fabrics:
                total_profit_loss = self.db_manager.calculate_profit_loss(fabric_id, start_date, end_date)
                report_data.append((fabric_name, total_profit_loss))

            if export_to_csv:
                self.export_to_csv(report_data, 'profit_loss_report', start_date, end_date)

            return report_data

        except Exception as e:
            print(f"Error generating profit/loss report: {e}")
            return []

    def export_to_csv(self, report_data, report_name, start_date=None, end_date=None):
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
                writer.writerow(['Fabric Name', 'Quantity/Amount', 'Value'])
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
