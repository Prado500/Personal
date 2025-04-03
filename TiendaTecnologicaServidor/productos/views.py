from django.shortcuts import render


import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .controller.controlador_tienda import ControladorTienda
from django.views.decorators.csrf import csrf_exempt

# Creamos un controlador en memoria.
controlador = ControladorTienda([])

@csrf_exempt
@require_http_methods(["POST"])
def create_celular(request):
    """
    Crea un celular a partir de datos JSON en el cuerpo de la petición.
    Ejemplo de JSON:
    {
      "nombre": "Samsung S20",
      "descripcion": "Celular gama alta",
      "precio": 2000,
      "stock": 10,
      "marca": "Samsung",
      "capacidad": 128,
      "fechaLanzamiento": "2025-03-20",
      "is_new": true
    }
    """

    
    try:
        
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    sku = data.get("sku")
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    precio = data.get("precio")
    stock = data.get("stock")
    marca = data.get("marca")
    capacidad = data.get("capacidad")
    fecha = data.get("fechaLanzamiento")
    is_new = data.get("is_new", True)  # Por defecto True
   

    # Validar datos mínimos
    if not sku or not nombre or precio is None or stock is None:
        return JsonResponse({"error": "Campos obligatorios faltantes"}, status=400)

    # Usamos el método de controlador
    controlador.agregar_producto(sku, nombre, descripcion, precio, stock, marca, capacidad, fecha, is_new)
    return JsonResponse({"message": "Celular creado con exito"}, status=201)


@require_http_methods(["GET"])
def list_celulares(request):
    """
    Lista todos los celulares en el controlador.
    Retorna un arreglo JSON.
    """
    if len(controlador.productos) == 0:
        return JsonResponse({"message": "Lista vacia"}, status=200)
    
    resultado = []
    for prod in controlador.productos:
        # Convertimos el objeto a dict
        item = {
            "nombre": prod.get_nombre(),
            "sku": prod.get_sku(),
            "descripcion": prod.get_descripcion(),
            "precio": prod.get_precio(),
            "stock": prod.get_stock(),
            "marca": prod.get_marca(),
            "capacidad": prod.get_capacidad(),
            "fechaLanzamiento": prod.get_fechaLanzamiento(),
            "isNew": getattr(prod, "is_new", True),  # si no existe, asume True
            "precio Con Iva": prod.calcularPrecio()
        }
        resultado.append(item)
    return JsonResponse(resultado, safe=False, status=200)

@csrf_exempt
@require_http_methods(["GET"])
def get_celular_by_sku(request, sku):
    producto = controlador.buscar_producto(sku)
    if producto is None:
        return JsonResponse({"error": "No se encontró celular con ese SKU"}, status=404)

    # Retorna todos los atributos
    item = {
        "sku": producto.get_sku(),
        "nombre": producto.get_nombre(),
        "descripcion": producto.get_descripcion(),
        "precio": producto.get_precio(),
        "stock": producto.get_stock(),
        "marca": producto.get_marca(),
        "capacidad": producto.get_capacidad(),
        "fechaLanzamiento": producto.get_fechaLanzamiento(),
        "isNew": getattr(producto, "is_new", True),
        "precioConIva": producto.calcularPrecio()
    }
    return JsonResponse(item, status=200)

@csrf_exempt
@require_http_methods(["PUT"])
def update_celular(request, sku):
    """
    Actualiza un celular existente buscándolo por nombre.
    Datos en JSON (solo lo que se desee actualizar):
    {
      "precio": 2500,
      "stock": 5,
      "is_new": false
    }
    """
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({"error": "JSON inválido"}, status=400)

    nuevo_precio = data.get("precio")
    nueva_descripcion = data.get("descripcion")
    nuevo_stock = data.get("stock")
    nueva_marca = data.get("marca")
    nueva_capacidad = data.get("capacidad")
    nueva_fecha_lanzamiento = data.get("fechaLanzamiento")
    es_nuevo = data.get("is_new")  # True/False

    controlador.actualizar_celular(
        sku,
        nuevo_precio=nuevo_precio,
        nueva_descripcion=nueva_descripcion,
        nuevo_stock=nuevo_stock,
        nueva_marca=nueva_marca,
        nueva_capacidad=nueva_capacidad,
        nueva_fecha_lanzamiento=nueva_fecha_lanzamiento,
        es_nuevo=es_nuevo
    )

    return JsonResponse({"message": f"Celular '{sku}' actualizado."}, status=200)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_celular(request, sku):
    """
    Elimina un celular buscándolo por nombre.
    """
    producto = controlador.buscar_producto(sku)
    if producto is None:
        return JsonResponse({"error": "No se encontró un celular con ese SKU"}, status=404)

    controlador.eliminar_producto(producto)
    return JsonResponse({"message": f"Celular con SKU '{sku}' eliminado con éxito"}, status=200)


@require_http_methods(["GET"])
def buscar_por_marca(request):
    """
    Ejemplo de uso: GET /celulares/buscar-por-marca?marca=Samsung
    Retorna lista de celulares coincidientes.
    """
    marca = request.GET.get("marca", None)
    if not marca:
        return JsonResponse({"error": "El parámetro 'marca' es obligatorio"}, status=400)

    # Creamos método en el controlador (o lo definimos inline):
    resultado = []
    for prod in controlador.productos:
        if prod.get_marca().lower() == marca.lower():
            item = {
            "nombre": prod.get_nombre(),
            "sku": prod.get_sku(),
            "descripcion": prod.get_descripcion(),
            "precio": prod.get_precio(),
            "stock": prod.get_stock(),
            "marca": prod.get_marca(),
            "capacidad": prod.get_capacidad(),
            "fechaLanzamiento": prod.get_fechaLanzamiento(),
            "isNew": getattr(prod, "is_new", True),  # si no existe, asume True
            "precio Con Iva": prod.calcularPrecio()
        }
            resultado.append(item)
    if len(resultado) == 0:
        return JsonResponse({"error": "No se encontraron celulares con esa marca"}, status=404)

    return JsonResponse(resultado, safe=False, status=200)


@require_http_methods(["GET"])
def buscar_por_rango_precio(request):
    """
    Ejemplo de uso: GET /celulares/buscar-por-precio?min=1000&max=3000
    """
    try:
        minimo = float(request.GET.get("min"))
        maximo = float(request.GET.get("max"))
    except (TypeError, ValueError):
        return JsonResponse({"error": "Parámetros 'min' o 'max' inválidos o ausentes"}, status=400)

    resultado = []
    for prod in controlador.productos:
        precio_base = prod.get_precio()
        if minimo <= precio_base <= maximo:
            item = {
            "nombre": prod.get_nombre(),
            "sku": prod.get_sku(),
            "descripcion": prod.get_descripcion(),
            "precio": prod.get_precio(),
            "stock": prod.get_stock(),
            "marca": prod.get_marca(),
            "capacidad": prod.get_capacidad(),
            "fechaLanzamiento": prod.get_fechaLanzamiento(),
            "isNew": getattr(prod, "is_new", True),  # si no existe, asume True
            "precio Con Iva": prod.calcularPrecio()
        }
            resultado.append(item)

    if not resultado:
        return JsonResponse({"error": "No se encontraron celulares en ese rango de precio"}, status=404)

    return JsonResponse(resultado, safe=False, status=200)
