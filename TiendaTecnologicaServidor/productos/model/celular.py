from .producto_tecnologico import ProductoTecnologico
from ..interfaces.iencender import ICelular

class Celular(ProductoTecnologico, ICelular):
    def __init__(self, nombre, descripcion, precio, stock, marca, capacidad, fechaLanzamiento, is_new=True):
        """
        is_new (bool): Indica si el celular es nuevo (True) o reacondicionado (False).
        Por defecto, asumimos que es nuevo (True).
        """
        super().__init__(nombre, descripcion, precio, stock, marca)
        self.set_capacidad(capacidad)
        self.set_fechaLanzamiento(fechaLanzamiento)
        self.set_is_new(is_new)

    def __str__(self):
        base_str = super().__str__()
        extra_info = (f"\nCapacidad: {self.capacidad}\n"
                      f"Fecha de lanzamiento: {self.fechaLanzamiento}\n"
                      f"¿Es nuevo?: {self.is_new}\n")
        return base_str + extra_info

    # GETTERS
    def get_nombre(self):
        return self.nombre

    def get_descripcion(self):
        return self.descripcion

    def get_precio(self):
        return self.precio

    def get_stock(self):
        return self.stock

    def get_marca(self):
        return self.marca

    def get_capacidad(self):
        return self.capacidad

    def get_fechaLanzamiento(self):
        return self.fechaLanzamiento

    def get_is_new(self) -> bool:
        return self.is_new

    # SETTERS
    def set_marca(self, marca):
        self.marca = marca

    def set_capacidad(self, capacidad):
        if capacidad <= 0:
            raise ValueError("La capacidad de almacenamiento no puede ser menor o igual a 0")
        self.capacidad = capacidad

    def set_fechaLanzamiento(self, fechaLanzamiento):
        self.fechaLanzamiento = fechaLanzamiento

    def set_descripcion(self, descripcion):
        self.descripcion = descripcion

    def set_precio(self, precio):
        if precio < 0:
            raise ValueError("el precio no puede ser negativo")
        self.precio = precio

    def set_stock(self, stock):
        if stock < 0:
            raise ValueError("no puede haber cantidades negativas en el stock")
        self.stock = stock

    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_is_new(self, is_new: bool):
        self.is_new = bool(is_new)

    def calcularPrecio(self):
        return self.precio + self.precio * 0.19

    def encender(self):
        print("Encendiendo celular")