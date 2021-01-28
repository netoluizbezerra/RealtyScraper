import scrapy
from selenium import webdriver
from scrapy.selector import Selector
from selenium.webdriver.chrome.options import Options
import time
from ..utils import get_random_agent
from ..clean_json import clean_json
from shutil import which

USER_AGENT = get_random_agent()


class ImoveisSpider(scrapy.Spider):
    name = 'extract_features'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    main = 'www.vivareal.com.br'
    allowed_domains = [main]
    handle_httpstatus_list = [403, 429]
    start_urls = ['https://vivareal.com.br']
    links = clean_json()

    first_page = 'https://' + main + links[0]


# Define a constructor:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_path = which('chromedriver')
        self.driver = webdriver.Chrome(executable_path=chrome_path)
#       self.driver.set_window_size(1920, 1080)
        self.driver.get(self.first_page)
        self.maxPages = len(self.links)
        self.link_imovel = []

    def parse(self, response):
        for page in range(1, self.maxPages):
            time.sleep(2)
            html = self.driver.page_source
            response_obj = Selector(text=html)

            # Extracting Features
            #logging.info(response.url)
            # endereço:
            try:
                end = response_obj.xpath("//div[contains(@class, 'title__address-wrapper')]/p/text()").get()
            except:
                end = None
            # Atributos Principais:
            try:
                area_tot = int(response_obj.xpath(
                    "//li[contains(@class, 'features__item features__item--area js-area')]/span/text()").get())
            except:
                area_tot = None

            try:
                banheiros = int(response_obj.xpath(
                    "//li[contains(@class, 'features__item features__item--bathroom js-bathrooms')]/span/text()").get())
            except:
                banheiros= None

            try:
                vagas = int(response_obj.xpath(
                    "//li[contains(@class, 'features__item features__item--parking js-parking')]/span/text()").get())
            except:
                vagas = None

            try:
                quartos = int(response_obj.xpath(
                    "//li[contains(@class, 'features__item features__item--bedroom js-bedrooms')]/span/text()").get())
            except:
                quartos = None

            try:
                suites = int(response_obj.xpath(
                    "//small[contains(@class, 'feature__extra-info')]/text()").get())
            except:
                suites = None

            # URL:
            try:
                url = response_obj.xpath(
                    "//meta[@property='og:url']/@content").get()
            except:
                url = None

            # Título:
            try:
                titulo = response_obj.xpath(
                    "//h3[contains(@class, 'description__title js-description-title')]/text()").get()
            except:
                titulo=None

            # Preço:
            try:
                preco = response_obj.xpath(
                    "//h3[contains(@class, 'price__price-info js-price-sale')]/text()").get()
                preco = preco.replace('R$', '').strip()
                preco = int(preco.replace('.', ''))
            except:
                preco=None

            # Imobiliária:
            try:
                imob = response_obj.xpath(
                    "//a[contains(@class, 'publisher__name')]/text()").get()
                imob = imob.replace('\n', ' ').strip()
            except:
                imob=None
            # Código:
            #cod = response_obj.xpath(
                #"//p[contains(@class, 'description__text')]").get()
            try:
                cod = (url.split("center=")[1]).split("&zoom")[0]
            except:
                cod = None

            # Descricao
            try:
                description_srt = ''
                description = response_obj.xpath("//p[contains(@class, 'description__text')]")
                for desc_line in description:
                    description_srt += desc_line.xpath('./text()').get()
            except:
                description_srt = None


            # Coordenadas Geograficas
            try:
                latitude = response_obj.xpath("//meta[contains(@property, 'latitude')]/@content").get()
                longitude = response_obj.xpath("//meta[contains(@property, 'longitude')]/@content").get()
            except:
                latitude = None
                longitude = None

            # Amenities:
            try:
                amenities_str = ''
                amenities_temp = response_obj.xpath(
                    "//ul[contains(@class, 'amenities__list')]/li"
                )
                for amenity in amenities_temp:
                    amenities_str += amenity.xpath("./text()").get()
            except:
                amenities_str = None

            yield {
                'price': preco,
                'titulo': titulo,
                'desc': description_srt,
                'amen': amenities_str,
                'end': end,
                'area_tot': area_tot,
                'banheiros': banheiros,
                'vagas': vagas,
                'quartos': quartos,
                'suites': suites,
                'preco': preco,
                'imob': imob,
                'url': url,
                'cod': cod,
                'latitude': latitude,
                'longitude': longitude
            }

            if page < self.maxPages:
                next_page = 'https://' + self.main + self.links[page]
                self.driver.get(next_page)

        self.driver.close()
