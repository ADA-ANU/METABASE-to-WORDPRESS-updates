from datetime import datetime
import json
import requests  # http://docs.python-requests.org/en/master/

# --------------------------------------------------
# Update the 4 params below to run this code
# --------------------------------------------------


def test():
    dataverse_server = 'https://dataverse-dev.ada.edu.au' # no trailing slash
    api_key = 'fdd7826a-1d20-4067-8d16-ce9c321b5761'
    dataset_id = 2115  # database id of the dataset
    persistentId = 'doi:10.5072/FK2/6XACVA' # doi or hdl of the dataset

    # --------------------------------------------------
    # Prepare "file"
    # --------------------------------------------------
    file_content = 'content: %s' % datetime.now()
    files = {'file': ('sample_file.txt', file_content)}

    # --------------------------------------------------
    # Using a "jsonData" parameter, add optional description + file tags
    # --------------------------------------------------
    params = dict(description='Blue skies!',
                categories=['Lily', 'Rosemary', 'Jack of Hearts'])

    params_as_json_string = json.dumps(params)

    payload = dict(jsonData=params_as_json_string)

    # --------------------------------------------------
    # Add file using the Dataset's id
    # --------------------------------------------------
    url_dataset_id = '%s/api/datasets/%s/add?key=%s' % (dataverse_server, dataset_id, api_key)

    # -------------------
    # Make the request
    # -------------------
    print('-' * 40)
    print('making request: %s' % url_dataset_id)
    r = requests.post(url_dataset_id, data=payload, files=files)

    # -------------------
    # Print the response
    # -------------------
    print('-' * 40)
    print(r.json())
    print(r.status_code)


if __name__ == "__main__":
    test()


