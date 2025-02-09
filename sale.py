from product import product  #Import class product of module product.py

# Class sale
class sale:
    def _init_(self, sale_id, num_articles, payment_method, total, products):
        self.sale_id = sale_id
        self._num_articles = num_articles
        self._payment_method = payment_method
        self._total = total
        self._products = products

    # Numbers articles
    @property
    def num_articles(self):
        return self._num_articles
    @num_articles.setter
    def num_articles(self, new_num_articles):
        self._num_articles = new_num_articles

    # Payment method
    @property
    def payment_method(self):
        return self._payment_method
    @payment_method.setter
    def payment_method(self, new_payment_method):
        self._payment_method = new_payment_method
    
    # Total 
    @property
    def total(self):
        return self._total
    @total.setter
    def total(self, new_total):
        self._total = new_total
    
    # Products
    @property
    def products(self):
        return self._products
    @products.setter
    def products(self, news_products):
        self._products = news_products

    # Sale obtain
    def obtain_sale(self):
        sale = f"ID: {self.sale_id}\nNumbers articles: {self.num_articles}\nPayment method: {self.payment_method}\n"
        sale += f"Total: {self.total}\nProducts: {self.products}"
        return sale