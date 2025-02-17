class Producto:
    def __init__(self, producto_id, nombre, descripcion, precio, cantidad_stock, proveedor_id):
        self.producto_id = producto_id
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.cantidad_stock = cantidad_stock
        self.proveedor_id = proveedor_id

    def obtener_detalles(self):
        return f"ID: {self.producto_id}, Nombre: {self.nombre}, Descripción: {self.descripcion}, Precio: {self.precio}, Stock: {self.cantidad_stock}, Proveedor ID: {self.proveedor_id}"