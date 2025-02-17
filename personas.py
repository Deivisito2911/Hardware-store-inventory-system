class Proveedor:
    def __init__(self, proveedor_id, nombre, contacto, direccion):
        self.proveedor_id = proveedor_id
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion

    def obtener_detalles(self):
        return f"ID: {self.proveedor_id}, Nombre: {self.nombre}, Contacto: {self.contacto}, Dirección: {self.direccion}"

class Cliente:
    def __init__(self, cliente_id, nombre, cedula, contacto, direccion):
        self.cliente_id = cliente_id
        self.nombre = nombre
        self.cedula = cedula
        self.contacto = contacto
        self.direccion = direccion

    def obtener_detalles(self):
        return f"ID: {self.cliente_id}, Nombre: {self.nombre}, Cédula: {self.cedula}, Contacto: {self.contacto}, Dirección: {self.direccion}"