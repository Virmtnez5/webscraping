# importar el modulo request para extrar una pagina web
import requests
# importar del modulo bs4 la libreria BeautifulSoup para transformar el codigo en html
from bs4 import BeautifulSoup
# Importar la clase datetime del modulo datetime para trabajar con fechas
from datetime import datetime

# Función para transformar una cadena de caracteres de fecha en un objeto de fecha de tipo datetime
def transformar_fecha(fecha_caracteres):
    fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]),
                     int(fecha_caracteres[6:8]))
    return fecha
# Funcion principal para realizar web scraping
def webscraping(url_scraping,categoria_scraping='todas'):
    # URL de de telemadrid
    url = url_scraping

    # Realizar la petición
    try:
        respuesta = requests.get(url)
        #print(respuesta)
        #print(respuesta.text)
        # Verificar si la petición fue exitosa (código 200)
        if respuesta.status_code == 200:
            try:
                # Crear el archivo noticias.csv si no existe y escribir la cabecera
                with open('../data/noticias.csv', 'w') as f:
                    f.write('titulo,url,categoria,fecha'+'\n')
                # Analizar el contenido con BeautifulSoup
            except:
                print("ERROR: no se pudo crear el archivo noticias.csv")
            try:
                # analizar el contenido HTML con BeatufulSoup
                soup = BeautifulSoup(respuesta.text, 'html.parser')
                #print(soup)
                # Aquí puedes realizar operaciones de Web Scraping
                # ...
                try:
                    # Encontrar todos los elementos 'article' con la clase 'card-news'
                    noticias = soup.find_all('article', class_='card-news')
                    if noticias:
                        #print(noticias)
                        lista_categorias = []
                        for articulo in noticias:
                            #print(articulo)
                            try:
                                # Extraer informacion del articulo
                                titulo = articulo.find('a', class_='oop-link').text.strip()
                                url_noticia = articulo.find('a', class_='opp-link')['href']
                                #print(url_noticia)
                                lista_url_noticia = url_noticia.split('/')
                                # Verificar si el segundo elemento de lista_url_noticia no está vacío
                                if lista_url_noticia[1] != '':
                                    # Asignar el valor del segundo elemento a la variable categoria
                                    categoria = lista_url_noticia[1]
                                # En caso contrario (si lista_url_noticia[1] está vacío),
                                # asignar el valor del cuarto elemento de lista_url_noticia a la variable categoria
                                else:
                                    categoria = lista_url_noticia[3]
                                # Agregar la categoría a la lista de categorías
                                lista_categorias.append(categoria)
                                # Dividir la URL de la noticia usando '--' como separador
                                lista_fecha = url_noticia.split('--')
                                # Extraer la cadena de caracteres de la fecha eliminando '.html' al final
                                fecha_caracteres = lista_fecha[1].replace('.html', '')
                                # print(fecha_caracteres)
                                # print(fecha_caracteres[0:4])
                                # print(fecha_caracteres[4:6])
                                # print(fecha_caracteres[6:8])
                                # print(fecha_caracteres[8:10])
                                # print(fecha_caracteres[10:12])
                                # print(fecha_caracteres[12:14])
                                fecha = transformar_fecha(fecha_caracteres)
                                fecha = fecha.strftime("%Y/%m/%d")
                                # Limpieza del titulo para evitar problemar en el archivo CSV
                                titulo = titulo.replace('\'','').replace('"','').replace(',','')
                                # Escribir en el archivo CSV según la categoría seleccionada
                                if categoria_scraping == 'todas':
                                    try:
                                        with open('../data/noticias.csv', 'a') as f:
                                            f.write(titulo+','+url_noticia+','+categoria+','+str(fecha)+'\n')
                                        # Analizar el contenido con BeautifulSoup
                                    except:
                                        print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                else:
                                    if categoria == categoria_scraping:
                                        try:
                                            with open('../data/noticias_'+categoria_scraping+'.csv', 'a') as f:
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')
                                            # Analizar el contenido con BeautifulSoup
                                        # Manejar cualquier excepción que pueda ocurrir al anexar la noticia al archivo noticias.csv
                                        except:
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                            # Capturar cualquier excepción que pueda ocurrir al intentar encontrar información de la noticia
                            except:
                                try:
                                    # Intentar encontrar información de la noticia utilizando otra clase de enlace ('lnk')
                                    titulo = articulo.find('a', class_='lnk').text.strip()
                                    url_noticia = articulo.find('a', class_='lnk')['href']
                                    # Dividir la URL de la noticia usando '/' como separador
                                    lista_url_noticia = url_noticia.split('/')
                                    # Verificar si el segundo elemento de lista_url_noticia no está vacío
                                    if lista_url_noticia[1] != '':
                                        # Asignar el valor del segundo elemento a la variable categoria
                                        categoria = lista_url_noticia[1]
                                    # En caso contrario (si lista_url_noticia[1] está vacío),
                                    # asignar el valor del cuarto elemento de lista_url_noticia a la variable categoria
                                    else:
                                        # Agregar la categoría a la lista de categorías
                                        categoria = lista_url_noticia[3]
                                    lista_categorias.append(categoria)
                                    # Dividir la URL de la noticia usando '--' como separador
                                    lista_fecha = url_noticia.split('--')
                                    # Extraer la cadena de caracteres de la fecha eliminando '.html' al final
                                    fecha_caracteres = lista_fecha[1].replace('.html', '')
                                    #print(fecha_caracteres)
                                    #print(fecha_caracteres[0:4])
                                    #print(fecha_caracteres[4:6])
                                    #print(fecha_caracteres[6:8])
                                    #print(fecha_caracteres[8:10])
                                    #print(fecha_caracteres[10:12])
                                    #print(fecha_caracteres[12:14])
                                    # Crear un objeto de fecha utilizando los elementos de fecha_caracteres
                                    fecha = datetime(int(fecha_caracteres[0:4]), int(fecha_caracteres[4:6]), int(fecha_caracteres[6:8]))
                                    # Formatear la fecha en el formato "YYYY/MM/DD"
                                    fecha = fecha.strftime("%Y/%m/%d")
                                    # Reemplazar caracteres no deseados en el título
                                    titulo = titulo.replace('\'', '').replace('"', '').replace(',', '')
                                    # Verificar si la categoría seleccionada es 'todas'
                                    if categoria_scraping == 'todas':
                                        # Analizar el contenido con BeautifulSoup
                                        except:
                                        # Intentar realizar las siguientes operaciones dentro de un bloque try-except
                                        try:
                                            # Intentar abrir el archivo noticias.csv en modo de escritura (añadir al final)
                                            with open('../data/noticias.csv', 'a') as f:
                                                # Escribir la información de la noticia en el archivo CSV
                                                f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                    fecha) + '\n')
                                            # Analizar el contenido con BeautifulSoup
                                        except:
                                            # Manejar cualquier excepción que pueda ocurrir al realizar las operaciones anteriores
                                            print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                    else:
                                        # En caso de que no haya ocurrido ninguna excepción en el bloque try
                                        if categoria == categoria_scraping:
                                            # Intentar abrir el archivo específico de la categoría en modo de escritura (añadir al final)
                                            try:
                                                with open('../data/noticias_' + categoria_scraping + '.csv', 'a') as f:
                                                    # Escribir la información de la noticia en el archivo CSV específico de la categoría
                                                    f.write(titulo + ',' + url_noticia + ',' + categoria + ',' + str(
                                                        fecha) + '\n')
                                                # Analizar el contenido con BeautifulSoup
                                            except:
                                                # Manejar cualquier excepción que pueda ocurrir al realizar las operaciones anteriores
                                                print("ERROR: no se pudo anexar la noticia al archivo noticias.csv")
                                except:
                                    pass
                        #print(lista_categorias)
                        conjunto_categorias = set(lista_categorias)
                        #print(conjunto_categorias)
                    else:
                        # Imprimir un mensaje de error si no se encontraron artículos en la página
                        print(f"Error La pagina {url} no contiene noticias")
                except:
                    # Manejar cualquier excepción que pueda ocurrir al convertir la página a código HTML
                        print(f"ERROR: No se pudo encontrar articulos en el codigo html")
            except:
                print(f"ERROR: no se pudo convertir la pagina a codigo html")
        else:
            # Imprimir un mensaje de error si la petición HTTP no fue exitosa
            print(f"Error al obtener la página web. Código de estado: {respuesta.status_code}")
    except:
        # Manejar cualquier excepción que pueda ocurrir al abrir la página web o procesarla
        print(f"ERROR: No se puede abrir la web pagina {url} o existe un error al procesarla")
    # Devolver el conjunto de categorías al final de la función
    return conjunto_categorias

# Obtener la lista de categoría
listado_categorias = webscraping('https://www.telemadrid.es/','todas')
# Menú para seleccionar la categoría
seleccion = 'x'
# Ejecutar un bucle mientras la variable 'seleccion' no sea '0'
while seleccion != '0':
    # Imprimir la lista de categorías disponibles
    print("Lista de categorias: ")
    i = 1
    for opcion in listado_categorias:
        print(f"{i}.- {opcion}")
        i = i + 1
    # Imprimir la opción para salir del bucle
    print("0.- Salir")
    # Solicitar al usuario que seleccione una opción ingresando un número
    seleccion = input("Por favor seleccione una opcion indicando un numero:")
    # Convertir la lista de categorías a una lista para facilitar el acceso por índice
    categorias_listas = list(listado_categorias)
    # Obtener la categoría seleccionada por el usuario utilizando su elección numérica
    categoria_seleccionada = categorias_listas[int(seleccion)-1]
    # Llamar a la función webscraping con la URL base y la categoría seleccionada
    webscraping('https://www.telemadrid.es/', categoria_seleccionada)