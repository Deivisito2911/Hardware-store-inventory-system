import tkinter as tk
from inventoryInterface import interfaceinventary

# Inicialización de la aplicación
if __name__ == "_main_":
    root = tk.Tk()
    app = interfaceinventary(root)
    root.mainloop()