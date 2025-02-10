import sqlite3
from tkinter import ttk, messagebox 
from producto import Producto  # Importamos la clase Producto del módulo producto.py

# Clase para manejar la base de datos
class BaseDatos:
    def __init__(self):
        # Conexión a la base de datos SQLite
        self.conexion = sqlite3.connect("inventario.db")
        self.cursor = self.conexion.cursor()  # Creación de un cursor para ejecutar consultas SQL
        self.crear_tabla()  # Llamada al método para crear la tabla si no existe

    def crear_tabla(self):
        # Crear tabla de productos si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                producto_id INTEGER PRIMARY KEY,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                precio REAL NOT NULL,
                cantidad_stock INTEGER NOT NULL,
                proveedor TEXT
            )
        ''')

        # Crear tabla de ventas si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS ventas (
                venta_id INTEGER PRIMARY KEY,
                cant_articulos INTEGER NOT NULL,
                medio_pago TEXT NOT NULL,
                total REAL NOT NULL,
                productos TEXT NOT NULL  
            )
        ''')# Guardaremos los IDs de los productos como una cadena separada por comas
        self.conexion.commit()

    def obtener_productos(self):
        self.cursor.execute("SELECT * FROM productos")
        rows = self.cursor.fetchall()  # Obtención de todas las filas resultantes
        return [Producto(*row) for row in rows] # Creación de objetos Producto a partir de las filas y retorno de una lista de productos

    def actualizar_stock_producto(self, producto_id, nueva_cantidad):
        try:
            self.cursor.execute('''
                UPDATE productos SET cantidad_stock=? WHERE producto_id=?
            ''', (nueva_cantidad, producto_id))
            self.conexion.commit()
            print(f"Stock actualizado para producto_id {producto_id}: {nueva_cantidad}")
        except sqlite3.Error as error:
            messagebox.showerror("Error en base de datos", f"No se pudo actualizar el stock del producto: {error}")
            print(f"Error al actualizar el stock: {error}")

    def agregar_venta(self, venta):
        try:
            # Convertir la lista de productos en una cadena de IDs separados por comas
            productos_ids = ",".join([str(p.producto_id) for p in venta.productos])
            
            # Insertar la venta en la tabla de ventas
            self.cursor.execute('''
                INSERT INTO ventas (cant_articulos, medio_pago, total, productos)
                VALUES (?, ?, ?, ?)
            ''', (venta.cant_articulos, venta.medio_pago, venta.total, productos_ids))
            self.conexion.commit()
        except sqlite3.Error as error:
            messagebox.showerror("Error en base de datos", f"No se pudo guardar la venta: {error}")

    def obtener_ventas(self):
        try:
            self.cursor.execute("SELECT * FROM ventas")
            ventas_db = self.cursor.fetchall()
            return ventas_db
        except sqlite3.Error as error:
            messagebox.showerror("Error en base de datos", f"No se pudo obtener las ventas: {error}")
            return []
        
    def agregar_producto(self, producto):
        # Ejecución de la consulta SQL para insertar un nuevo producto en la tabla
        self.cursor.execute('''
            INSERT INTO productos (nombre, descripcion, precio, cantidad_stock, proveedor)
            VALUES (?, ?, ?, ?, ?)
        ''', (producto.nombre, producto.descripcion, producto.precio, producto.cantidad_stock, producto.proveedor))
        self.conexion.commit()  # Confirmación de los cambios en la base de datos

    def eliminar_producto(self, producto):
        self.cursor.execute('''
            DELETE FROM productos WHERE producto_id=?               
        ''', (producto.producto_id,))
        self.conexion.commit()
        
    def actualizar_producto(self, producto):
        try:
            # Ejecutar la consulta SQL para actualizar el producto
            self.cursor.execute('''
                UPDATE productos SET nombre=?, descripcion=?, precio=?, cantidad_stock=?, proveedor=? WHERE producto_id=?
            ''', (producto.nombre, producto.descripcion, producto.precio, producto.cantidad_stock, producto.proveedor, producto.producto_id))
            self.conexion.commit()  # Confirmar los cambios en la base de datos
        except sqlite3.Error as error:
            # Manejar cualquier error de base de datos
            messagebox.showerror("Error en base de datos", f"No se pudo actualizar el producto: {error}")
    
    def buscar_productos_por_nombre(self, nombre):
        try:
            # Consulta SQL para buscar productos por coincidencia de nombre
            self.cursor.execute("SELECT * FROM productos WHERE nombre LIKE ?", ('%' + nombre + '%',))
            productos = self.cursor.fetchall()
            self.conexion.commit()
        except sqlite3.Error as error:
            # Manejar cualquier error de base de datos
            messagebox.showerror("Error en base de datos", f"No se pudo obtener el producto: {error}")
        return productos
    
    def buscar_productos_por_proveedor(self, proveedor):
        try:
            # Consulta SQL para buscar productos por proveedor
            self.cursor.execute("SELECT * FROM productos WHERE proveedor=?", (proveedor,))
            productos = self.cursor.fetchall()
            self.conexion.commit()
        except sqlite3.Error as error:
            # Manejar cualquier error de base de datos
            messagebox.showerror("Error en base de datos", f"No se pudo obtener el producto: {error}")
        return productos

    def buscar_producto_por_id(self, producto_id):
        try:
            # Consulta SQL para buscar un producto por ID
            self.cursor.execute("SELECT * FROM productos WHERE producto_id=?", (producto_id,))
            producto = self.cursor.fetchone()
            self.conexion.commit()
        except sqlite3.Error as error:
            # Manejar cualquier error de base de datos
            messagebox.showerror("Error en base de datos", f"No se pudo obtener el producto: {error}")
        return producto
    
    def cerrar_conexion(self):
        self.conexion.close()  # Cierre de la conexión a la base de datos
