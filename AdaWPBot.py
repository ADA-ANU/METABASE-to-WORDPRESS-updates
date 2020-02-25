#!/usr/bin/env python
import urllib
import requests
import json
import Constants
import css
from datetime import datetime
import tweepy
import pytz

newlyPublished = []
newlyUpdated = []
wpToken = ""
waitingToTweet = []
Pcount = 0
Ucount = 0


def currentDateTime():
    d_naive = datetime.now()
    timezone = pytz.timezone("Australia/ACT")
    d_aware = timezone.localize(d_naive).strftime('%Y-%m-%d %H:%M:%S')
    return d_aware


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


def smart_truncate(content, length=100, suffix=' ...'):
    if len(content) <= length:
        return content
    else:
        return ' '.join(content[:length+1].split(' ')[0:-1]) + suffix


def wpCreatePostBody(jwtToken, content, category):

    title = content['dataset_title']
    p = "<p style=" + css.p + ">"
    contents = p + "Dataset Link: <a href=" + content['URL'] + " target='_blank'>Click Here</a></p>"
    if category == Constants.CATEGORY_NEWPOST:
        contents += p + "Pubilication Date: " + content['publish date'] + "</p>"
    elif category == Constants.CATEGORY_UPDATEDPOST:
        contents += p + "Version: " + str(content['versionnumber']) + "." + str(content['minorversionnumber']) + "</p>"
        contents += p + "Update Date: " + content['publication date'] + "</p>"
    contents += p + "DOI: " + content['DOI'].split(":")[1] + "</p>"
    contents += "<p style=" + css.content + ">" + content['dataset_description'] + "</p>"
    excerpt = smart_truncate(content['dataset_description'], 200)

    #body = "title={title}&content={content}&status=publish&categories={category}&aam-jwt={token}".format(title=title, content=contents, category=category, token=jwtToken)
    body = {
            "title": title,
            "status": "publish",
            "content": contents,
            "categories": category,
            'aam-jwt': jwtToken,
            'excerpt': excerpt
            }
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
        else:
            print(json.loads(r.text))
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
                    if id != 2047 and id != 2049:
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
    if diff.days >= Constants.dateDiff:
        return True
    else:
        return False


def fetchDatasets():
    print(currentDateTime() + " Ada WP Bot is fetching data from Metabase")
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
    print(currentDateTime() + " Fetch done.")


def createWPposts(content, category):
    global Pcount, Ucount

    for i in range(len(content)):
        print("Uploading " + str(i+1) + " post.")
        payload = wpCreatePostBody(fetchWPToken(), content[i], category)
        try:
            r = requests.post(Constants.API_WP_CREATEPOSTS, data=payload, headers=Constants.API_WP_CREATEPOTS_HEADER)
            if category == Constants.CATEGORY_NEWPOST and r.status_code == 200 or r.status_code == 201:
                Pcount += 1
            if category == Constants.CATEGORY_UPDATEDPOST and r.status_code == 200 or r.status_code == 201:
                Ucount += 1
            print(r.status_code)
        except Exception as error:
            print('ERROR', error)
    if category == Constants.CATEGORY_NEWPOST:
        print(currentDateTime() + " " + str(Pcount) + " Newly Published Dataset have been updated.")
    elif category == Constants.CATEGORY_UPDATEDPOST:
        print(currentDateTime() + " " + str(Ucount) + " Recently Updated Dataset have been updated.")


def createTwitterAPI():
    # authentication of consumer key and secret

    auth = tweepy.OAuthHandler(Constants.consumer_key, Constants.consumer_secret)

    # authentication of access token and secret
    auth.set_access_token(Constants.access_token, Constants.access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    try:
        api.verify_credentials()
    except:
        print("Error during authentication")

    return api


def main():
    print(currentDateTime() + " Executing...")
    checkPostsDate(Constants.API_WP_GETPOSTS_PUBLISH)
    checkPostsDate(Constants.API_WP_GETPOSTS_UPDATE)
    fetchDatasets()
    print(currentDateTime() + " There are " + str(len(newlyPublished)) + " Newly Published Dataset.")
    print(currentDateTime() + " There are " + str(len(newlyUpdated)) + " Newly Updated Dataset.")
    if len(newlyPublished) > 0:
        print(currentDateTime() + " Ada WP Bot is uploading the Newly Published Dataset.")
        createWPposts(newlyPublished, Constants.CATEGORY_NEWPOST)
    if len(newlyUpdated) > 0:
        print(currentDateTime() + " Ada WP Bot is uploading Recently Updated Dataset.")
        createWPposts(newlyUpdated, Constants.CATEGORY_UPDATEDPOST)


if __name__ == "__main__":
    main()




