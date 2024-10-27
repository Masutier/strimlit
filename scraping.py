import requests
import sqlite3 as sql3
from bs4 import BeautifulSoup
from geopy.geocoders import Nominatim
from dbs import db_conn


def obtener_total_paginas(base_url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(base_url, headers=headers)
        response.raise_for_status()  # Verificar si la solicitud fue exitosa
    except requests.exceptions.RequestException as e:
        print(f"Error al obtener la página: {e}")
        return 0
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Buscar el elemento de paginación
    search_results_content = soup.find('div', class_='search-results-pagination')
    if search_results_content:
        paginacion = search_results_content.find('ul', class_='list')
        if paginacion:
            # print("Paginación encontrada")
            # print(paginacion.prettify())  # Imprimir el HTML de la paginación para depuración
            paginas = paginacion.find_all('li', class_='ant-pagination-item')
            if paginas:
                total_paginas = int(paginas[-2].text.strip())  # Obtener el número de la penúltima página
                return total_paginas
       # else:
            #print("No se encontró el elemento de paginación")
    else:
        print("No se encontró el contenedor de paginación")
    return 0


def extraer_datos_fincaraiz(base_url, total_pages):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    locales = []

    for page in range(1, total_pages + 1):
        url = f"{base_url}?page={page}"
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Verificar si la solicitud fue exitosa
        except requests.exceptions.RequestException as e:
            print(f"Error al obtener la página {page}: {e}")
            continue
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Buscar dentro de 'search-results-content'
        search_results_content = soup.find('div', class_='search-results-content')
        if search_results_content:
            listings_wrapper = search_results_content.find('section', class_='listingsWrapper')
            if listings_wrapper:
                for local in listings_wrapper.find_all('div', class_='listingCard'):
                    titulo_element = local.find('span', class_='lc-title')
                    ubicacion_element = local.find('strong', class_='lc-location')
                    precio_element = local.find('span', class_='heading')
                    typology_element = local.find('div', class_='lc-typologyTag')
                    enlace_element = local.find('a', href=True)

                    if titulo_element and ubicacion_element and precio_element:
                        titulo = titulo_element.text.strip()
                        ubicacion = ubicacion_element.text.strip()
                        precio = precio_element.text.strip()
                        typology = typology_element.text.strip() if typology_element else "N/A"
                        enlace ="https://www.fincaraiz.com.co" + enlace_element['href']
                        try:
                            latitud, longitud = convertir_ubicacion_a_coordenadas(ubicacion)
                        except:
                            print("Not Found")

                        locales.append({
                            'titulo': titulo,
                            'ubicacion': ubicacion,
                            'precio': precio,
                            'typology': typology,
                            'enlace': enlace,
                            'latitud': latitud,
                            'longitud': longitud
                        })

    return locales


def convertir_ubicacion_a_coordenadas(ubicacion):
    print('ubicacion', ubicacion)
    print("*" * 100)
    #geolocator = Nominatim(user_agent="myGeocoder")
    geolocator = Nominatim(user_agent="WhereIsMyPromises")
    location = geolocator.geocode(ubicacion)
    if location:
        return location.latitude, location.longitude
    else:
        return None, None


def main():
    base_url = "https://www.fincaraiz.com.co/arriendo/locales"
    total_pages = obtener_total_paginas(base_url)
    locales = extraer_datos_fincaraiz(base_url, total_pages)

    if locales:
        for local in locales:
            Titulo = local['titulo']
            Ubicacion = local['ubicacion']
            Precio = str(local['precio'])
            Typology = local['typology']
            Enlace = local['enlace']
            Latitud = local['latitud'] 
            Longitud = local['longitud']                         

            try:
                conn = db_conn()
                conn.execute("CREATE TABLE Locales (Titulo, Ubicacion, Precio, Typology, Enlace, Latitud, Longitud)")
                conn.commit()
                conn.execute("INSERT INTO Locales (Titulo, Ubicacion, Precio, Typology, Enlace, Latitud, Longitud) VALUES (?, ?, ?, ?, ?, ?, ?)", (Titulo, Ubicacion, Precio,Typology,Enlace,Latitud,Longitud))
                conn.commit()
                conn.close()
                print(f"Titulo: {local['titulo']}, Ubicacion: {local['ubicacion']}, Precio: {local['precio']}, Typology: {local['typology']}, Enlace: {local['enlace']}, Latitud: {local['latitud']}, Longitud: {local['longitud']}")
            except:
                conn = db_conn()
                conn.execute("INSERT INTO Locales (Titulo, Ubicacion, Precio, Typology, Enlace, Latitud, Longitud) VALUES (?, ?, ?, ?, ?, ?, ?)", (Titulo, Ubicacion, Precio,Typology,Enlace, Latitud,Longitud))
                conn.commit()
                conn.close()
                print(f"Titulo: {local['titulo']}, Ubicacion: {local['ubicacion']}, Precio: {local['precio']}, Typology: {local['typology']}, Enlace: {local['enlace']}, Latitud: {local['latitud']}, Longitud: {local['longitud']}")
    else:
        print("No se encontraron locales.")


main()
