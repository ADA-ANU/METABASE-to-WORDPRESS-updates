import dotenv
import os
dotenv.load_dotenv()

CATEGORY_NEWPOST = "24"

CATEGORY_UPDATEDPOST = "25"

API_METABASE_AUTHENTICATION_ENDPOINT = "https://dataverse-dev.ada.edu.au/metabase/api/session"
#"http://sw-dev.ada.edu.au:8085/wp-json/aam/v2/authenticate"
API_WP_AUTHENTICATION_ENDPOINT = "https://ada.edu.au/wp-json/aam/v2/authenticate"
#"http://sw-dev.ada.edu.au:8085/wp-json/wp/v2/posts?categories=26"
API_WP_GETPOSTS_PUBLISH = "https://ada.edu.au/wp-json/wp/v2/posts?categories=24&per_page=20"
#"http://sw-dev.ada.edu.au:8085/wp-json/wp/v2/posts?categories=27"
API_WP_GETPOSTS_UPDATE = "https://ada.edu.au/wp-json/wp/v2/posts?categories=25&per_page=20"
#"http://sw-dev.ada.edu.au:8085/wp-json/wp/v2/posts/"
API_WP_UPDATEPOSTS = "https://ada.edu.au/wp-json/wp/v2/posts/"
#"http://sw-dev.ada.edu.au:8085/wp-json/aam/v1/validate-jwt"
API_WP_VALIDATE = "https://ada.edu.au/wp-json/aam/v1/validate-jwt"
#328
API_DATASETS_QUERY_NEWPUBLICATION = "https://dataverse-dev.ada.edu.au/metabase/api/card/396/query/json"

API_DATASETS_QUERY_NEWPUPDATE = "https://dataverse-dev.ada.edu.au/metabase/api/card/397/query/json"
#"http://sw-dev.ada.edu.au:8085/wp-json/wp/v2/posts"
API_WP_CREATEPOSTS = "https://ada.edu.au/wp-json/wp/v2/posts"

API_DV_DATASETINFO = "https://dataverse.ada.edu.au/api/datasets/:persistentId/?persistentId=doi:"

API_DATAVERSES_PUBLISHDATASET = "https://dataverse-dev.ada.edu.au/api/datasets/"

API_DATAVERSES_CREATEDATASET = "https://dataverse-dev.ada.edu.au/api/dataverses/DEV-ADA/datasets/"


API_METABASE_AUTHENTICATION_HEADER = {
    'Content-Type': 'application/json'
}

API_METABASE_AUTHENTICATION_BODY = {
    "username": os.getenv("METABASE_USERNAME"),
    "password": os.getenv("METABASE_PASSWORD")
}

API_WP_AUTHENTICATION_HEADER = {
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

API_WP_POSTS_HEADER = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    "Cache-Control": "no-cache"
}

API_FETCH_HEADER = {
    # "Cache-Control": "max-age=0",
    # "Upgrade-Insecure-Requests": "1",
    # "Connection": "keep-alive",
    # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36",
    # "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    # "Sec-Fetch-Site": "none",
    # "Sec-Fetch-Mode": "navigate",
    # "Sec-Fetch-User": "?1",
    # "Sec-Fetch-Dest": "document",
    # "Accept-Encoding": "gzip, deflate, br",
    # "Accept-Language": "en,zh-CN;q=0.9,zh;q=0.8,en-US;q=0.7",
    "Cookie": "et-pb-recent-items-font_family=Montserrat; "

}

API_WP_AUTHENTICATION_BODY = {
    "username": os.getenv("WP_USERNAME"),
    "password": os.getenv("WP_PASSWORD"),
    "issueJWT": "true"
}

API_WP_VALIDATE_HEADER = {
    'Content-Type': 'application/json'
}

API_WP_CREATEPOTS_HEADER = {
    'Content-Type': 'application/x-www-form-urlencoded'
}

API_DATAVERSES_PUBLISHDATASET_HEADER = {
    "X-Dataverse-key": os.getenv("DATAVERSE_TOKEN")
}

dateDiff = 14

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")
access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")
admin1 = os.getenv("ADMIN1")
admin2 = os.getenv("ADMIN2")
pwAdmin1 = os.getenv("PWADMIN1")

