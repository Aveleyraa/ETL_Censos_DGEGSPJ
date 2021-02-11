import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests 
  


"""
El url es el origen de la página de donde proviene la información 
en est ejemplo, primer se explora la página donde se encuentran los archivos 
para extraer todos los links de los mismos, para después descargarlos en la carpeta de origen 
"""
  
# URL de INEGI  
url_inegi = 'https://www.inegi.org.mx'


#obtiene las direcciones de donde se van a descargar los archivos
def get_sub_links():

    url = "https://www.inegi.org.mx/programas/cngspspe/2019/#Tabulados"
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)
    page = driver.page_source   

    soup = BeautifulSoup(page, 'html.parser')
    driver.quit()
    tags_sub = soup.findAll('a', class_='componente enlMen')

    url_sub_pag = [url_inegi + i['href'] + '#Tabulados' for i in tags_sub if i['href'].startswith('/programas')]

    return url_sub_pag




  
def get_excel(url_sub_pag):  
    
    excel_links = []
    while len(excel_links) <= len(url_sub_pag):

        for i in url_sub_pag:
            
            url = str(i)
            options = Options()
            options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(3)
            page = driver.page_source           

            soup = BeautifulSoup(page, 'html.parser')
            container = soup.find_all('div', attrs={
                'class':'table-responsive'})
            driver.quit()
            tags = soup.findAll('a', class_='aLink')
            
            excel_links.append([url_inegi + link['href'] for link in tags if link['href'].endswith('xlsx')]) 
            print(len(excel_links))
    #excel_links = ", ".join(map(str, excel_links))
    excel_links = [x for t in excel_links for x in t if isinstance(x, str)]
    return excel_links



def descarga_excel(excel_links):  
  
    for link in excel_links:  
  
        '''itera a traves de todos los links excel_links
        y descarga unos por uno los archivos'''
          
        # obtiene el nombre del archivo haciendo un split en el link  
          
        file_name = link.split('/')[-1]  
  
        print( "Descargando archivo:%s"%file_name)  
          
        # crea el objeto   
        r = requests.get(link, stream = True)  
          
        # inicia la descarga 
        with open(file_name, 'wb') as f:  
            for chunk in r:  
                if chunk:  
                    f.write(chunk)  
          
        print( "%s descargado!\n"%file_name ) 
  
    print ("Todos los archivos han sido descargados!") 
    return
  
  
if __name__ == "__main__":  
  
    # obtiene todos los links   
    url_sub_pag = get_sub_links() 

    
    excel_links = get_excel(url_sub_pag) 
    
    # descarga todos los archivos de tabulados en excel
    descarga_excel(excel_links)  
      