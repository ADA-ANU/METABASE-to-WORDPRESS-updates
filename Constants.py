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