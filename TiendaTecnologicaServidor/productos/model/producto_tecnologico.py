from abc import ABC, abstractmethod

class ProductoTecnologico(ABC):
    def __init__(self, nombre, descripcion, precio, stock, marca):
        self.set_nombre(nombre)
        self.set_descripcion(descripcion)
        self.set_precio(precio)
        self.set_stock(stock)
        self.set_marca(marca)

    def __str__(self):
        return (f"Nombre: {self.nombre}\nDescripcion: {self.descripcion}\n"
                f"Precio: {self.precio}\nStock: {self.stock}\nMarca: {self.marca}")

    @abstractmethod
    def get_nombre(self): pass

    @abstractmethod
    def get_descripcion(self): pass

    @abstractmethod
    def get_precio(self): pass

    @abstractmethod
    def get_stock(self): pass

    @abstractmethod
    def get_marca(self): pass

    @abstractmethod
    def set_nombre(self, nombre): pass

    @abstractmethod
    def set_descripcion(self, descripcion): pass

    @abstractmethod
    def set_precio(self, precio): pass

    @abstractmethod
    def set_stock(self, stock): pass

    @abstractmethod
    def set_marca(self, marca): pass

    @abstractmethod
    def calcularPrecio(self): pass