import io
import time
import requests
import pandas as pd


def obtener_coordenadas(localidad, barrio):
    nombre = f"{barrio}, {localidad}, Bogotá, Colombia"
    url = f'https://nominatim.openstreetmap.org/search?q={nombre}&format=json'
    headers = {'User-Agent': 'openstreetmap/1.0 (heidy_2105@hotmail.com)'}
    respuesta = requests.get(url, headers=headers)

    if respuesta.status_code == 200:
        try:
            datos = respuesta.json()
            if datos:
                lat = datos[0]['lat']
                lon = datos[0]['lon']
                return lat, lon
        except ValueError:
            print("Error al decodificar la respuesta JSON")
    else:
        print(f"Error en la solicitud: {respuesta.status_code} - {respuesta.text}")

    return None, None


def createLocalCoord()
    df = pd.read_excel(io.BytesIO(uploaded['data/BARRIOS_BOGOTA_2024.xlsx'])) # Reemplaza 'your_excel_file.xlsx' con el nombre de tu archivo
    print(df.head()) 

    # Agregar columnas de coordenadas con retraso
    coordenadas = []
    for index, row in df.iterrows():
        lat, lon = obtener_coordenadas(row['LOCALIDAD'], row['BARRIO'])
        coordenadas.append((lat, lon))
        time.sleep(2)  # Esperar 2 segundos entre solicitudes

    df['latitud'], df['longitud'] = zip(*coordenadas)

    # Guardar el nuevo DataFrame
    df.to_csv('data/localidades_con_coordenadas.csv', index=False)


createLocalCoord()
