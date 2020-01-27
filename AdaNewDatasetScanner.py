import requests
import json
import env

API_METABASE_AUTHENTICATION_ENDPOINT = "https://dataverse-dev.ada.edu.au/metabase/api/session"

API_WP_AUTHENTICATION_ENDPOINT = "http://sw-dev.ada.edu.au:8085/wp-json/aam/v2/authenticate"

API_WP_VALIDATE = "http://sw-dev.ada.edu.au:8085/wp-json/aam/v1/validate-jwt"

API_DATASETS_QUERY = "https://dataverse-dev.ada.edu.au/metabase/api/card/295/query/json"

API_WP_CREATEPOSTS = "http://sw-dev.ada.edu.au:8085/wp-json/wp/v2/posts"

API_METABASE_AUTHENTICATION_HEADER = {
    'Content-Type': 'application/json'
}

API_METABASE_AUTHENTICATION_BODY = {
    "username": env.METABASE_USERNAME,
    "password": env.METABASE_PASSWORD
}

API_WP_AUTHENTICATION_HEADER = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

API_WP_AUTHENTICATION_BODY = {
    "username": env.WP_USERNAME,
    "password": env.WP_PASSWORD,
    "issueJWT": "true"
}

API_WP_VALIDATE_HEADER = {
    'Content-Type': 'application/json'
}

API_WP_CREATEPOTS_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded'
}



dataSets = []

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


def wpCreatePostBody(jwtToken, title, content):

    body = "title={title}&content={content}&status=publish&categories=8&aam-jwt={token}".format(title=title, content=content, token=jwtToken)
    return body

def fetchMetabaseSessionToken():
    try:
        r = requests.post(API_METABASE_AUTHENTICATION_ENDPOINT, data=json.dumps(API_METABASE_AUTHENTICATION_BODY), headers=API_METABASE_AUTHENTICATION_HEADER)
        if r.status_code == 200:
            token = (json.loads(r.text)["id"])
            return token
    except Exception as error:
        print('ERROR', error)


def fetchWPToken():
    try:
        r = requests.post(API_WP_AUTHENTICATION_ENDPOINT, data=json.dumps(API_WP_AUTHENTICATION_BODY), headers=API_WP_AUTHENTICATION_HEADER)
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
        r = requests.post(API_WP_VALIDATE, data=json.dumps(wpValidateBody(wpToken)), headers=API_WP_VALIDATE_HEADER)
        if r.status_code == 200:
            token = json.loads(r.text)['isValid']
            return token
    except Exception as error:
        print('ERROR', error)


def fetchDatasets():

    sessionToken = fetchMetabaseSessionToken()
    try:
        r = requests.post(API_DATASETS_QUERY, headers=datasetHeader(sessionToken))
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
        payload = wpCreatePostBody(fetchWPToken(), content[i]['dataset_title'], content[i]['dataset_description'])
        try:
            r = requests.post(API_WP_CREATEPOSTS, data=payload, headers=API_WP_CREATEPOTS_HEADER)
            print(r.status_code)
            print(json.loads(r.text))
        except Exception as error:
            print('ERROR', error)



createWPposts(dataSets)





