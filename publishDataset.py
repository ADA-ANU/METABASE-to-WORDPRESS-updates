import requests
import json
import Constants
import css
from datetime import datetime
import pytz
from time import sleep


def currentDateTime():
    d_naive = datetime.now()
    timezone = pytz.timezone("Australia/ACT")
    d_aware = timezone.localize(d_naive).strftime('%Y-%m-%d %H:%M:%S')
    return d_aware


def publishDataset(doi, type):
    # url = Constants.API_DATAVERSES_PUBLISHDATASET + doi + "/actions/:publish?type=" + type
    pubUrl = "https://dataverse.ada.edu.au/api/datasets/:persistentId/actions/:publish?persistentId=doi:" + doi + "&type=" + type
    # pubUrl = "https://dataverse-dev.ada.edu.au/api/datasets/:persistentId/actions/:publish?persistentId=doi:10.5072/FK2/MM1V7P&type=major"
    try:
        # , headers = Constants.API_DATAVERSES_PUBLISHDATASET_HEADER
        r = requests.post(pubUrl, headers=Constants.API_DATAVERSES_PUBLISHDATASET_HEADER)
        print(r.status_code)
        print(json.loads(r.text))
    except Exception as error:
        print('ERROR', error)


def main():
    print(currentDateTime() + " Executing...")
    res = ["10.26193/CKC649", "10.26193/K8AHOY", "10.26193/JQXVRQ", "10.26193/XBF63J", "10.26193/Y7HBNW", "10.26193/AGIDRG", "10.26193/NAZZBG", "10.26193/SA9G1E", "10.26193/2H6BND", "10.26193/Z4OGT6",
           "10.26193/6W1R4F", "10.26193/LB2QTN", "10.26193/SOYOV2", "10.26193/N9FSVR", "10.26193/GOFLFC", "10.26193/TZRDNP", "10.26193/KEJTOO", "10.26193/VVH5NW", "10.26193/ERBD94", "10.26193/AG50NU",
           "10.26193/PZDCBX", "10.26193/4SCG3F", "10.26193/P7PVBQ", "10.26193/GQKPH1", "10.26193/EJRYSI", "10.26193/AYTRNG", "10.26193/BGG553", "10.26193/ECTVFO", "10.26193/K7RB0K", "10.26193/TA5KY0"]
    for i in res:
        publishDataset(i, "major")
    # checkPostsDate(Constants.API_WP_GETPOSTS_PUBLISH)
    # checkPostsDate(Constants.API_WP_GETPOSTS_UPDATE)
    # fetchDatasets()
    # print(currentDateTime() + " There are " + str(len(newlyPublished)) + " Newly Published Dataset.")
    # print(currentDateTime() + " There are " + str(len(newlyUpdated)) + " Newly Updated Dataset.")
    # if len(newlyPublished) > 0:
    #     print(currentDateTime() + " Ada WP Bot is uploading the Newly Published Dataset.")
    #     createWPposts(newlyPublished, Constants.CATEGORY_NEWPOST)
    # if len(newlyUpdated) > 0:
    #     print(currentDateTime() + " Ada WP Bot is uploading Recently Updated Dataset.")
    #     createWPposts(newlyUpdated, Constants.CATEGORY_UPDATEDPOST)
    # checkPostsStatus(Constants.API_WP_GETPOSTS_PUBLISH)
    # checkPostsStatus(Constants.API_WP_GETPOSTS_UPDATE)


if __name__ == "__main__":
    main()