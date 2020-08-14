#!/usr/bin/env python
import urllib
import requests
import json
import Constants
import css
from datetime import datetime
import pytz
from time import sleep

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
        else:
            print("Failed to fetch Metabase token.")
    except Exception as error:
        print('ERROR', error)
        print("Failed to fetch Metabase token.")


def fetchWPToken():
    try:
        r = requests.post(Constants.API_WP_AUTHENTICATION_ENDPOINT, data=json.dumps(Constants.API_WP_AUTHENTICATION_BODY), headers=Constants.API_WP_AUTHENTICATION_HEADER)
        if r.status_code == 200:
            token = json.loads(r.text)['jwt']['token']
            return token
        else:
            print(json.loads(r.text))
            print("Failed to fetch WP token.")
    except Exception as error:
        print('ERROR', error)
        print("Failed to fetch WP token.")


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


def checkPostsStatus(url):
    print(currentDateTime() + " Checking posts' status...")
    try:
        # with urlopen("https://sunlightlabs.github.io/congress/legislators?api_key='(myapikey)") as conn:
        #     r = conn.read()
        #     # encoding = r.info().get_content_charset('utf-8')
        #     j = json.loads(r)
        #     print(j)
        r = requests.get(url, headers=Constants.API_FETCH_HEADER)
        if r.status_code == 200:
            res = json.loads(r.text)
            for i in res:
                postid = i['id']
                postname = i['title']['rendered']
                content = i['content']['rendered']
                doi = content.split('persistentId=doi:')[1].split('\"')[0]
                try:
                    r = requests.get(Constants.API_DV_DATASETINFO+doi, headers=Constants.API_WP_POSTS_HEADER)
                    if r.status_code == 200:
                        res = json.loads(r.text)
                        if 'latestVersion' not in res['data']:
                            print(postname + "(" + str(postid) + ")" + " is going to be set to draft.")
                            payload = "status=draft&aam-jwt={token}".format(token=fetchWPToken())
                            try:
                                r = requests.post(Constants.API_WP_UPDATEPOSTS+str(postid), data=payload, headers=Constants.API_WP_CREATEPOTS_HEADER)
                                if r.status_code == 200:
                                    print("Done.")
                                else:
                                    print("Failed to set the post to draft.")
                            except Exception as error:
                                print('ERROR', error)
                except Exception as error:
                    print('ERROR', error)

            print(currentDateTime() + " Status check finished.")

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
        else:
            print("Failed to fetch newly published data from Metabase.")

    except Exception as error:
        print('ERROR', error)
        print("Failed to fetch newly published data from Metabase.")

    try:
        r = requests.post(Constants.API_DATASETS_QUERY_NEWPUPDATE, headers=datasetHeader(sessionToken))
        if r.status_code == 200:
            res = json.loads(r.text)

            if len(res) > 0:
                for i in res:
                    newlyUpdated.append(i)
        else:
            print(r)
            print("Failed to fetch recently updated data from Metabase.")
    except Exception as error:
        print('ERROR', error)
        print("Failed to fetch recently updated data from Metabase.")
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
            sleep(2)
            print(r.status_code)
        except Exception as error:
            print('ERROR', error)
    if category == Constants.CATEGORY_NEWPOST:
        print(currentDateTime() + " " + str(Pcount) + " Newly Published Dataset have been updated.")
    elif category == Constants.CATEGORY_UPDATEDPOST:
        print(currentDateTime() + " " + str(Ucount) + " Recently Updated Dataset have been updated.")


def main():
    print(currentDateTime() + " Executing...")
    # checkPostsDate(Constants.API_WP_GETPOSTS_PUBLISH)
    # checkPostsDate(Constants.API_WP_GETPOSTS_UPDATE)
    fetchDatasets()
    print(currentDateTime() + " There are " + str(len(newlyPublished)) + " Newly Published Dataset.")
    print(currentDateTime() + " There are " + str(len(newlyUpdated)) + " Newly Updated Dataset.")
    if len(newlyPublished) > 0:
        print(currentDateTime() + " Ada WP Bot is uploading the Newly Published Dataset.")
        createWPposts(newlyPublished, Constants.CATEGORY_NEWPOST)
    if len(newlyUpdated) > 0:
        print(currentDateTime() + " Ada WP Bot is uploading Recently Updated Dataset.")
        createWPposts(newlyUpdated, Constants.CATEGORY_UPDATEDPOST)
    checkPostsStatus(Constants.API_WP_GETPOSTS_PUBLISH)
    checkPostsStatus(Constants.API_WP_GETPOSTS_UPDATE)


if __name__ == "__main__":
    main()




