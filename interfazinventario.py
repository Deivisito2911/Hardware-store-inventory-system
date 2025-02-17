import tkinter as tk
from tkinter import ttk, messagebox 
import time
from bdd import BaseDatos  
from inventario import Inventario 
from producto import Producto  
from venta import Venta  
from ventas import Ventas
from personas import Proveedor, Cliente

class InterfazInventario:
    def __init__(self, root):
        # Inicialización de la clase BaseDatos para manejar la base de datos
        self.base_datos = BaseDatos()
        # Inicialización de la clase Inventario para manejar el inventario de productos
        self.inventario = Inventario()
        # Crea una lista de Ventas
        self.ventas = Ventas()
        # Carga de los productos desde la base de datos al inventario
        self.cargar_productos_desde_db()
        

        # Configuración de la ventana principal de la aplicación
        self.root = root
        self.root.title("Sistema de Gestión de Inventarios")
        self.root.geometry("800x450")

        # Configuración del notebook para mostrar pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Creación de las pestañas "Agregar Producto" , "Modificar Producto" , etc
        self.pagina_agregar = ttk.Frame(self.notebook)
        self.pagina_modificar = ttk.Frame(self.notebook)
        self.pagina_estadisticas = ttk.Frame(self.notebook)
        self.pagina_ventas = ttk.Frame(self.notebook)
        self.notebook.add(self.pagina_agregar, text='Agregar Producto')
        self.notebook.add(self.pagina_modificar, text='Modificar Producto')
        self.notebook.add(self.pagina_estadisticas, text='Estadisticas')
        self.notebook.add(self.pagina_ventas, text='Ventas')

        # Crear nuevas pestaña clientes
        self.pagina_clientes = ttk.Frame(self.notebook)
        self.notebook.add(self.pagina_clientes, text='Clientes')

        # Crear interfaces para clientes
        self.crear_interfaz_clientes()

        # Crear la pestaña de proveedores
        self.pagina_proveedores = ttk.Frame(self.notebook)
        self.notebook.add(self.pagina_proveedores, text='Proveedores')
        self.crear_interfaz_proveedores()

        # Creación de la interfaz para agregar un nuevo producto
        self.crear_interfaz_agregar_producto()
        # Creación de la interfaz para modificar un producto existente
        self.crear_interfaz_modificar_producto()
        # Creación del botón para eliminar un producto
        self.crear_boton_eliminar_producto()  # Llamar a la función aquí
        # Creación del botón para mostrar el informe de inventarios
        self.crear_boton_mostrar_informe()
        # Creación de la interfaz de estadísticas
        self.crear_interfaz_estadisticas()
        #Creación de la interfaz para cargar nueva venta
        self.crear_interfaz_agregar_venta()
        #Creación del botón para mostrar ventas
        self.crear_boton_mostrar_ventas()
        
    def crear_interfaz_proveedores(self):
        # Combobox para seleccionar proveedores (Pestaña Proveedores)
        tk.Label(self.pagina_proveedores, text="Seleccionar Proveedor", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.combo_proveedores_proveedores = ttk.Combobox(self.pagina_proveedores, font=("Arial", 12))  # Nombre distinto
        self.combo_proveedores_proveedores.grid(row=0, column=1, padx=10, pady=5)
        self.combo_proveedores_proveedores.bind("<<ComboboxSelected>>", lambda event: self.cargar_datos_proveedor_seleccionado(event, self.combo_proveedores_proveedores))  # Pasa el combobox
        self.actualizar_lista_proveedores(self.combo_proveedores_proveedores)  # Pasar el combobox

        # Campos para agregar/modificar proveedores
        etiquetas_proveedor = ["Nombre", "Contacto", "Dirección"]
        self.entries_proveedor = {}
        for i, etiqueta in enumerate(etiquetas_proveedor):
            tk.Label(self.pagina_proveedores, text=etiqueta, font=("Arial", 12)).grid(row=i + 1, column=0, padx=10, pady=5)
            entry = tk.Entry(self.pagina_proveedores, font=("Arial", 12))
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            self.entries_proveedor[etiqueta] = entry

        # Botones para agregar, modificar y eliminar proveedores
        self.boton_agregar_proveedor = tk.Button(self.pagina_proveedores, text="Agregar Proveedor", command=lambda: self.agregar_proveedor(self.combo_proveedores_proveedores), font=("Arial", 12), bg="#4CAF50", fg="white")
        self.boton_agregar_proveedor.grid(row=len(etiquetas_proveedor) + 1, column=0, pady=10)

        self.boton_modificar_proveedor = tk.Button(self.pagina_proveedores, text="Modificar Proveedor", command=lambda: self.modificar_proveedor(self.combo_proveedores_proveedores), font=("Arial", 12), bg="#008CBA", fg="white")
        self.boton_modificar_proveedor.grid(row=len(etiquetas_proveedor) + 1, column=1, pady=10)

        self.boton_eliminar_proveedor = tk.Button(self.pagina_proveedores, text="Eliminar Proveedor", command=lambda: self.eliminar_proveedor(self.combo_proveedores_proveedores), font=("Arial", 12), bg="#FF5733", fg="white")
        self.boton_eliminar_proveedor.grid(row=len(etiquetas_proveedor) + 2, column=0, columnspan=2, pady=10)

    def crear_interfaz_clientes(self):
        etiquetas_cliente = ["Nombre", "Cédula", "Contacto", "Dirección"]
        self.entries_cliente = {}
        for i, etiqueta in enumerate(etiquetas_cliente):
            tk.Label(self.pagina_clientes, text=etiqueta, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.pagina_clientes, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries_cliente[etiqueta] = entry

        self.boton_agregar_cliente = tk.Button(self.pagina_clientes, text="Agregar Cliente", command=self.agregar_cliente, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.boton_agregar_cliente.grid(row=len(etiquetas_cliente) + 1, column=0, columnspan=2, pady=10)

    def crear_interfaz_agregar_producto(self):
        etiquetas_agregar = ["Nombre del Producto", "Descripción", "Precio", "Stock", "Proveedor"]
        self.entries_agregar = {}
        for i, etiqueta in enumerate(etiquetas_agregar[:-1]):  # Excluir "Proveedor" de los campos de entrada
            tk.Label(self.pagina_agregar, text=etiqueta, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.pagina_agregar, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries_agregar[etiqueta] = entry

        # Combobox para seleccionar proveedores (Pestaña Agregar Producto)
        tk.Label(self.pagina_agregar, text="Proveedor", font=("Arial", 12)).grid(row=len(etiquetas_agregar) - 1, column=0, padx=10, pady=5)
        self.combo_proveedores_agregar = ttk.Combobox(self.pagina_agregar, font=("Arial", 12))  # Nombre distinto
        self.combo_proveedores_agregar.grid(row=len(etiquetas_agregar) - 1, column=1, padx=10, pady=5)
        self.actualizar_lista_proveedores(self.combo_proveedores_agregar)  # Pasar el combobox
        self.combo_proveedores_agregar.bind("<<ComboboxSelected>>", lambda event: self.cargar_datos_proveedor_seleccionado(event, self.combo_proveedores_agregar))  # Pasa el combobox
        
        # Botón para agregar un nuevo proveedor
        self.boton_agregar_proveedor = tk.Button(self.pagina_agregar, text="Agregar Nuevo Proveedor", command=self.mostrar_ventana_agregar_proveedor, font=("Arial", 12), bg="#008CBA", fg="white")
        self.boton_agregar_proveedor.grid(row=len(etiquetas_agregar), column=0, columnspan=2, pady=10)

        # Botón para agregar el producto
        self.boton_agregar = tk.Button(self.pagina_agregar, text="Agregar Producto", command=lambda: self.agregar_producto(self.combo_proveedores_agregar), font=("Arial", 12), bg="#4CAF50", fg="white")  # Pasa el combobox
        self.boton_agregar.grid(row=len(etiquetas_agregar) + 1, column=0, columnspan=2, pady=10)

    def crear_interfaz_modificar_producto(self):
        etiquetas_modificar = ["Seleccione Producto:", "Nombre del Producto", "Descripción", "Precio", "Stock", "Proveedor"]
        self.combo_modificar = ttk.Combobox(self.pagina_modificar, values=["Seleccionar"] + [producto.nombre for producto in self.inventario.productos], font=("Arial", 12))
        self.combo_modificar.grid(row=0, column=1, padx=10, pady=5)
        self.combo_modificar.set("Seleccionar")
        self.combo_modificar.bind("<<ComboboxSelected>>", self.actualizar_datos_producto_seleccionado)
        self.entries_modificar = {}
        for i, etiqueta in enumerate(etiquetas_modificar[1:]):  # Excluir "Seleccione Producto:"
            tk.Label(self.pagina_modificar, text=etiqueta, font=("Arial", 12)).grid(row=i + 1, column=0, padx=10, pady=5)
            entry = tk.Entry(self.pagina_modificar, font=("Arial", 12))
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            self.entries_modificar[etiqueta] = entry

        # Combobox para seleccionar proveedores
        tk.Label(self.pagina_modificar, text="Proveedor", font=("Arial", 12)).grid(row=len(etiquetas_modificar), column=0, padx=10, pady=5)
        self.combo_proveedores_modificar = ttk.Combobox(self.pagina_modificar, font=("Arial", 12))
        self.combo_proveedores_modificar.grid(row=len(etiquetas_modificar), column=1, padx=10, pady=5)
        self.actualizar_lista_proveedores_modificar()  # Cargar proveedores existentes

        # Botón para modificar el producto
        self.boton_modificar = tk.Button(self.pagina_modificar, text="Modificar Producto", command=self.modificar_producto, font=("Arial", 12), bg="#008CBA", fg="white")
        self.boton_modificar.grid(row=len(etiquetas_modificar) + 1, column=0, columnspan=2, pady=10)

    def crear_interfaz_estadisticas(self):
        total_productos_distintos = len(self.inventario.productos)
        total_productos = sum(producto.cantidad_stock for producto in self.inventario.productos)
        valor_total_inventario = sum(producto.precio * producto.cantidad_stock for producto in self.inventario.productos)
        precio_promedio = valor_total_inventario / total_productos if total_productos > 0 else 0
        
        # Crear etiquetas para mostrar las estadísticas
        etiquetas_estadisticas = [
            f"Cantidad productos distintos: {total_productos_distintos}",
            f"Cantidad Total de Productos: {total_productos}",
            f"Valor Total del Inventario: ${valor_total_inventario:.2f}",
            f"Precio Promedio de Productos: ${precio_promedio:.2f}"
        ]

        # Colocar las etiquetas en la página de estadísticas
        for i, etiqueta in enumerate(etiquetas_estadisticas):
            tk.Label(self.pagina_estadisticas, text=etiqueta, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky='nsew')
        
        # Programar la próxima actualización de las estadísticas en 1 segundo
        self.root.after(1000, self.crear_interfaz_estadisticas)

    def crear_interfaz_agregar_venta(self):
        # Etiquetas y campos de entrada
        etiquetas_agregar = ["Seleccionar Producto", "Cantidad", "Medio de Pago", "Total"]
        self.entries_agregar_ventas = {}

        # Campo para la cédula del cliente
        tk.Label(self.pagina_ventas, text="Cédula del Cliente", font=("Arial", 12)).grid(row=4, column=0, padx=10, pady=5)
        self.entry_cedula_cliente = tk.Entry(self.pagina_ventas, font=("Arial", 12))
        self.entry_cedula_cliente.grid(row=4, column=1, padx=10, pady=5)

        # Botón para buscar cliente por cédula
        self.boton_buscar_cliente = tk.Button(self.pagina_ventas, text="Buscar Cliente", command=self.buscar_cliente_por_cedula, font=("Arial", 12), bg="#008CBA", fg="white")
        self.boton_buscar_cliente.grid(row=4, column=2, padx=10, pady=5)

        # Campo para mostrar el nombre del cliente
        tk.Label(self.pagina_ventas, text="Nombre del Cliente", font=("Arial", 12)).grid(row=5, column=0, padx=10, pady=5)
        self.entry_nombre_cliente = tk.Entry(self.pagina_ventas, font=("Arial", 12), state="readonly")
        self.entry_nombre_cliente.grid(row=5, column=1, padx=10, pady=5)

        # Combobox para seleccionar productos
        tk.Label(self.pagina_ventas, text="Seleccionar Producto", font=("Arial", 12)).grid(row=0, column=0, padx=10, pady=5)
        self.combo_productos = ttk.Combobox(self.pagina_ventas, font=("Arial", 12))
        self.combo_productos.grid(row=0, column=1, padx=10, pady=5)
        self.combo_productos.bind("<<ComboboxSelected>>", self.actualizar_precio_venta)
        self.combo_productos.bind("<KeyRelease>", self.filtrar_productos)

        # Cargar la lista de productos al iniciar
        self.actualizar_lista_productos()

        # Campo para la cantidad
        tk.Label(self.pagina_ventas, text=etiquetas_agregar[1], font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5)
        self.entry_cantidad = tk.Entry(self.pagina_ventas, font=("Arial", 12))
        self.entry_cantidad.grid(row=1, column=1, padx=10, pady=5)
        self.entry_cantidad.bind("<KeyRelease>", self.actualizar_precio_venta)

        # Campo para el medio de pago
        tk.Label(self.pagina_ventas, text=etiquetas_agregar[2], font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5)
        self.entry_medio_pago = tk.Entry(self.pagina_ventas, font=("Arial", 12))
        self.entry_medio_pago.grid(row=2, column=1, padx=10, pady=5)

        # Campo para el total (solo lectura)
        tk.Label(self.pagina_ventas, text=etiquetas_agregar[3], font=("Arial", 12)).grid(row=3, column=0, padx=10, pady=5)
        self.entry_total = tk.Entry(self.pagina_ventas, font=("Arial", 12), state="readonly")
        self.entry_total.grid(row=3, column=1, padx=10, pady=5)

        # Botón para agregar la venta
        self.boton_agregar = tk.Button(self.pagina_ventas, text="Agregar Venta", command=self.agregar_venta, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.boton_agregar.grid(row=6, column=0, columnspan=3, pady=10)  # Ajustar la fila y el columnspan
        # Cargar la lista de productos en el Combobox
        self.actualizar_lista_productos()

    def crear_boton_eliminar_producto(self):
        self.boton_eliminar = tk.Button(self.pagina_modificar, text="Eliminar Producto", command=self.eliminar_producto, font=("Arial", 12), bg="#FF5733", fg="white")
        self.boton_eliminar.grid(row=8, column=0, columnspan=2, pady=10)

    def crear_boton_mostrar_ventas(self):
        self.boton_mostrar_informe = tk.Button(self.root, text="Mostrar Ventas", command=self.mostrar_ventas, font=("Arial", 12), bg="#333", fg="white")
        self.boton_mostrar_informe.pack(pady=10)

    def crear_boton_mostrar_informe(self):
        self.boton_mostrar_informe = tk.Button(self.root, text="Mostrar Informe", command=self.mostrar_informe, font=("Arial", 12), bg="#333", fg="white")
        self.boton_mostrar_informe.pack(pady=10)

    def agregar_proveedor(self, combobox):
        try:
            nombre = self.entries_proveedor["Nombre"].get()
            contacto = self.entries_proveedor["Contacto"].get()
            direccion = self.entries_proveedor["Dirección"].get()
            proveedor = Proveedor(None, nombre, contacto, direccion)
            self.base_datos.agregar_proveedor(proveedor)
            messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")

            # Actualizar la lista de proveedores en todas las pestañas
            self.actualizar_lista_proveedores(self.combo_proveedores_proveedores)  # Actualiza el combobox de proveedores
            self.actualizar_lista_proveedores(self.combo_proveedores_agregar)  # Actualiza el combobox de agregar producto
            self.actualizar_lista_proveedores_modificar() # Actualiza el combobox de modificar producto

            # Limpiar los campos de entrada
            self.entries_proveedor["Nombre"].delete(0, tk.END)
            self.entries_proveedor["Contacto"].delete(0, tk.END)
            self.entries_proveedor["Dirección"].delete(0, tk.END)

        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos para el proveedor.")

    def agregar_cliente(self):
        try:
            nombre = self.entries_cliente["Nombre"].get()
            cedula = self.entries_cliente["Cédula"].get()
            contacto = self.entries_cliente["Contacto"].get()
            direccion = self.entries_cliente["Dirección"].get()
            cliente = Cliente(None, nombre, cedula, contacto, direccion)
            self.base_datos.agregar_cliente(cliente)
            messagebox.showinfo("Éxito", "Cliente agregado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos para el cliente.")

    def agregar_venta(self):
        try:
            producto_seleccionado = self.combo_productos.get()
            cantidad = int(self.entry_cantidad.get())
            medio_pago = self.entry_medio_pago.get()
            total = float(self.entry_total.get())
            cedula_cliente = self.entry_cedula_cliente.get()

            # Buscar el cliente por cédula
            cliente = self.base_datos.buscar_cliente_por_cedula(cedula_cliente)
            if not cliente:
                messagebox.showerror("Error", "Cliente no registrado.")
                return

            producto = next((p for p in self.inventario.productos if p.nombre == producto_seleccionado), None)
            if producto:
                if producto.cantidad_stock < cantidad:
                    messagebox.showerror("Error", "No hay suficiente stock para realizar la venta.")
                    return

                # Crear la venta con el cliente_id
                venta = Venta(len(self.ventas.ventas) + 1, cantidad, medio_pago, total, [producto], cliente[0])
                
                # Guardar la venta en la lista de ventas
                self.ventas.agregar_venta(venta)
                
                # Guardar la venta en la base de datos
                self.base_datos.agregar_venta(venta)

                # Actualizar el stock del producto
                nuevo_stock = producto.cantidad_stock - cantidad
                self.base_datos.actualizar_stock_producto(producto.producto_id, nuevo_stock)
                
                # Actualizar el objeto producto en la lista de inventario
                producto.cantidad_stock = nuevo_stock

                messagebox.showinfo("Éxito", "Venta agregada correctamente.")
            else:
                messagebox.showerror("Error", "Seleccione un producto válido.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos para la venta.")

    def agregar_producto(self,combobox):
        try:
            nombre = self.entries_agregar["Nombre del Producto"].get()
            descripcion = self.entries_agregar["Descripción"].get()
            precio = float(self.entries_agregar["Precio"].get())
            stock = int(self.entries_agregar["Stock"].get())
            proveedor_nombre = combobox.get()  # Usa el combobox que se pasó como argumento

            # Buscar el ID del proveedor por su nombre
            proveedores = self.base_datos.obtener_proveedores()
            proveedor_id = next((proveedor[0] for proveedor in proveedores if proveedor[1] == proveedor_nombre), None)

            if not proveedor_id:
                messagebox.showerror("Error", "Seleccione un proveedor válido.")
                return

            producto = Producto(len(self.inventario.productos) + 1, nombre, descripcion, precio, stock, proveedor_id)
            self.inventario.agregar_producto(producto)
            self.base_datos.agregar_producto(producto)

            # Actualizar los combobox de productos
            self.combo_modificar["values"] = ["Seleccionar"] + [p.nombre for p in self.inventario.productos]
            self.actualizar_lista_productos()

            # Limpiar los campos de entrada
            self.entries_agregar["Nombre del Producto"].delete(0, tk.END)
            self.entries_agregar["Descripción"].delete(0, tk.END)
            self.entries_agregar["Precio"].delete(0, tk.END)
            self.entries_agregar["Stock"].delete(0, tk.END)

            messagebox.showinfo("Éxito", "Producto agregado correctamente.")
        except ValueError:
            messagebox.showerror("Error", "Ingrese datos válidos para el producto.")

    def cargar_productos_desde_db(self):
        # Cargar productos
        productos_db = self.base_datos.obtener_productos()
        self.inventario.productos = productos_db

        # Cargar ventas
        ventas_db = self.base_datos.obtener_ventas()
        for venta in ventas_db:
            venta_id, cant_articulos, medio_pago, total, productos_ids, cliente_id = venta  # Asegúrate de incluir cliente_id
            productos = [self.inventario.buscar_producto(int(id)) for id in productos_ids.split(",")]
            productos = [p for p in productos if p is not None]  # Filtrar productos no encontrados
            venta = Venta(venta_id, cant_articulos, medio_pago, total, productos, cliente_id)  # Pasar cliente_id
            self.ventas.agregar_venta(venta)     

    def cargar_datos_proveedor_seleccionado(self, event, combobox):  # Añade el parámetro combobox
        selected_proveedor = combobox.get()  # Usa el combobox que se pasó como argumento
        print(f"Proveedor seleccionado: {selected_proveedor}")

        if selected_proveedor != "Seleccionar":
            proveedores = self.base_datos.obtener_proveedores()
            proveedor = next((p for p in proveedores if p[1] == selected_proveedor), None)
            if proveedor:
                # ... (resto del código para rellenar los entries)
                self.entries_proveedor["Nombre"].delete(0, tk.END)
                self.entries_proveedor["Nombre"].insert(0, proveedor[1])
                self.entries_proveedor["Contacto"].delete(0, tk.END)
                self.entries_proveedor["Contacto"].insert(0, proveedor[2])
                self.entries_proveedor["Dirección"].delete(0, tk.END)
                self.entries_proveedor["Dirección"].insert(0, proveedor[3])
            else:
                print("Proveedor no encontrado en la lista.")
        else:
            print("Ningún proveedor seleccionado.")
        
    def mostrar_ventas(self):
        informe = self.ventas.generar_informe_ventas(self.base_datos)  # Pasar base_datos
        mensaje = "\n\n".join(informe)

        # Crear una ventana secundaria para mostrar el informe
        ventana_informe = tk.Toplevel(self.root)
        ventana_informe.title("Informe de Ventas")
        
        # Crear un frame para contener el mensaje con desplazamiento
        frame_mensaje = tk.Frame(ventana_informe)
        frame_mensaje.pack(fill="both", expand=True)

        # Crear un scrollbar para desplazarse verticalmente
        scrollbar = ttk.Scrollbar(frame_mensaje, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Crear un Text widget para mostrar el mensaje
        txt_informe = tk.Text(frame_mensaje, yscrollcommand=scrollbar.set)
        txt_informe.pack(fill="both", expand=True)
        txt_informe.insert("1.0", mensaje)

        # Configurar el scrollbar para controlar el desplazamiento del Text widget
        scrollbar.config(command=txt_informe.yview)

    def mostrar_ventana_agregar_proveedor(self):
        ventana_proveedor = tk.Toplevel(self.root)
        ventana_proveedor.title("Agregar Nuevo Proveedor")

        etiquetas_proveedor = ["Nombre", "Contacto", "Dirección"]
        entries_proveedor = {}
        for i, etiqueta in enumerate(etiquetas_proveedor):
            tk.Label(ventana_proveedor, text=etiqueta, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(ventana_proveedor, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            entries_proveedor[etiqueta] = entry

        def guardar_proveedor():
            try:
                nombre = entries_proveedor["Nombre"].get()
                contacto = entries_proveedor["Contacto"].get()
                direccion = entries_proveedor["Dirección"].get()
                proveedor = Proveedor(None, nombre, contacto, direccion)
                self.base_datos.agregar_proveedor(proveedor)

                # Actualizar la lista de proveedores en todas las pestañas
                self.actualizar_lista_proveedores(self.combo_proveedores_proveedores)  # Actualiza el combobox de proveedores
                self.actualizar_lista_proveedores(self.combo_proveedores_agregar)  # Actualiza el combobox de agregar producto
                self.actualizar_lista_proveedores_modificar() # Actualiza el combobox de modificar producto

                messagebox.showinfo("Éxito", "Proveedor agregado correctamente.")
                ventana_proveedor.destroy()

                # Limpiar los campos de entrada
                self.entries_proveedor["Nombre"].delete(0, tk.END)
                self.entries_proveedor["Contacto"].delete(0, tk.END)
                self.entries_proveedor["Dirección"].delete(0, tk.END)


            except ValueError:
                messagebox.showerror("Error", "Ingrese datos válidos para el proveedor.")

        boton_guardar = tk.Button(ventana_proveedor, text="Guardar Proveedor", command=guardar_proveedor, font=("Arial", 12), bg="#4CAF50", fg="white") # No se pasa el combobox aqui
        boton_guardar.grid(row=len(etiquetas_proveedor), column=0, columnspan=2, pady=10)

    def mostrar_informe(self):
        informe = self.inventario.generar_informe()
        mensaje = "\n\n".join(informe)

        # Crear una ventana secundaria para mostrar el informe
        ventana_informe = tk.Toplevel(self.root)
        ventana_informe.title("Informe de Inventarios")
        
        # Crear un frame para contener el mensaje con desplazamiento
        frame_mensaje = tk.Frame(ventana_informe)
        frame_mensaje.pack(fill="both", expand=True)

        # Crear un scrollbar para desplazarse verticalmente
        scrollbar = ttk.Scrollbar(frame_mensaje, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # Crear un Text widget para mostrar el mensaje
        txt_informe = tk.Text(frame_mensaje, yscrollcommand=scrollbar.set)
        txt_informe.pack(fill="both", expand=True)
        txt_informe.insert("1.0", mensaje)

        # Configurar el scrollbar para controlar el desplazamiento del Text widget
        scrollbar.config(command=txt_informe.yview)

    def filtrar_productos(self, event):
        texto = self.combo_productos.get()
        if texto == "":
            self.combo_productos["values"] = [producto.nombre for producto in self.inventario.productos]
        else:
            filtrado = [producto.nombre for producto in self.inventario.productos if texto.lower() in producto.nombre.lower()]
            self.combo_productos["values"] = filtrado
    
    def buscar_cliente_por_cedula(self):
        cedula = self.entry_cedula_cliente.get()
        cliente = self.base_datos.buscar_cliente_por_cedula(cedula)
        if cliente:
            self.entry_nombre_cliente.config(state="normal")
            self.entry_nombre_cliente.delete(0, tk.END)
            self.entry_nombre_cliente.insert(0, cliente[1])  # Suponiendo que el nombre está en el índice 1
            self.entry_nombre_cliente.config(state="readonly")
        else:
            messagebox.showinfo("Información", "Cliente no encontrado. Puede agregar un nuevo cliente.")

    def modificar_proveedor(self, combobox):
        selected_proveedor = combobox.get()
        if selected_proveedor != "Seleccionar":
            proveedor = next((p for p in self.base_datos.obtener_proveedores() if p[1] == selected_proveedor), None)
            if proveedor:
                nuevo_nombre = self.entries_proveedor["Nombre"].get()
                nuevo_contacto = self.entries_proveedor["Contacto"].get()
                nueva_direccion = self.entries_proveedor["Dirección"].get()

                if nuevo_nombre and nuevo_contacto and nueva_direccion:
                    try:
                        # Actualizar el proveedor en la base de datos
                        self.base_datos.actualizar_proveedor(Proveedor(proveedor[0], nuevo_nombre, nuevo_contacto, nueva_direccion))
                        messagebox.showinfo("Éxito", "Proveedor modificado correctamente.")
                        self.actualizar_lista_proveedores(self.combo_proveedores_proveedores)  # Actualiza el combobox de proveedores
                        self.actualizar_lista_proveedores(self.combo_proveedores_agregar)  # Actualiza el combobox de agregar producto
                        self.actualizar_lista_proveedores_modificar() # Actualiza el combobox de modificar producto

                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo modificar el proveedor: {e}")
                else:
                    messagebox.showerror("Error", "Complete todos los campos.")
            else:
                messagebox.showerror("Error", "Proveedor no encontrado.")
        else:
            messagebox.showerror("Error", "Seleccione un proveedor para modificar.")

    def modificar_producto(self):
        selected_product = self.combo_modificar.get()
        if selected_product != "Seleccionar":
            producto = next((p for p in self.inventario.productos if p.nombre == selected_product), None)
            if producto:
                nuevo_nombre = self.entries_modificar["Nombre del Producto"].get()
                nueva_descripcion = self.entries_modificar["Descripción"].get()
                nuevo_precio = self.entries_modificar["Precio"].get()
                nuevo_stock = self.entries_modificar["Stock"].get()
                nuevo_proveedor_nombre = self.combo_proveedores_modificar.get()

                # Buscar el ID del proveedor por su nombre
                proveedores = self.base_datos.obtener_proveedores()
                nuevo_proveedor_id = next((proveedor[0] for proveedor in proveedores if proveedor[1] == nuevo_proveedor_nombre), None)

                if nuevo_nombre and nueva_descripcion and nuevo_precio and nuevo_stock and nuevo_proveedor_id:
                    try:
                        producto.nombre = nuevo_nombre
                        producto.descripcion = nueva_descripcion
                        producto.precio = float(nuevo_precio)
                        producto.cantidad_stock = int(nuevo_stock)
                        producto.proveedor_id = nuevo_proveedor_id
                        self.base_datos.actualizar_producto(producto)
                        messagebox.showinfo("Éxito", "Producto modificado correctamente.")
                    except ValueError:
                        messagebox.showerror("Error", "Ingrese datos válidos para precio y stock.")
                else:
                    messagebox.showerror("Error", "Complete todos los campos.")
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        else:
            messagebox.showerror("Error", "Seleccione un producto para modificar.")
            
    def eliminar_producto(self):
        selected_product = self.combo_modificar.get()
        if selected_product != "Seleccionar":
            producto = next((p for p in self.inventario.productos if p.nombre == selected_product), None)
            if producto:
                self.inventario.eliminar_producto(producto)
                self.base_datos.eliminar_producto(producto)
                self.combo_modificar["values"] = ["Seleccionar"] + [p.nombre for p in self.inventario.productos]
                messagebox.showinfo("Éxito", "Producto eliminado correctamente.")
            else:
                messagebox.showerror("Error", "Producto no encontrado.")
        else:
            messagebox.showerror("Error", "Seleccione un producto para eliminar.")

    def eliminar_proveedor(self,combobox):
        selected_proveedor = combobox.get() # Usar el combobox que se pasó como argumento
        if selected_proveedor != "Seleccionar":
            proveedor = next((p for p in self.base_datos.obtener_proveedores() if p[1] == selected_proveedor), None)
            if proveedor:
                try:
                    # Eliminar el proveedor de la base de datos
                    self.base_datos.eliminar_proveedor(proveedor[0])  # Suponiendo que el ID está en el índice 0
                    messagebox.showinfo("Éxito", "Proveedor eliminado correctamente.")

                    # Actualizar la lista de proveedores en todas las pestañas
                    self.actualizar_lista_proveedores(self.combo_proveedores_proveedores)  # Actualiza el combobox de proveedores
                    self.actualizar_lista_proveedores(self.combo_proveedores_agregar)  # Actualiza el combobox de agregar producto
                    self.actualizar_lista_proveedores_modificar() # Actualiza el combobox de modificar producto

                    # Limpiar los campos de entrada
                    self.entries_proveedor["Nombre"].delete(0, tk.END)
                    self.entries_proveedor["Contacto"].delete(0, tk.END)
                    self.entries_proveedor["Dirección"].delete(0, tk.END)

                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo eliminar el proveedor: {e}")
            else:
                messagebox.showerror("Error", "Proveedor no encontrado.")
        else:
            messagebox.showerror("Error", "Seleccione un proveedor para eliminar.")

    def actualizar_precio_venta(self, event=None):
        producto_seleccionado = self.combo_productos.get()
        cantidad = self.entry_cantidad.get()

        if producto_seleccionado and cantidad:
            producto = next((p for p in self.inventario.productos if p.nombre == producto_seleccionado), None)
            if producto:
                try:
                    cantidad = int(cantidad)
                    total = producto.precio * cantidad
                    self.entry_total.config(state="normal")
                    self.entry_total.delete(0, tk.END)
                    self.entry_total.insert(0, f"{total:.2f}")
                    self.entry_total.config(state="readonly")
                except ValueError:
                    self.entry_total.config(state="normal")
                    self.entry_total.delete(0, tk.END)
                    self.entry_total.insert(0, "0.00")
                    self.entry_total.config(state="readonly")

    def actualizar_lista_productos(self):
        productos = self.base_datos.obtener_productos()  # Esto devuelve una lista de objetos Producto
        nombres_productos = [producto.nombre for producto in productos]  # Acceder al atributo nombre
        self.combo_productos["values"] = nombres_productos
        if nombres_productos:
            self.combo_productos.current(0)  # Seleccionar el primer producto por defecto
            
    def actualizar_datos_producto_seleccionado(self, event):
        selected_product = self.combo_modificar.get()
        if selected_product != "Seleccionar":
            producto = next((p for p in self.inventario.productos if p.nombre == selected_product), None)
            if producto:
                self.entries_modificar["Nombre del Producto"].delete(0, tk.END)
                self.entries_modificar["Nombre del Producto"].insert(0, producto.nombre)
                self.entries_modificar["Descripción"].delete(0, tk.END)
                self.entries_modificar["Descripción"].insert(0, producto.descripcion)
                self.entries_modificar["Precio"].delete(0, tk.END)
                self.entries_modificar["Precio"].insert(0, str(producto.precio))
                self.entries_modificar["Stock"].delete(0, tk.END)
                self.entries_modificar["Stock"].insert(0, str(producto.cantidad_stock))

                # Actualizar el Combobox de proveedores
                proveedores = self.base_datos.obtener_proveedores()
                proveedor_nombre = next((proveedor[1] for proveedor in proveedores if proveedor[0] == producto.proveedor_id), None)
                if proveedor_nombre:
                    self.combo_proveedores_modificar.set(proveedor_nombre)
                else:
                    self.combo_proveedores_modificar.set("")

    def actualizar_lista_proveedores_modificar(self):
        proveedores = self.base_datos.obtener_proveedores()
        nombres_proveedores = [proveedor[1] for proveedor in proveedores]  # Suponiendo que el nombre está en el índice 1
        self.combo_proveedores_modificar["values"] = nombres_proveedores
        if nombres_proveedores:
            self.combo_proveedores_modificar.current(0)  # Seleccionar el primer proveedor por defecto

    def actualizar_lista_proveedores(self, combobox):  # Recibir el combobox como argumento
        proveedores = self.base_datos.obtener_proveedores()
        nombres_proveedores = ["Seleccionar"] + [proveedor[1] for proveedor in proveedores]
        combobox["values"] = nombres_proveedores  # Usar el combobox recibido
        combobox.current(0)  # Establecer "Seleccionar" como opción por defecto