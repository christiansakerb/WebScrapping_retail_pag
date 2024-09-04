import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def obtener_soup(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Crear un objeto BeautifulSoup con el contenido de la página
        return BeautifulSoup(response.text, 'html.parser')

#En cada página puede haber más de una foto por producto, para nuestr ejercicio solo extraemos una de ellas
def obtener_primeras_imagenes(urls):
    # Mantener solo la primera imagen de cada grupo
    primeras_imagenes = []
    imagen_anterior = ""

    for url in urls:        
        id_imagen = url.split('/')[-1]  # Extrae el ID del producto de la URL
        id_imagen = id_imagen.split('-')[0].split('.')[0].split('_')[0]

       # print(url,id_imagen,imagen_anterior,id_imagen[0],id_imagen[0].isdigit())
        if id_imagen != imagen_anterior and id_imagen[0].isdigit(): #and id_imagen[0].isdigit():# :  
            
            primeras_imagenes.append(url)
            imagen_anterior = id_imagen

    return primeras_imagenes

#url base + url producto 
def agregar_p(url_base,urls):
    nuevos_links = []
    for url in urls:
        url_nueva = url_base + url 
        nuevos_links.append(url_nueva)
    return nuevos_links

#Creación del Scrapper
def Scrapper(soup,url_base= "www.example.com/"):
    key_to_search = ["productReference","productName","linkText","imageUrl","Precios"]#"highPrice"
    key_multiples = ["imageUrl"]

    lista_variables = []
    largo_listas = []

    
    for ky in key_to_search:

        pattern = rf'"{ky}":"(.*?)"'
          
        results = re.findall(pattern, soup)
        link_text_list = list(results)
         
        if ky in key_multiples:
            link_text_list = obtener_primeras_imagenes(link_text_list)

        if ky == 'linkText': 
            link_text_list = agregar_p(url_base,link_text_list)
        lista_variables.append(link_text_list)
        largo_listas.append(len(link_text_list))

    data = {
        'SKU': lista_variables[0],
        'NOMBRE': lista_variables[1],
        'LINK': lista_variables[2],
        'PRECIO': lista_variables[4]}

    df = pd.DataFrame(data)
    #df.to_excel('Results_wscrapped.xlsx')
    return df