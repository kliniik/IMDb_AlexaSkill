import requests
import json
import re
from bs4 import BeautifulSoup
from googletrans import Translator

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

# Obtener el título y detalle del usuario o de un argumento
def obtener_input(pelicula=None, detalle=None):
    if pelicula:
        pelicula = pelicula.strip().lower()
    else:
        pelicula = input("Introduce el título de la película: ").strip().lower()

    if detalle:
        detalle = detalle.strip().lower()
    else:
        detalle = input("Introduce el detalle que deseas conocer (opcional): ").strip()#.lower()

    return pelicula, detalle if detalle else None

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
    return soup.select("ul.ipc-metadata-list a.ipc-metadata-list-summary-item__t") or None

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
def buscarIMDb(pelicula=None, detalle=None):
    """Función principal que busca la película en IMDb y devuelve sus detalles. 
    Si se especifica un detalle ("Título", "Descripción", "Director", "Duración", 
    "Puntuación", "Número de votos" o "URL"), solo devuelve ese detalle."""
    traductor = Translator()
    titulo_original_usuario, detalle_usuario = obtener_input(pelicula, detalle)

    # Buscamos en el glosario
    if titulo_original_usuario in GLOSARIO:
        titulo_original_usuario = GLOSARIO[titulo_original_usuario]

    # Buscamos en IMDb
    resultados = buscar_en_imdb(titulo_original_usuario)

    # Buscamos en inglés si no se encontraron resultados 
    if not resultados:
        try:
            titulo_traducido = traductor.translate(titulo_original_usuario, dest='en').text.lower().strip()
        except Exception as e:
            print(f"Error al traducir: {e}")
            titulo_traducido = titulo_original_usuario.lower().strip()
        resultados = buscar_en_imdb(titulo_traducido)

    if not resultados:
        return {"Error": "No se encontraron resultados en IMDb."}

    # Obtenemos los detalles de las primeras 6 películas
    for resultado in resultados[:6]:
        detalles = obtener_detalles_pelicula(resultado)

        # Normalizamos los títulos para comparar
        titulo_norm = re.sub(r'^(Título original:|Original title:)\s*', '', detalles["Título"], flags=re.IGNORECASE).lower().strip()
        usuario_norm = re.sub(r'\s+', ' ', titulo_original_usuario).strip().lower()

        # Comparamos los títulos
        if usuario_norm == titulo_norm:
            if detalle_usuario:  # Si se proporcionó un detalle
                return detalles.get(detalle_usuario, "Detalle no encontrado")  # Retorna solo el detalle
            return detalles  # Si no se proporcionó un detalle, retorna toda la información

    return {"Error": "No se encontró una coincidencia exacta."}
