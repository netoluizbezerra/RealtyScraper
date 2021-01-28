from scrapy.selector import Selector
import time
import json as json
import undetected_chromedriver as uc
import re

link = 'https://www.wimoveis.com.br/imoveis-distrito-federal-goias.html'

driver = uc.Chrome()
driver.get(link)
html_temp = driver.page_source
response_obj_temp = Selector(text=html_temp)

listing_size = response_obj_temp.xpath(
    "//h1[contains(@class, 'list-result-title')]/text()"
).get()
listing_size = float(re.sub("[^0-9]", "", listing_size))

i_max = (listing_size/21).__round__()
i = 0
temp = []
go = True

while i < i_max:
    i += 1
    time.sleep(2)
    html = driver.page_source
    response_obj = Selector(text=html)
    links = response_obj.xpath(
        "//div[contains(@data-qa, 'posting ')]"
    )

    for link in links:
        temp.append({'url': 'https://www.wimoveis.com.br{}'.format(link.xpath("./@data-to-posting").get())})

    try:
        _next = driver.find_element_by_xpath(
            f'//a[contains(@aria-label, "Siguiente")]'
        )
        print('Page Scraped')
        _next.click()
        go = True
    except:
        print('End of Scraping')
        go = False

with open('links.json', 'w') as f:
    json.dump(temp, f)

