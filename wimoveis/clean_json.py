import json
import os


def clean_json():
    path = '/home/luizneto/Documents/inrealty_project/wimoveis/'
    os.chdir(path)

    with open("links.json", "r+") as jsonFile:
        urls = json.load(jsonFile)
    list_temp = []
    for i in range(0, len(urls)):
        list_temp.append(urls[i]['url'])
    return list(set(list_temp))





