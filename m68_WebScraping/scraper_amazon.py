import requests
from bs4 import BeautifulSoup
import pandas as pd

# Configuración
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}
BASE_URL = "https://www.amazon.com/s?k=laptops"

def obtener_productos(url):
    """Extrae productos de la página de listado de Amazon."""
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.content, "html.parser")

    productos = []
    for item in soup.select(".s-result-item[data-component-type='s-search-result']"):
        titulo = item.select_one("h2 a span")
        precio = item.select_one(".a-price .a-offscreen")
        link = item.select_one("h2 a")["href"]
        
        if titulo and precio:
            productos.append({
                "titulo": titulo.text.strip(),
                "precio": precio.text.strip(),
                "link": f"https://www.amazon.com{link}"
            })
    return productos

def obtener_detalles(productos):
    """Extrae detalles adicionales de cada producto."""
    for producto in productos:
        detalle_url = producto["link"]
        detalle_resp = requests.get(detalle_url, headers=HEADERS)
        detalle_soup = BeautifulSoup(detalle_resp.content, "html.parser")
        
        descripcion = detalle_soup.select_one("#productDescription")
        calificaciones = detalle_soup.select_one(".a-icon-alt")
        
        producto["descripcion"] = descripcion.text.strip() if descripcion else "No disponible"
        producto["calificaciones"] = calificaciones.text.strip() if calificaciones else "No disponible"
    return productos

def guardar_csv(productos, filename="productos_amazon.csv"):
    """Guarda los datos en un archivo CSV."""
    df = pd.DataFrame(productos)
    df.to_csv(filename, index=False, encoding="utf-8")
    print(f"Datos guardados en {filename}")

def main():
    print("Extrayendo datos de Amazon...")
    productos = obtener_productos(BASE_URL)
    print(f"{len(productos)} productos encontrados. Extrayendo detalles...")
    productos_con_detalles = obtener_detalles(productos)
    guardar_csv(productos_con_detalles)

if __name__ == "__main__":
    main()
