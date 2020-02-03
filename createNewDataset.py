#!/usr/bin/env python
import random
import string

import requests
import json
import Constants
import os

def publishDataset(id, type):
    url = Constants.API_DATAVERSES_PUBLISHDATASET + str(id) + "/actions/:publish?type=" + type

    try:
        r = requests.post(url, headers=Constants.API_DATAVERSES_PUBLISHDATASET_HEADER)
        print(r.status_code)
        print(json.loads(r.text))
    except Exception as error:
        print('ERROR', error)


def createDataset():
    script_dir = os.path.dirname(__file__) + "/create-dataset.json"
    with open(script_dir, 'r+') as f:
        data = json.load(f)
        data['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value'] = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    try:
        r = requests.post(Constants.API_DATAVERSES_CREATEDATASET, data=json.dumps(data), headers=Constants.API_DATAVERSES_PUBLISHDATASET_HEADER)
        print(r.status_code)
        print(json.loads(r.text))
        res = json.loads(r.text)

        publishDataset(res['data']['id'], "major")
    except Exception as error:
        print('ERROR', error)


def updateDataset(doi):
    #url = Constants.API_DATAVERSES_PUBLISHDATASET + str(id) + "/versions/:draft"
    url = "https://dataverse-dev.ada.edu.au/api/datasets/:persistentId/versions/:draft?persistentId=" + doi
    #print(url)
    #print("https://dataverse-dev.ada.edu.au/api/datasets/2058/versions/:draf")
    script_dir = os.path.dirname(__file__) + "/dataset-update-metadata.json"
    with open(script_dir, 'r+') as f:
        data = json.load(f)
        data["metadataBlocks"]["citation"]["fields"][0]["value"] = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        print()


    try:
        r = requests.put(url, data=json.dumps(data), headers=Constants.API_DATAVERSES_PUBLISHDATASET_HEADER)

        print(r.status_code)
        print(json.loads(r.text))
        res = json.loads(r.text)
        #publishDataset(res['data']['id'], "major")
        pubUrl = "https://dataverse-dev.ada.edu.au/api/datasets/:persistentId/actions/:publish?persistentId=" + doi + "&type=major"
        try:
            r = requests.post(pubUrl, headers=Constants.API_DATAVERSES_PUBLISHDATASET_HEADER)
            print(r.status_code)
            print(json.loads(r.text))
        except Exception as error:
            print('ERROR', error)

    except Exception as error:
        print('ERROR', error)



for i in range(5):
    createDataset()

updateDataset("doi:10.5072/FK2/CDCUTL")
updateDataset("doi:10.5072/FK2/L6FSFU")
updateDataset("doi:10.5072/FK2/YRGC5F")
updateDataset("doi:10.5072/FK2/DHLVCJ")
updateDataset("doi:10.5072/FK2/BNA7IF")

