import requests
import json
import Constants

dataSets = []


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


def wpCreatePostBody(jwtToken, title, content,category):

    body = "title={title}&content={content}&status=publish&categories={category}&aam-jwt={token}".format(title=title, content=content, category=category, token=jwtToken)
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


wpToken = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1Nzk4MjYzMTcsImlzcyI6Imh0dHA6XC9cL3N3LWRldi5hZGEuZWR1LmF1OjgwODUiLCJleHAiOjE1Nzk5MTI3MTcsImp0aSI6IjZkMDc2NDFhLTkwMDctNDc4NS04ZGY5LTAxMzEyZTUwOWY5YyIsInVzZXJJZCI6MTAsInJldm9jYWJsZSI6dHJ1ZSwicmVmcmVzaGFibGUiOmZhbHNlfQ.npMws6jPLUwyc0VfTem1RyHlgPPVXV_jlUtwk-hfzvg"
    #fetchWPToken()


def validateWPToken():
    print(wpToken)
    try:
        r = requests.post(Constants.API_WP_VALIDATE, data=json.dumps(wpValidateBody(wpToken)), headers=Constants.API_WP_VALIDATE_HEADER)
        if r.status_code == 200:
            token = json.loads(r.text)['isValid']
            return token
    except Exception as error:
        print('ERROR', error)


def fetchDatasets():

    sessionToken = fetchMetabaseSessionToken()
    try:
        r = requests.post(Constants.API_DATASETS_QUERY, headers=datasetHeader(sessionToken))
        if r.status_code == 200:
            res = json.loads(r.text)

            if len(res) > 0:
                for i in res:
                    dataSets.append(i)
    except Exception as error:
        print('ERROR', error)


def createWPposts(content):
    fetchDatasets()
    for i in range(len(content)):
        #if i < 1:
        print(content[i])
        payload = wpCreatePostBody(fetchWPToken(), content[i]['dataset_title'], content[i]['dataset_description'], "26")
        try:
            r = requests.post(Constants.API_WP_CREATEPOSTS, data=payload, headers=Constants.API_WP_CREATEPOTS_HEADER)
            print(r.status_code)
            print(json.loads(r.text))
        except Exception as error:
            print('ERROR', error)



createWPposts(dataSets)





