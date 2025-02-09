# Class sales
class sales:
    def __init__(self):
        self.sales = []

    def add_sale(self, sale):
        self.sales.append(sale)

    def delete_sale(self, sale):
        self.sales = [p for p in self.sales if p.sale_id != sale.sale_id]

    def generate_report_sales(self):
        report = [sale.obtain_sale() for sale in self.sales]
        return report