import requests
import json
import re
from bs4 import BeautifulSoup
from googletrans import Translator
import os
import argparse

# Glosario de traducciones manuales 
GLOSARIO = {
    "la jungla de cristal": "die hard",
    "¡olvídate de mí!": "eternal sunshine of the spotless mind",
    "la salchicha peleona": "beverly hills ninja",
    "sonrisas y lágrimas": "the sound of music",
    "dos rubias de pelo en pecho": "white chicks",
    "este muerto está muy vivo": "weekend at bernie's",
    "con faldas y a lo loco": "some like it hot",
    "tú a boston y yo a california": "the parent trap",
    "un canguro superduro": "the pacifier",
    "101 dálmatas": "one hundred and one dalmatians",
    "niños grandes": "grown ups",
    "la guerra de las galaxias": "star wars",
    "el planeta de los simios": "planet of the apes",
    "el señor de los anillos": "the lord of the rings",
    "una rubia muy legal": "legally blonde",
    "spiderman": "spider-man"
}

# Obtener el título del usuario o de un argumento
def obtener_titulo(pelicula):
    if pelicula != None:
        return pelicula.strip().lower()
    return input("Introduce el título de la película: ").strip().lower()

# Buscar la pelicula en IMDb
def buscar_en_imdb(titulo):
    """Realiza una búsqueda en IMDb y devuelve los resultados"""
    titulo_url = re.sub(r'\s+', '+', titulo)
    titulo_url = re.sub(r'[^\w\+\-]', '', titulo_url)
    url = f"https://www.imdb.com/find/?q={titulo_url}&s=tt"

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return None  # Error al acceder a IMDb

    soup = BeautifulSoup(response.text, "html.parser")

    # filtro peliculas
    resultados = soup.select("div.ipc-metadata-list-summary-item__c")
    peliculas = []
    
    for resultado in resultados:
        tags = resultado.select("ul.ipc-inline-list.ipc-metadata-list-summary-item__tl.base li.ipc-inline-list__item span")
        tags = [tag.text for tag in tags if not re.search(r'\d', tag.text)]
        if len(tags) == 0:
            peliculas.append(resultado.find('a', class_=re.compile('.*ipc-metadata-list-summary-item__t.*')))

    return peliculas or None

# Obtener detalles de la película
def obtener_detalles_pelicula(resultado):
    """Obtiene detalles de la película desde IMDb"""
    link_pelicula = f"https://www.imdb.com{resultado['href']}"

    headers = {"User-Agent": "Mozilla/5.0"}
    response_pelicula = requests.get(link_pelicula, headers=headers)
    soup_pelicula = BeautifulSoup(response_pelicula.text, "html.parser")

    # Obtener los datos de JSON-LD
    script_tag = soup_pelicula.find("script", type="application/ld+json")
    json_ld_data = json.loads(script_tag.string) if script_tag else {}

    # Obtener el título original
    titulo_original = soup_pelicula.select_one("div.sc-ec65ba05-1.fUCCIx")
    titulo_original = titulo_original.text.strip() if titulo_original else resultado.text.strip()

    # Obtener la duración
    duracion = json_ld_data.get("duration", "No disponible")
    if "PT" in duracion:
        horas = re.search(r'PT(\d+)H', duracion)
        minutos = re.search(r'PT\d+H?(\d+)M', duracion)
        duracion = f"{horas.group(1)}h {minutos.group(1)}m" if horas and minutos else (
            f"{horas.group(1)}h" if horas else f"{minutos.group(1)}m" if minutos else "No disponible")
    
    titulo_original = re.sub(r'^\s*(Título original:|Original title:)\s*[\n]*', '', titulo_original, flags=re.IGNORECASE)
    return {
        "Título": titulo_original,
        "Descripción": json_ld_data.get("description", "No disponible"),
        "Director": json_ld_data.get("director", [{}])[0].get("name", "No disponible"),
        "Duración": duracion,
        "Puntuación": json_ld_data.get("aggregateRating", {}).get("ratingValue", "No disponible"),
        "Número de votos": json_ld_data.get("aggregateRating", {}).get("ratingCount", "No disponible"),
        "URL": link_pelicula
    }

# La función principal 
def buscarIMDb(pelicula=None):
    """Función principal que busca la película en IMDb y devuelve sus detalles"""
    traductor = Translator()
    titulo_original_usuario = obtener_titulo(pelicula)

    # Buscamos en el glosario y en cache
    if titulo_original_usuario in GLOSARIO:
        titulo_original_usuario = GLOSARIO[titulo_original_usuario]
    
    # Crear json vacio si no existe
    if not os.path.isfile('cache.json'): 
        with open('cache.json', 'w') as f:
            json.dump({}, f)

    # Buscar en json
    with open('cache.json', 'r') as f:
        cache = json.load(f)

    if titulo_original_usuario in cache:
        return cache[titulo_original_usuario]

    # Buscamos en IMDb
    resultados = buscar_en_imdb(titulo_original_usuario)

    # Buscamos en inglés si no se encontraron resultados 
    if not resultados:
        try:
            titulo_traducido = traductor.translate(titulo_original_usuario, dest='en').text.lower().strip()
        except:
            titulo_traducido = titulo_original_usuario.lower().strip()
        resultados = buscar_en_imdb(titulo_traducido)

    if not resultados:
        return {"Error": "No se encontraron resultados en IMDb."}

    def guardar_cache(detalles):
        # Guardar en json
        with open('cache.json', 'r') as f:
            cache = json.load(f)

        cache[titulo_original_usuario] = detalles

        with open('cache.json', 'w') as f:
            json.dump(cache, f)
            
        return detalles
        
    # Buscar titulos exactos
    for resultado in resultados[:6]:
        detalles = obtener_detalles_pelicula(resultado)

        # Normalizamos los títulos para comparar
        titulo_norm = detalles["Título"].lower().strip()
        print(titulo_norm)
        usuario_norm = re.sub(r'\s+', ' ', titulo_original_usuario).strip().lower()

        # Comparamos los títulos parecidos exactos
        if usuario_norm == titulo_norm:
            guardar_cache(detalles)
            return detalles

    # Buscar titulos parecidos
    for resultado in resultados[:6]:
        detalles = obtener_detalles_pelicula(resultado)

        # Normalizamos los títulos para comparar
        titulo_norm = detalles["Título"].lower().strip()
        usuario_norm = re.sub(r'\s+', ' ', titulo_original_usuario).strip().lower()

        # Comparamos los títulos parecidos exactos
        if usuario_norm in titulo_norm:
            guardar_cache(detalles)
            return detalles

    return {"Error": "No se encontró una coincidencia."}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Buscar información de la película")
    parser.add_argument('--pelicula', type=str, required=True, help='El título de la película')
    parser.add_argument('--detalles', type=str, nargs='*', required=False, help='Lista de detalles (titulo, descripcion, director, duracion, puntuacion, votos, url)')
    
    correspondencia = {
                        "titulo": "Título",
                        "descripcion": "Descripción",
                        "director": "Director",
                        "duracion": "Duración",
                        "puntuacion": "Puntuación",
                        "votos": "Número de votos",
                        "url": "URL"
                    }
    
    # Argumentos
    args = parser.parse_args()
    pelicula = args.pelicula
    detalles = args.detalles

    # Resolución
    detalles_pelicula = buscarIMDb(pelicula)

    if not detalles:
        detalles = list(correspondencia.keys())
    
    results = [(correspondencia[detalle],detalles_pelicula[correspondencia[detalle]]) for detalle in detalles]
    print('-'*200)
    for result in results:
        print(f'{result[0]}: {result[1]}')
    print('-'*200)


