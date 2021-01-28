import scrapy
from scrapy.selector import Selector
import time
from ..utils import get_random_agent
from scrapy_selenium import SeleniumRequest

USER_AGENT = get_random_agent()


class ImoveisSpider(scrapy.Spider):
    name = 'imoveis'
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
    main = 'www.vivareal.com.br'
    allowed_domains = [main]
    first_page = 'https://' + main + '/aluguel/distrito-federal/brasilia/?pagina=1'
    handle_httpstatus_list = [403, 429]
    start_urls = ['https://vivareal.com.br']

    def start_requests(self):
        yield SeleniumRequest(
            url='https://www.vivareal.com.br/aluguel/distrito-federal/brasilia/?pagina=1',
            wait_time=3,
            callback=self.parse
        )

    def parse(self, response):
        for i in range(95):
            driver = response.meta['driver']
            html = driver.page_source
            response_obj = Selector(text=html)

            links = response_obj.xpath(
                "//div[contains(@data-type,'property')]//a[contains(@class, 'property-card__labels-container js-main')]"
            )
            for link in links:
                yield {
                    'url': link.xpath("./@href").get()
                }
            time.sleep(10)
            self.log('pag numero {}'.format(i))
            next = driver.find_element_by_xpath(
                     f'//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/a'
            )
            next.click()





    # {'url': '/imovel/apartamento-2-quartos-bom-retiro-centro-sao-paulo-com-garagem-42m2-aluguel-RS1900-id-2491761679/?_
    #  _vt = lnv:a
    # '}
    # 2021 - 01 - 07
    # 05: 17:28[scrapy.core.scraper]
    # DEBUG: Scraped
    # from < 200
    # https: // www.vivareal.com.br / aluguel / sp / sao - paulo
    #           /?__vt = lnv % 3
    # Aa >
    # {'url': '/imovel/apartamento-3-quartos-vila-clementino-zona-sul-sao-paulo-com-garagem-104m2-aluguel-RS4100-id-25064
    #  93999 /?__vt = lnv:a
    # '}
    # 2021 - 01 - 07
    # 05: 17:28[scrapy.core.scraper]
    # DEBUG: Scraped
    # from < 200
    # https: // www.vivareal.com.br / aluguel / sp / sao - paulo
    #           /?__vt = lnv % 3
    # Aa >
    # {'url': '/imovel/sala-comercial-vila-mariana-zona-sul-sao-paulo-com-garagem-46m2-aluguel-RS1499-id-2499877324/?__vt
    # = lnv:a
    # '}
    # 2021 - 01 - 07
    # 05: 17:28[scrapy.core.scraper]
    # DEBUG: Scraped
    # from < 200
    # https: // www.vivareal.com.br / aluguel / sp / sao - paulo
    #           /?__vt = lnv % 3
    # Aa >
    # {'url': '/imovel/apartamento-2-quartos-vila-madalena-zona-oeste-sao-paulo-com-garagem-72m2-aluguel-RS3600-id-249929
    #  1439 /?__vt = lnv:a
    # '}

    # def parse(self, response):
    #     for page in range(1, self.pageNumber):
    #         time.sleep(2)
    #         data = self.driver.execute_script("return document.getElementsByTagName('html')[0].innerHTML")
    #         soup_complete_source = BeautifulSoup(data.encode('utf-8'), "lxml")
    #         soup = soup_complete_source.find(class_='results-list js-results-list')
    #
    #         for line in soup.findAll(class_="js-card-selector"):
    #             full_link = line.find(class_='property-card__main-info').a.get('href')
    #             print(full_link)
    #             self.link_imovel.append(full_link)
    #
    #         if page < self.pageNumber:
    #             receita = self.driver.find_element_by_xpath(
    #                 f'//*[@id="js-site-main"]/div[2]/div[1]/section/div[2]/div[2]/div/ul/li[9]/a')
    #             receita.click()
    #
