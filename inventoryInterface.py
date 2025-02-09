import tkinter as tk
from tkinter import ttk, messagebox 
import time
from dba import Database  
from inventary import inventary 
from product import product  
from sale import sale  
from sales import sales

class interfaceinventary:
    def _init_(self, root):
        # Inicialización de la clase Database para manejar la base de date
        self.Database = Database()
        # Inicialización de la clase inventary para manejar el inventary de products
        self.inventary = inventary()
        # Crea una lista de sales
        self.sales = sales()
        # Carga de los products desde la base de date al inventary
        self.load_products_from_db()
        

        # Configuración de la window principal de la aplicación
        self.root = root
        self.root.title("Inventory management system")
        self.root.geometry("800x450")

        # Configuración del notebook para view pestañas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(expand=True, fill='both')

        # Creación de las pestañas "add product" , "update product" , etc
        self.page_add = ttk.Frame(self.notebook)
        self.page_update = ttk.Frame(self.notebook)
        self.page_statistics = ttk.Frame(self.notebook)
        self.page_sales = ttk.Frame(self.notebook)
        self.notebook.add(self.page_add, text='add product')
        self.notebook.add(self.page_update, text='update product')
        self.notebook.add(self.page_statistics, text='statistics')
        self.notebook.add(self.page_sales, text='sales')

        # Creación de la interface para add un new product
        self.create_interface_add_product()
        # Creación de la interface para update un product existente
        self.create_interface_update_product()
        # Creación del botón para delete un product
        self.create_button_delete_product()  # Llamar a la función aquí
        # Creación del botón para view el report de inventarys
        self.create_button_view_report()
        # Creación de la interface de estadísticas
        self.create_interface_statistics()
        #Creación de la interface para cargar new sale
        self.create_interface_add_venta()
        #Creación del botón para view sales
        self.create_button_view_sales()
        

    def load_products_from_db(self):
        products_db = self.Database.obtain_products()
        self.inventary.products = products_db

    def create_interface_add_product(self):
        label_add = ["Product name", "Description", "Price", "Stock", "Supplier"]
        self.entries_add = {}
        for i, label in enumerate(label_add):
            tk.Label(self.page_add, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.page_add, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries_add[label] = entry
        self.button_add = tk.Button(self.page_add, text="add product", command=self.add_product, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.button_add.grid(row=len(label_add) + 1, column=0, columnspan=2, pady=10)

    def create_interface_update_product(self):
        label_update = ["Product selection:", "Product name", "Description", "Price", "Stock", "Supplier"]
        self.combo_update = ttk.Combobox(self.page_update, values=["Seleccionar"] + [product.name for product in self.inventary.products], font=("Arial", 12))
        self.combo_update.grid(row=0, column=1, padx=10, pady=5)
        self.combo_update.set("Selection")
        self.combo_update.bind("<<ComboboxSelected>>", self.update_date_product_seleccionado)
        self.entries_update = {}
        for i, label in enumerate(label_update[1:]):
            tk.Label(self.page_update, text=label, font=("Arial", 12)).grid(row=i + 1, column=0, padx=10, pady=5)
            entry = tk.Entry(self.page_update, font=("Arial", 12))
            entry.grid(row=i + 1, column=1, padx=10, pady=5)
            self.entries_update[label] = entry
        self.button_update = tk.Button(self.page_update, text="update product", command=self.update_product, font=("Arial", 12), bg="#008CBA", fg="white")
        self.button_update.grid(row=len(label_update) + 1, column=0, columnspan=2, pady=10)

    def create_interface_statistics(self):
        total_different_products = len(self.inventary.products)
        total_products = sum(product.cantidad_stock for product in self.inventary.products)
        total_inventory_value = sum(product.price * product.cantidad_stock for product in self.inventary.products)
        average_price = total_inventory_value / total_products if total_products > 0 else 0
        
        # create label para view las estadísticas
        label_statistics = [
            f"Quantity of different products: {total_different_products}",
            f"Total amount of products: {total_products}",
            f"Total inventory value: ${total_inventory_value:.2f}",
            f"Average price of products: ${average_price:.2f}"
        ]

        # Colocar las label en la página de estadísticas
        for i, label in enumerate(label_statistics):
            tk.Label(self.page_statistics, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5, sticky='nsew')
        
        # Programar la próxima actualización de las estadísticas en 1 segundo
        self.root.after(1000, self.create_interface_statistics)

    def create_button_delete_product(self):
        self.button_delete = tk.Button(self.page_update, text="delete product", command=self.delete_product, font=("Arial", 12), bg="#FF5733", fg="white")
        self.button_delete.grid(row=8, column=0, columnspan=2, pady=10)

    def create_button_view_report(self):
        self.button_view_report = tk.Button(self.root, text="view report", command=self.view_report, font=("Arial", 12), bg="#333", fg="white")
        self.button_view_report.pack(pady=10)

    def create_interface_add_venta(self):
        label_add = ["Stock", "Payment method", "Total", "Products"]
        self.entries_add_sales = {}
        for i, label in enumerate(label_add):
            tk.Label(self.page_sales, text=label, font=("Arial", 12)).grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self.page_sales, font=("Arial", 12))
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries_add_sales[label] = entry
        self.button_add = tk.Button(self.page_sales, text="add sale", command=self.add_venta, font=("Arial", 12), bg="#4CAF50", fg="white")
        self.button_add.grid(row=len(label_add) + 1, column=0, columnspan=2, pady=10)
    
    def create_button_view_sales(self):
        self.button_view_report = tk.Button(self.root, text="view sales", command=self.view_sales, font=("Arial", 12), bg="#333", fg="white")
        self.button_view_report.pack(pady=10)
    

    
    def add_sale(self):
        try:
            num_articles = self.entries_add_sales["Cantidad Artículos"].get()
            payment_method = self.entries_add_sales["Medio de Pago"].get()
            total = float(self.entries_add_sales["Total"].get())
            products = int(self.entries_add_sales["products"].get())
            sale = sale(len(self.sales.sales) + 1, num_articles, payment_method, total, products)
            self.sales.add_venta(sale)
            messagebox.showinfo("Success", "product added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Enter valid dates for the product.")

    def view_sales(self):
        report = self.sales.generar_report_sales()
        message = "\n\n".join(report)

        # create una window secundaria para view el report
        window_report = tk.Toplevel(self.root)
        window_report.title("report de sales")
        
        # create un frame para contener el message con desplazamiento
        frame_message = tk.Frame(window_report)
        frame_message.pack(fill="both", expand=True)

        # create un scrollbar para desplazarse verticalmente
        scrollbar = ttk.Scrollbar(frame_message, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # create un Text widget para view el message
        txt_report = tk.Text(frame_message, yscrollcommand=scrollbar.set)
        txt_report.pack(fill="both", expand=True)
        txt_report.insert("1.0", message)

        # Configurar el scrollbar para controlar el desplazamiento del Text widget
        scrollbar.config(command=txt_report.yview)

    def add_product(self):
        try:
            name = self.entries_add["Product name"].get()
            description = self.entries_add["description"].get()
            price = float(self.entries_add["price"].get())
            stock = int(self.entries_add["stock"].get())
            supplier = self.entries_add["supplier"].get()
            product = product(len(self.inventary.products) + 1, name, description, price, stock, supplier)
            self.inventary.add_product(product)
            self.Database.add_product(product)
            self.combo_update["values"] = ["Selection"] + [p.name for p in self.inventary.products]
            messagebox.showinfo("Success", "Product added successfully.")
        except ValueError:
            messagebox.showerror("Error", "Enter valid dates for the product.")

    def update_date_product_seleccionado(self, event):
        selected_product = self.combo_update.get()
        if selected_product != "Seleccionar":
            product = next((p for p in self.inventary.products if p.name == selected_product), None)
            if product:
                self.entries_update["Product name"].delete(0, tk.END)
                self.entries_update["Product name"].insert(0, product.name)
                self.entries_update["Description"].delete(0, tk.END)
                self.entries_update["Description"].insert(0, product.description)
                self.entries_update["Price"].delete(0, tk.END)
                self.entries_update["Price"].insert(0, str(product.price))
                self.entries_update["Stock"].delete(0, tk.END)
                self.entries_update["Stock"].insert(0, str(product.cantidad_stock))
                self.entries_update["Supplier"].delete(0, tk.END)
                self.entries_update["Supplier"].insert(0, product.supplier)

    def update_product(self):
        selected_product = self.combo_update.get()
        if selected_product != "Selection":
            product = next((p for p in self.inventary.products if p.name == selected_product), None)
            if product:
                new_price = self.entries_update["price"].get()
                new_stock = self.entries_update["stock"].get()
                new_supplier = self.entries_update["supplier"].get()
                new_description = self.entries_update["description"].get()
                if new_price and new_stock and new_supplier and new_description:
                    try:
                        new_price = float(new_price)
                        new_stock = int(new_stock)
                        product.price = new_price
                        product.stock = new_stock
                        product.supplier = new_supplier
                        product.description = new_description
                        self.Database.update_product(product)
                        self.Database.cerrar_conexion()
                        self.Database = Database()
                        messagebox.showinfo("Success", "Product successfully modified.")
                    except ValueError:
                        messagebox.showerror("Error", "Please enter valid dates for price and stock.")
                else:
                    messagebox.showerror("Error", "Enter new price, stock, supplier and description.")
            else:
                messagebox.showerror("Error", "Product not found.")
        else:
            messagebox.showerror("Error", "Select a product to update.s")

    def delete_product(self):
        selected_product = self.combo_update.get()
        if selected_product != "Selection":
            product = next((p for p in self.inventary.products if p.name == selected_product), None)
            if product:
                self.inventary.delete_product(product)
                self.Database.delete_product(product)
                self.combo_update["values"] = ["Selection"] + [p.name for p in self.inventary.products]
                messagebox.showinfo("Success", "Product removed successfully.")
            else:
                messagebox.showerror("Error", "Product not found.")
        else:
            messagebox.showerror("Error", "Select a product to remove.")

    def view_report(self):
        report = self.inventary.generar_report()
        message = "\n\n".join(report)

        # create una window secundaria para view el report
        window_report = tk.Toplevel(self.root)
        window_report.title("report de inventarys")
        
        # create un frame para contener el message con desplazamiento
        frame_message = tk.Frame(window_report)
        frame_message.pack(fill="both", expand=True)

        # create un scrollbar para desplazarse verticalmente
        scrollbar = ttk.Scrollbar(frame_message, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        # create un Text widget para view el message
        txt_report = tk.Text(frame_message, yscrollcommand=scrollbar.set)
        txt_report.pack(fill="both", expand=True)
        txt_report.insert("1.0", message)

        # Configurar el scrollbar para controlar el desplazamiento del Text widget
        scrollbar.config(command=txt_report.yview)