from sdk import obtener_soup,Scrapper

lista_urls = ["www.ejemplo.com"]



if __name__ == 'main.py':
    for url in lista_urls:

        Scrapper(obtener_soup(url),url_base= "www.example.com/")