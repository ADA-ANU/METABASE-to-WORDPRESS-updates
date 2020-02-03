#!/usr/bin/env python
import urllib
import requests
import json
import Constants
import css
from datetime import datetime
import tweepy

from pyDataverse.api import Api
from pyDataverse.models import Dataverse

newlyPublished = []
newlyUpdated = []
wpToken = ""
waitingToTweet = []


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
    print(jwtToken)
    title = content['dataset_title']
    p = "<p style=" + css.p + ">"
    contents = p + "Dataset Link: <a href=" + content['URL'] + " target='_blank'>Click Here</a></p>"
    if category == "26":
        contents += p + "Pubilication Date: " + content['publish date'] + "</p>"
    elif category == "27":
        contents += p + "Version: " + str(content['versionnumber']) + "." + str(content['minorversionnumber']) + "</p>"
        contents += p + "Update Date: " + content['publication date'] + "</p>"
    contents += p + "DOI: " + content['DOI'].split(":")[1] + "</p>"
    contents += "<p style=" + css.content + ">" + content['dataset_description'] + "</p>"
    #body = "title={title}&content={content}&status=publish&categories={category}&aam-jwt={token}".format(title=title, content=contents, category=category, token=jwtToken)
    body = {
            "title": title,
            "status": "publish",
            "content": contents,
            "categories": category,
            'aam-jwt': jwtToken
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
    if diff.days >= Constants.dateDiff:
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

            print(content[i])
            payload = wpCreatePostBody(fetchWPToken(), content[i], category)
            try:
                r = requests.post(Constants.API_WP_CREATEPOSTS, data=payload, headers=Constants.API_WP_CREATEPOTS_HEADER)
                print(r.status_code)
                print(json.loads(r.text))
            except Exception as error:
                print('ERROR', error)


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

def updateTwitter(content, category):

    api = createTwitterAPI()
    tweet = ""
    if len(content) > 0:
        for i in range(len(content)):

            temp = tweetCompositionSimple(content[i], i, category)

            if len(temp) > 479:
                tempT = temp[0:479] + "..."
                waitingToTweet.append(tempT)
            elif len(tweet) > 0 and len(tweet + tweetCompositionSimple(content[i], i, category)) > 479:
                waitingToTweet.append(tweet)
                tweet = tweetCompositionSimple(content[i], i, category)
                if i == len(content) - 1:
                    waitingToTweet.append(tweet)
            else:
                tweet += tweetCompositionSimple(content[i], i, category)
                if i == len(content) - 1:
                    waitingToTweet.append(tweet)

    # update the status

    if len(waitingToTweet) > 0:
        for i in waitingToTweet:

            try:
                api.update_status(status=i)
            except Exception as error:
                print(error)

    waitingToTweet.clear()



def tweetComposition(content, num, category):
    title = content['dataset_title']
    description = content['dataset_description']
    url = content['URL']
    doi = content['DOI']
    if category == "27":
        publicationDate = content['publication date']
        version = str(content['versionnumber']) + "." + str(content['minorversionnumber'])
        if num == 0:
            tweet = "Recently updated datasets on our Dataverse: " + "\r\n" \
                + "\r\n" \
                + str(num+1) + ". " + "Title: " + title + " (" + doi + ") " + "V" + version + "\r\n" \
                + "Publication Date: " + publicationDate + "\r\n" \
                + "URL: " + url + "\r\n" \
                + "Description: " + description + "\r\n"

        else:

            tweet = str(num + 1) + ". " + "Title: " + title + " (" + doi + ") " + "V" + version + "\r\n" \
                + "Publication Date: " + publicationDate + "\r\n" \
                + "URL: " + url + "\r\n" \
                + "Description: " + description + "\r\n"

    else:
        publicationDate = content['publish date']
        if num == 0:
            tweet = "Newly published datasets on our Dataverse: " + "\r\n" \
                + "\r\n" \
                + str(num + 1) + ". " + "Title: " + title + " (" + doi + ")" + "\r\n" \
                + "Publication Date: " + publicationDate + "\r\n" \
                + "URL: " + url + "\r\n" \
                + "Description: " + description + "\r\n"

        else:
            tweet = str(num + 1) + ". " + "Title: " + title + " (" + doi + ")" + "\r\n" \
                + "Publication Date: " + publicationDate + "\r\n" \
                + "URL: " + url + "\r\n" \
                + "Description: " + description + "\r\n"

    return tweet


def tweetCompositionSimple(content, num, category):
    title = content['dataset_title']
    description = content['dataset_description']
    url = content['URL']
    doi = content['DOI']

    if category == "27":
        publicationDate = content['publication date']
        version = str(content['versionnumber']) + "." + str(content['minorversionnumber'])
        if num == 0:
            tweet = "Recently updated datasets on our Dataverse: " + "\r\n" \
                + "\r\n" \
                + str(num+1) + ". " + title + " (" + doi + ") " + "V" + version + "\r\n" \
                + url + "\r\n"
        else:
            tweet = str(num + 1) + ". " + title + " (" + doi + ") " + "V" + version + "\r\n" \
                + url + "\r\n"


    elif category == "26":
        publicationDate = content['publish date']
        if num == 0:
            tweet = "Newly published datasets on our Dataverse: " + "\r\n" \
                + "\r\n" \
                + str(num + 1) + ". " + title + " (" + doi + ")" + "\r\n" \
                + url + "\r\n"

        else:
            tweet = str(num + 1) + ". " + title + " (" + doi + ")" + "\r\n" \
                + url + "\r\n" \

    return tweet


def main():
    print("Executing...")
    checkPostsDate(Constants.API_WP_GETPOSTS_PUBLISH)
    checkPostsDate(Constants.API_WP_GETPOSTS_UPDATE)
    fetchDatasets()
    createWPposts(newlyPublished, "26")
    createWPposts(newlyUpdated, "27")
    updateTwitter(newlyPublished, "26")
    updateTwitter(newlyUpdated, "27")


if __name__ == "__main__":
    main()




