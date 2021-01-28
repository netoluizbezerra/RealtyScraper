import time
from scrapy.selector import Selector
import json
import re
import undetected_chromedriver as uc
from wimoveis.clean_json import clean_json

link = 'https://www.wimoveis.com.br/propriedades/adriana-muniz-99141-0147-2953389041.html'

links = clean_json()
driver = uc.Chrome()
temp = []
i = -1


for link in links:
    i+=1
    print('imovel {}'.format(i))
    driver.get(link)
    time.sleep(2)
    html = driver.page_source
    response_obj = Selector(text=html)

    try:
        try:
            end1 = response_obj.xpath("//h2[@class='title-location']/text()").get()
            end2 = response_obj.xpath("//h2[@class='title-location']/span/text()").get()
            end = '{}{}'.format(end1, end2)
        except:
            end = response_obj.xpath("//h2[@class='title-location']/text()").get()
    except:
        end = None

    attr = response_obj.xpath("//li[contains(@class, 'icon-feature')]").getall()
    listToStr = ' '.join([str(elem) for elem in attr])

    area_total_check = 'icon-stotal'
    area_util_check = 'icon-scubierta'
    vagas_check = 'icon-cochera'
    banheiros_check = 'icon-bano'
    quartos_check = 'icon-dormitorio'
    suites_check = 'icon-toilete'
    idade_imovel_check = 'icon-antiguedad'

    if area_total_check in listToStr:
        area_total = int(re.sub("[^0-9]", "", attr[0]))
        del attr[0]
    else:
        area_total = None

    if area_util_check in listToStr:
        area_util = int(re.sub("[^0-9]", "", attr[0]))
        del attr[0]
    else:
        area_util = None

    if banheiros_check in listToStr:
        banheiros = int(re.sub("[^0-9]", "", attr[0]))
        del attr[0]
    else:
        banheiros = None

    if vagas_check in listToStr:
        vagas = int(re.sub("[^0-9]", "", attr[0]))
        del attr[0]
    else:
        vagas = None

    if quartos_check in listToStr:
        quartos = int(re.sub("[^0-9]", "", attr[0]))
        del attr[0]
    else:
        quartos = None

    if suites_check in listToStr:
        suites = int(re.sub("[^0-9]", "", attr[0]))
        del attr[0]
    else:
        suites = None

    if idade_imovel_check in listToStr:
        if 'novo' in attr[0]:
            idade_imovel = 0
        else:
            idade_imovel = re.sub("[^0-9]", "", attr[0])
            del attr[0]
    else:
        idade_imovel = None

    # URL:
    try:
        url = link
    except:
        url = None

    # Título:
    try:
        titulo = response_obj.xpath(
            "//*[@id='article-container']/section[1]/div[1]/h1/text()").get()
    except:
        titulo = None

    # Preço:
    try:
        preco = response_obj.xpath(
            "//*[@id='contact-form-sticky']/div[1]/div[1]/div/div[1]/div[2]/span/span/text()").get()
        preco = preco.replace('R$', '').strip()
        preco = int(preco.replace('.', ''))
    except:
        preco = None

    # IPTU
    try:
        extras = response_obj.xpath(
            "//div[@class='block-expensas block-row']/span/text()").getall()

        extras_str = response_obj.xpath(
            "//div[@class='block-expensas block-row']/text()").getall()

        listToStr_extras = ' '.join([str(elem) for elem in extras_str])

        if "Cond" and "IPTU" in listToStr_extras:
            cond = extras[0]
            cond = cond.replace('R$', '').strip()
            cond = int(cond.replace('.', ''))

            iptu = extras[1]
            iptu = iptu.replace('R$', '').strip()
            iptu = int(iptu.replace('.', ''))

        elif "Cond" in listToStr_extras:
            cond = extras[0]
            cond = cond.replace('R$', '').strip()
            cond = int(cond.replace('.', ''))

            iptu = None

        elif "IPTU" in listToStr_extras:
            iptu = extras[0]
            iptu = iptu.replace('R$', '').strip()
            iptu = int(iptu.replace('.', ''))

            cond = None

    except:
        iptu = None
        cond = None

    # Imobiliária:
    try:
        imob = response_obj.xpath(
            "//h5[contains(@class, 'PublisherTitle')]/text()").get()
        imob = imob.replace('\n', ' ').strip()
    except:
        imob = None

    # Descricao
    try:
        "//div[@id='longDescription']"
        description = response_obj.xpath("//*[@id='longDescription']/div/text()").getall()
        description_srt = ''
        for desc_line in description:
            description_srt += desc_line
    except:
        description_srt = None

    # Coordenadas Geograficas
    try:
        coord_str = response_obj.xpath("//img[contains(@class, 'static-map')]/@src").get()
        coordinates = (coord_str.split("center=")[1]).split("&zoom")[0].split(',')
        latitude = coordinates[0]
        longitude = coordinates[1]

    except:
        latitude = None
        longitude = None

    # Amenities:
    try:
        amenities_str = ''
        amenities_temp = response_obj.xpath(
            "//ul[contains(@class, 'sc-bqyKva ehfErK')]/li/h4/text()"
        ).getall()
        for amenity in amenities_temp:
            amenities_str += amenity
    except:
        amenities_str = None


    temp.append({
        'preco': preco,
        'iptu': iptu,
        'condominio': cond,
        'titulo': titulo,
        'desc': description_srt,
        'amen': amenities_str,
        'end': end,
        'area_tot': area_total,
        'banheiros': banheiros,
        'vagas': vagas,
        'quartos': quartos,
        'suites': suites,
        'imob': imob,
        'url': url,
        'latitude': latitude,
        'longitude': longitude
    })


driver.close()
with open('webimoveis.json', 'w') as f:
    json.dump(temp, f)







