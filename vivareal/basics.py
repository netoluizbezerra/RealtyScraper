from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_path = which('chromedriver')
driver = webdriver.Firefox()
driver.get('https://www.vivareal.com.br/aluguel/sp/sao-paulo/?__vt=lnv:a&pagina=2')
driver.close()


import re, time, os
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd

# Inicializamos as listas para guardar as informações

link_imovel = []  # nesta lista iremos guardar a url
address = []  # nesta lista iremos guardar o endereço
neighbor = []  # nesta lista iremos guardar o bairro
anunciante = []  # nesta lista iremos guardar o anunciante
area = []  # nesta lista iremos guardar a area
tipo = []  # nesta lista iremos guardar o tipo de imóvel
room = []  # nesta lista iremos guardar a quantidade de quartos
bath = []  # nesta lista iremos guardar a quantidade de banheiros
park = []  # nesta lista iremos guardar a quantidade de vagas de garagem
price = []  # nesta lista iremos guardar o preço do imóvel

# Ele irá solicitar quantas páginas você deseja coletar
pages_number = int(input('Quantas paginas? '))
# inicializa o tempo de execução
tic = time.time()

# Configure chromedriver
# para executar, é necessário que você baixe o chromedriver e deixe ele na mesma pasta de execução, ou mude o path
chromedriver = "./chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome()

# Informe o link inicial para inicializar o scraping. Você pode trocar entre diversos filtros.
# Este scraper foi desenvolvido para o filtro de alugueis na cidade de santa maria no rio grande do sul.
# Pode acontecer das informações mudarem caso novos filtros sejam adicionados.
link = f'https://www.vivareal.com.br/aluguel/sp/sao-paulo/?__vt=lnv:a&pagina=1'
# link = f'https://www.vivareal.com.br/aluguel/rio-grande-do-sul/santa-maria/?pagina=1#onde=BR-Rio_Grande_do_Sul-NULL-Santa_Maria'
driver.get(link)

# Criando o loop entre as paginas do site
for page in range(1, pages_number + 1):

    # Definimos um sleep time para não sobrecarregar o site
    time.sleep(15)
    # coletamos todas as informações da página e transformamos em formato legivel
    data = driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    soup_complete_source = BeautifulSoup(data.encode('utf-8'), "lxml")

    # identificamos todos os itens de card de imóveis
    soup = soup_complete_source.find(class_='results-list js-results-list')

    # Web-Scraping
    # para cada elemento no conjunto de cards, colete:
    for line in soup.findAll(class_="js-card-selector"):
        # colete o endereço completo e o bairro
        try:
            full_address = line.find(class_="property-card__address").text.strip()
            address.append(full_address.replace('\n', ''))  # Get all address
            if full_address[:3] == 'Rua' or full_address[:7] == 'Avenida' or full_address[
                                                                             :8] == 'Travessa' or full_address[
                                                                                                  :7] == 'Alameda':
                neighbor_first = full_address.strip().find('-')
                neighbor_second = full_address.strip().find(',', neighbor_first)
                if neighbor_second != -1:
                    neighbor_text = full_address.strip()[neighbor_first + 2:neighbor_second]
                    neighbor.append(neighbor_text)  # Guarde na lista todos os bairros
                else:  # Bairro não encontrado
                    neighbor_text = '-'
                    neighbor.append(neighbor_text)  # Caso o bairro não seja encontrado
            else:
                get_comma = full_address.find(',')
                if get_comma != -1:
                    neighbor_text = full_address[:get_comma]
                    neighbor.append(
                        neighbor_text)  # Guarde na lista todos os bairros com problema de formatação provenientes do proprio website
                else:
                    get_hif = full_address.find('-')
                    neighbor_text = full_address[:get_hif]
                    neighbor.append(neighbor_text)

            # Coleta o link
            full_link = line.find(class_='property-card__main-info').a.get('href')
            link_imovel.append(full_link)

            # Coleta o anunciante
            full_anunciante = line.find(class_='property-card__account-link js-property-card-account-link').img.get(
                'alt').title()
            anunciante.append(full_anunciante)

            # Coleta a área
            full_area = line.find(
                class_="property-card__detail-value js-property-card-value property-card__detail-area js-property-card-detail-area").text.strip()
            area.append(full_area)

            # Coleta tipologia
            full_tipo = line.find(class_='property-card__title js-cardLink js-card-title').text.split()[0]
            full_tipo = full_tipo.replace(' ', '')
            full_tipo = full_tipo.replace('\n', '')
            tipo.append(full_tipo)

            # Coleta numero de quartos
            full_room = line.find(
                class_="property-card__detail-item property-card__detail-room js-property-detail-rooms").text.strip()
            full_room = full_room.replace(' ', '')
            full_room = full_room.replace('\n', '')
            full_room = full_room.replace('Quartos', '')
            full_room = full_room.replace('Quarto', '')
            room.append(full_room)  # Get apto's rooms

            # Coleta numero de banheiros
            full_bath = line.find(
                class_="property-card__detail-item property-card__detail-bathroom js-property-detail-bathroom").text.strip()
            full_bath = full_bath.replace(' ', '')
            full_bath = full_bath.replace('\n', '')
            full_bath = full_bath.replace('Banheiros', '')
            full_bath = full_bath.replace('Banheiro', '')
            bath.append(full_bath)  # Get apto's Bathrooms

            # Coleta numero de vagas de garagem
            full_park = line.find(
                class_="property-card__detail-item property-card__detail-garage js-property-detail-garages").text.strip()
            full_park = full_park.replace(' ', '')
            full_park = full_park.replace('\n', '')
            full_park = full_park.replace('Vagas', '')
            full_park = full_park.replace('Vaga', '')
            park.append(full_park)  # Get apto's parking lot

            # Coleta preço
            full_price = re.sub('[^0-9]', '', line.find(
                class_="property-card__price js-property-card-prices js-property-card__price-small").text.strip())
            price.append(full_price)  # Get apto's parking lot

        except:
            continue

    # condicional para parar de iterar entre pages
    if page < pages_number:
        receita = driver.find_element_by_xpath(
            f'//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/a')
        receita.click()

# fecha o chromedriver
driver.quit()

# cria um dataframe pandas e salva como um arquivo CSV
for i in range(0, len(neighbor)):
    combinacao = [link_imovel[i], address[i], neighbor[i], anunciante[i], area[i], tipo[i], room[i], bath[i], park[i],
                  price[i]]
    df = pd.DataFrame(combinacao)
    with open('VivaRealData2.csv', 'a', encoding='utf-16', newline='') as f:
        df.transpose().to_csv(f, encoding='iso-8859-1', header=False)

# Tempo de execução
toc = time.time()
get_time = round(toc - tic, 3)
print('Finished in ' + str(get_time) + ' seconds')
print(str(len(price)) + ' results!')
