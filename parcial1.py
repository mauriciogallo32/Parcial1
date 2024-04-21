#comandos para iniciar el redis en el ubuntu:
# sudo service redis-server start
# redis-cli

import redis

# Conexión a Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# Función para agregar un nuevo artículo al presupuesto
def agregar_articulo():
    nombre = input("Nombre del artículo: ")
    precio = input("Precio del artículo: ")

    nuevo_articulo = {
        'nombre': nombre,
        'precio': precio
    }
    redis_client.hmset(f"articulo:{nombre}", nuevo_articulo)
    print("Artículo agregado con éxito.")


# Función para actualizar un artículo existente en el presupuesto
def actualizar_articulo():
    nombre = input("Ingrese el nombre del artículo que desea actualizar: ")
    articulo = redis_client.hgetall(f"articulo:{nombre}")

    if articulo:
        print(f"Artículo actual: {articulo}")
        nombre = input("Nuevo nombre del artículo (deje en blanco para no cambiar): ") or articulo[b'nombre'].decode()
        precio = input("Nuevo precio del artículo (deje en blanco para no cambiar): ") or articulo[b'precio'].decode()

        nuevo_articulo = {
            'nombre': nombre,
            'precio': precio
        }

        redis_client.hmset(f"articulo:{nombre}", nuevo_articulo)
        print("Artículo actualizado con éxito.")
    else:
        print("Artículo no encontrado.")


# Función para eliminar un artículo del presupuesto
def eliminar_articulo():
    nombre = input("Ingrese el nombre del artículo que desea eliminar: ")

    if redis_client.exists(f"articulo:{nombre}"):
        redis_client.delete(f"articulo:{nombre}")
        print("Artículo eliminado con éxito.")
    else:
        print("Artículo no encontrado.")


# Función para ver un listado de todos los artículos en el presupuesto
def ver_listado_articulos():
    articulos = redis_client.keys("articulo:*")

    if articulos:
        print("Listado de artículos:")
        for articulo_key in articulos:
            articulo = redis_client.hgetall(articulo_key)
            print(f"Nombre: {articulo[b'nombre'].decode()}, Precio: {articulo[b'precio'].decode()}")
    else:
        print("No hay artículos en el presupuesto.")


# Función principal
def menu_principal():
    while True:
        print("\n--- Menú ---")
        print("a) Agregar nuevo artículo")
        print("c) Actualizar artículo existente")
        print("d) Eliminar artículo existente")
        print("e) Ver listado de artículos")
        print("f) Salir")

        opcion = input("Ingrese la opción deseada: ").lower()

        if opcion == 'a':
            agregar_articulo()
        elif opcion == 'c':
            actualizar_articulo()
        elif opcion == 'd':
            eliminar_articulo()
        elif opcion == 'e':
            ver_listado_articulos()
        elif opcion == 'f':
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida. Por favor, elija una opción válida.")


if __name__ == "__main__":
    menu_principal()
