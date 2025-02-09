#Class product
class product:
    def __init__(self, product_id, name, description, price, stock, supplier):
        self.product_id = product_id
        self._name = name
        self._decription = description
        self._price = price
        self._stock = stock
        self._supplier = supplier

    #Name
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, new_name):
        self._name = new_name
    
    #Description
    @property
    def description(self):
        return self._decription
    @description.setter
    def description(self, new_description):
        self._decription = new_description
    
    #Price
    @property
    def stock(self):
        return self._stock
    @stock.setter
    def stock(self, new_stock):
        self._stock = new_stock

    #Supplier
    @property
    def supplier(self):
        return self._supplier
    @stock.setter
    def stock(self, new_supplier):
        self._supplier = new_supplier
    
    #Obtain details
    def obtainDetails(self):
        details = f"ID: {self.product_id}\nName: {self.name}\nDescription: {self.description}\n"
        details += f"Price: {self._price}\nStock: {self.stock}\nSupplier: {self.supplier}"
        return details

