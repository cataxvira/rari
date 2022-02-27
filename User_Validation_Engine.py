import time

import pandas as pd
import requests
from openpyxl import load_workbook

bearer_token = "AAAAAAAAAAAAAAAAAAAAAJWCVgEAAAAA1PUhi%2BO0b2pAEJlEm0xOKh1SBdA%3Dl8KdFZKVXxJ389r3qHzxTCbAkd5p0EWA7t5djKSNqtBFPrV0Pz"


def create_url(user_names):
    user_names_str = ','.join([str(elem).strip('@') for elem in user_names])
    usernames = "usernames=" + user_names_str
    user_fields = "user.fields=description,created_at"

    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def connect_to_endpoint(url):
    response = requests.request("GET", url, auth=bearer_oauth)
    # check response.text for evaluation
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    else:
        print("response code -", response.status_code, '\n' "Success!!")
    return response.json()


def main(bat):
    url = create_url(bat)
    json_response = connect_to_endpoint(url)
    time.sleep(240)
    # print(json_response)

    data_df = pd.json_normalize(json_response['data'])
    error_df: pd.DataFrame()
    try:
        error_df = pd.json_normalize(json_response['errors'])
    except KeyError as error:
        print("no errors in current user names")
        error_df = pd.DataFrame(
            columns=['parameter', 'resource_id', 'value', 'detail', 'title', 'resource_type', 'type'])
    return data_df, error_df


if __name__ == "__main__":
    file_path = input("Please Enter File Path Here - ")
    df = pd.DataFrame(pd.read_excel(file_path, usecols="D"))
    user_list = list(df['handle'].tolist())
    batchSize = 100
    batches = len(user_list) / batchSize + 1
    start = 0
    end = batchSize - 1
    data_dfs = []
    main_errors_dfs = []

    for bat in range(0, int(batches)):
        batch = user_list[start: end]
        start = end
        end += batchSize - 1
        data, errors = main(batch)
        data_dfs.append(data)
        main_errors_dfs.append(errors)

    main_df = pd.concat(data_dfs, ignore_index=True)
    Main_error_df = pd.concat(main_errors_dfs, ignore_index=True)

    path = file_path

    book = load_workbook(path)
    writer = pd.ExcelWriter(path, engine='openpyxl')
    writer.book = book
    main_df.to_excel(writer, sheet_name='Valid_users')
    Main_error_df.to_excel(writer, sheet_name='Invalid_users')
    writer.save()
