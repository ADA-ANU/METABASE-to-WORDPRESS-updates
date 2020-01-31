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


def createDataset(name):
    script_dir = os.path.dirname(__file__) + "/create-dataset.json"
    with open(script_dir, 'r+') as f:
        data = json.load(f)
        data['datasetVersion']['metadataBlocks']['citation']['fields'][0]['value'] = name

    try:
        r = requests.post(Constants.API_DATAVERSES_CREATEDATASET, data=json.dumps(data), headers=Constants.API_DATAVERSES_PUBLISHDATASET_HEADER)
        print(r.status_code)
        print(json.loads(r.text))
        res = json.loads(r.text)
        publishDataset(res['data']['id'], "major")
    except Exception as error:
        print('ERROR', error)


def updateDataset(id):
    url = Constants.API_DATAVERSES_PUBLISHDATASET + str(id) + "/versions/:draft"
    print(url)
    print("https://dataverse-dev.ada.edu.au/api/datasets/2058/versions/:draf")
    script_dir = os.path.dirname(__file__) + "/create-dataset.json"
    with open(script_dir, 'r+') as f:
        data = json.load(f)

    try:
        r = requests.put(url, headers=Constants.API_DATAVERSES_PUBLISHDATASET_HEADER)
        print(r.status_code)
        print(json.loads(r.text))
        res = json.loads(r.text)
        # publishDataset(res['data']['id'], "major")
    except Exception as error:
        print('ERROR', error)


updateDataset("2058")
#createDataset("MJP's test")


