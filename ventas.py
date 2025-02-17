
class Ventas:
    def __init__(self):
        self.ventas = []

    def agregar_venta(self, venta):
        self.ventas.append(venta)

    def eliminar_venta(self, venta):
        self.ventas = [p for p in self.ventas if p.venta_id != venta.venta_id]

    def generar_informe_ventas(self, base_datos):
        informe = []
        for venta in self.ventas:
            cliente = base_datos.buscar_cliente_por_id(venta.cliente_id)  # Obtener los datos del cliente
            if cliente:
                cedula_cliente = cliente[2]  # Suponiendo que la cédula está en el índice 2
                nombre_cliente = cliente[1]  # Suponiendo que el nombre está en el índice 1
            else:
                cedula_cliente = "No registrado"
                nombre_cliente = "No registrado"

            venta_info = f"ID: {venta.venta_id}\nCantidad de artículos: {venta.cant_articulos}\nMedio de pago: {venta.medio_pago}\n"
            venta_info += f"Total: {venta.total}\nProductos: {', '.join([p.nombre for p in venta.productos])}\n"
            venta_info += f"Cliente: {nombre_cliente} (Cédula: {cedula_cliente})"
            informe.append(venta_info)
        return informe