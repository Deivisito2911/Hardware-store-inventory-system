# Clase Inventary
class Inventary:
    def _init_(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def delete_product(self, product):
        self.products = [p for p in self.products if p.product_id != product.product_id]


    def search_product(self, product_id):
        for product in self.products:
            if product.product_id == product_id:
                return product
        return None

    def generate_report(self):
        report = [product.obtain_details() for product in self.products]
        return report