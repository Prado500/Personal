from ..model.celular import Celular

class ControladorTienda:
    def __init__(self, productos):
        self.productos = productos

    def agregar_producto(self, sku, nombre, descripcion, precio, stock, marca, capacidad, fechaLanzamiento, is_new=True):
        """
        Crea un Celular y lo agrega a self.productos. 
        is_new indica si el celular es nuevo (True) o reacondicionado (False).
        Por defecto, asumimos que es nuevo.
        """
        try:
            # Aquí pasamos is_new al constructor de Celular:
            celular = Celular(sku, nombre, descripcion, precio, stock, marca, capacidad, fechaLanzamiento, is_new)
            self.productos.append(celular)
        except ValueError as e:
            print(e)

    def listar_productos(self):
        """
        Muestra todos los productos de la tienda en consola,
        incluyendo si son nuevos o reacondicionados (si su __str__ lo indica).
        """
        for producto in self.productos:
            print(producto.__str__())

    def get_producto(self, index):
        """ 
        Muestra el producto en la posición 'index'. 
        """
        print(self.productos[index].__str__())

        
    def buscar_producto(self, sku):
        """
        Busca en la lista self.productos por 'sku' en lugar de 'nombre'.
        """
        for prod in self.productos:
            if prod.get_sku() == sku:   # (// NUEVO)
                return prod
        return None

    def actualizar_celular(self, sku, nuevo_precio=None, nueva_descripcion=None, 
                           nuevo_stock=None, nueva_marca=None, nueva_capacidad=None, 
                           nueva_fecha_lanzamiento=None, es_nuevo=None):
        """
        Actualiza un celular existente buscándolo por nombre.
        Solo modifica los atributos que reciban un valor distinto de None.
        'es_nuevo' (bool) indica si el celular pasa a ser nuevo o reacondicionado.
        """
        celular_obj = self.buscar_producto(sku)
        if celular_obj is None:
            return print(f"No se encontró un celular con el sku: {sku}") 

        # Actualizar atributos según parámetros no nulos:
        if nuevo_precio is not None:
            celular_obj.set_precio(nuevo_precio)
        if nueva_descripcion is not None:
            celular_obj.set_descripcion(nueva_descripcion)
        if nuevo_stock is not None:
            celular_obj.set_stock(nuevo_stock)
        if nueva_marca is not None:
            celular_obj.set_marca(nueva_marca)
        if nueva_capacidad is not None:
            celular_obj.set_capacidad(nueva_capacidad)
        if nueva_fecha_lanzamiento is not None:
            celular_obj.set_fechaLanzamiento(nueva_fecha_lanzamiento)
        if es_nuevo is not None:
            # Ajustamos is_new
            celular_obj.set_is_new(es_nuevo)

        print(f"Celular con SKU '{sku}' actualizado correctamente.")

    def eliminar_producto(self, producto):
        """ 
        Elimina un producto de la lista self.productos.
        """
        self.productos.remove(producto)

    def calcular_total(self):
        """ 
        Retorna la suma de (precioCalculado * stock) de todos los productos.
        """
        total = 0
        for i in self.productos:
            total += i.calcularPrecio() * i.get_stock()
        return total
