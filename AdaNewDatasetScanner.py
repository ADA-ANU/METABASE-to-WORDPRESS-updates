import urllib
import requests
import json
import Constants
import css
from datetime import datetime

newlyPublished = []
newlyUpdated = []
wpToken = ""


def datasetHeader(session_token):

    header = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-Metabase-Session': session_token
    }
    return header


def wpValidateBody(jwtToken):

    body = {
        "jwt": jwtToken
    }
    return body


def wpCreatePostBody(jwtToken, content, category):

    title = content['dataset_title']
    p = "<p style=" + css.p + ">"
    contents = p + "Dataset Link: <a href=" + urllib.parse.quote_plus(content['URL']) + " target='_blank'>Click Here</a></p>"
    if category == "26":
        contents += p + "Pubilication Date: " + content['publish date'] + "</p>"
    elif category == "27":
        contents += p + "Version: " + str(content['versionnumber']) + "." + str(content['minorversionnumber']) + "</p>"
        contents += p + "Update Date: " + content['publication date'] + "</p>"
    contents += p + "DOI: " + content['DOI'].split(":")[1] + "</p>"
    contents += "<p style=" + css.content + ">" + content['dataset_description'] + "</p>"
    body = "title={title}&content={content}&status=publish&categories={category}&aam-jwt={token}".format(title=title, content=contents, category=category, token=jwtToken)
    return body

def fetchMetabaseSessionToken():
    try:
        r = requests.post(Constants.API_METABASE_AUTHENTICATION_ENDPOINT, data=json.dumps(Constants.API_METABASE_AUTHENTICATION_BODY), headers=Constants.API_METABASE_AUTHENTICATION_HEADER)
        if r.status_code == 200:
            token = (json.loads(r.text)["id"])
            return token
    except Exception as error:
        print('ERROR', error)


def fetchWPToken():
    try:
        r = requests.post(Constants.API_WP_AUTHENTICATION_ENDPOINT, data=json.dumps(Constants.API_WP_AUTHENTICATION_BODY), headers=Constants.API_WP_AUTHENTICATION_HEADER)
        if r.status_code == 200:
            token = json.loads(r.text)['jwt']['token']
            return token
    except Exception as error:
        print('ERROR', error)


# def validateWPToken():
#
#     try:
#         r = requests.post(Constants.API_WP_VALIDATE, data=json.dumps(wpValidateBody(wpToken)), headers=Constants.API_WP_VALIDATE_HEADER)
#         if r.status_code == 200:
#             token = json.loads(r.text)['isValid']
#             return token
#     except Exception as error:
#         print('ERROR', error)


def checkPostsDate(url):

    try:
        r = requests.get(url, headers=Constants.API_WP_POSTS_HEADER)
        if r.status_code == 200:
            res = json.loads(r.text)
            for i in res:
                date = i['date']
                id = i['id']
                if dateDiff(date):
                    if id != 1598 and id != 1584:
                        payload = "status=draft&aam-jwt={token}".format(token=fetchWPToken())
                        try:
                            r = requests.post(Constants.API_WP_UPDATEPOSTS+str(id), data=payload, headers=Constants.API_WP_CREATEPOTS_HEADER)
                            print(r.status_code)
                        except Exception as error:
                            print('ERROR', error)

    except Exception as error:
        print('ERROR', error)



def dateDiff(date):
    dateNow = datetime.now()
    diff = dateNow - datetime.strptime(date, '%Y-%m-%dT%H:%M:%S')
    if diff.days > Constants.dateDiff:
        return True
    else:
        return False


def fetchDatasets():

    sessionToken = fetchMetabaseSessionToken()
    try:
        r = requests.post(Constants.API_DATASETS_QUERY_NEWPUBLICATION, headers=datasetHeader(sessionToken))
        if r.status_code == 200:
            res = json.loads(r.text)

            if len(res) > 0:
                for i in res:
                    newlyPublished.append(i)
    except Exception as error:
        print('ERROR', error)

    try:
        r = requests.post(Constants.API_DATASETS_QUERY_NEWPUPDATE, headers=datasetHeader(sessionToken))
        if r.status_code == 200:
            res = json.loads(r.text)

            if len(res) > 0:
                for i in res:
                    newlyUpdated.append(i)
    except Exception as error:
        print('ERROR', error)


def createWPposts(content, category):
    if len(content) > 0:
        for i in range(len(content)):
            if i < 1:
                print(content[i])
                payload = wpCreatePostBody(fetchWPToken(), content[i], category)
                print(payload)
                try:
                    r = requests.post(Constants.API_WP_CREATEPOSTS, data=payload, headers=Constants.API_WP_CREATEPOTS_HEADER)
                    print(r.status_code)
                    #print(json.loads(r.text))
                except Exception as error:
                    print('ERROR', error)


checkPostsDate(Constants.API_WP_GETPOSTS_PUBLISH)
checkPostsDate(Constants.API_WP_GETPOSTS_UPDATE)
fetchDatasets()
#createWPposts(newlyPublished, "26")
createWPposts(newlyUpdated, "27")





