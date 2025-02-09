import sqlite3
from tkinter import ttk, messagebox 
from product import product  #Import of product class of module product.py

# Class for databse manage
class Database:
    def _init_(self):
        # SQLite database connection
        self.connection = sqlite3.connect("inventario.db")
        self.cursor = self.connection.cursor()  # Creating a cursor to execute a SQL query
        self.create_table()  # Call to method to create table if it does not exist

    def create_table(self):
        # Executing the SQL query to create the products table if it does not exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                stock INTEGER NOT NULL,
                supplier TEXT
            )
        ''')
        self.connection.commit()  # Confirming changes to the database

    def obtain_products(self):
        self.cursor.execute("SELECT * FROM products")
        rows = self.cursor.fetchall()  # Getting all the resulting rows
        return [product(*row) for row in rows] # Creating product objects from rows and returning a list of products

    def add_product(self, product):
        # Executing the SQL query to insert a new product into the table
        self.cursor.execute('''
            INSERT INTO products (name, description, price, stock, supplier)
            VALUES (?, ?, ?, ?, ?)
        ''', (product.name, product.description, product.price, product.stock, product.supplier))
        self.connection.commit()  # Confirming changes to the database

    def delete_product(self, product):
        self.cursor.execute('''
            DELETE FROM products WHERE product_id=?               
        ''', (product.product_id,))
        self.connection.commit()
        
    def update_product(self, product):
        try:
            # Execute the SQL query to update the product
            self.cursor.execute('''
                UPDATE products SET name=?, description=?, price=?, stock=?, supplier=? WHERE product_id=?
            ''', (product.name, product.description, product.price, product.stock, product.supplier, product.product_id))
            self.connection.commit()  # Commit changes to the database
        except sqlite3.Error as error:
            # Handling any database errors
            messagebox.showerror("Database error", f"Failed to update product: {error}")
    
    def search_products_name(self, name):
        try:
            # SQL query to search products by name match
            self.cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))
            products = self.cursor.fetchall()
            self.connection.commit()
        except sqlite3.Error as error:
            # Handling any database errors
            messagebox.showerror("Database error", f"Failed to obtain product: {error}")
        return products
    
    def search_products_supplier(self, supplier):
        try:
            # SQL query to search for products by supplier
            self.cursor.execute("SELECT * FROM products WHERE supplier=?", (supplier,))
            products = self.cursor.fetchall()
            self.connection.commit()
        except sqlite3.Error as error:
            # Handling any database errors
            messagebox.showerror("Database error", f"Failed to obtain product: {error}")
        return products

    def search_product_por_id(self, product_id):
        try:
            # SQL query to search for a product by ID
            self.cursor.execute("SELECT * FROM products WHERE product_id=?", (product_id,))
            product = self.cursor.fetchone()
            self.connection.commit()
        except sqlite3.Error as error:
            # Handling any database errors
            messagebox.showerror("Database error", f"Failed to obtain product: {error}")
        return product
    
    def close_connection(self):
        self.connection.close()  # Closed database connection