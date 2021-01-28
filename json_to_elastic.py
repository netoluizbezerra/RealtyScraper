from elasticsearch import Elasticsearch
from datetime import datetime
import json
import os

data_provider = input('Input Data Provider: ')

def json_to_elastic(data_provider):
    date = datetime.today().strftime('%Y-%m-%d')
    path = "/home/luizneto/Documents/inrealty_project/{}".format(data_provider)
    os.chdir(path)

    with open("{}.json".format(data_provider), "r+") as jsonFile:
        listing = json.load(jsonFile)

    _id = list()
    [_id.append('{}_{}_{}'.format(date, data_provider, i)) for i in range(len(listing))]

    es = Elasticsearch(
        ['https://search-products-aqzpwd5sntugxqsd66e6z67ze4.us-east-2.es.amazonaws.com'])
    try:
        for i in range(len(listing)):
            es.index(index='webimoveis', id=_id[i], body=listing[i])
            print('{} loop'.format(i))
        print("SUCCESS uploading: {}, captured {} ".format(data_provider, date))
        os.remove("{}.json".format(data_provider))

    except:
        print("FAILURE uploading {} ".format(data_provider, date))


json_to_elastic(data_provider)
