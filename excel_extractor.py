import pandas as pd
import collections
import requests
import json
import os

BASE_URL = 'https://webapp-backend-dev.herokuapp.com'
# BASE_URL = 'http://webapp/api'
BASE_URL = os.environ.get('BASE_URL', BASE_URL)


def get_access_token():
    # authenticate url
    url = BASE_URL + '/auth/local'

    # authenticate headers
    headers = {
        'Authorization': f'Basic {os.environ.get("AUTHORIZATION")}',
        'Origin': 'https://webapp.orangedigitalcloud.com',
        'Referer': 'https://webapp.orangedigitalcloud.com/'
    }

    # authenticate data
    data = {
        'grant_type': 'password',
        'username': os.environ.get('USERNAME'),
        'password': os.environ.get('PASSWORD'),
        'auth': 'basic'
    }

    response = requests.post(url, headers=headers, json=data)

    # extract access token
    access_token = response.json()["access_token"]

    return access_token


def read_enums_in_server():
    # Define the GraphQL endpoint
    url = BASE_URL + "/graphql"
    headers = {"Authorization": "Bearer " + get_access_token()}

    # Define the introspection query
    query = """
    query IntrospectionQuery {
        __schema {
        types {
            kind
            name
            enumValues {
            name
            }
        }
        }
    }
    """

    # Send the introspection query to the GraphQL server
    response = requests.post(url, json={'query': query}, headers=headers)

    # Extract the enums from the introspection query response
    enums = dict()
    for t in json.loads(response.text)["data"]["__schema"]["types"]:
        if t["kind"] == "ENUM":
            enumValues = t["enumValues"][0]
            enums[t["name"]] = list()
            for enumValue in t["enumValues"]:
                enums[t["name"]].append(enumValue["name"])

    # Now we have list of all the enums in the system in a dictionary with this structure:
    """
    {
        'EnumName': ['EnumValue1', 'EnumValue2', ...],
        ...
    }
    """

    values = [val for sublist in enums.values() for val in sublist]

    return {
        'flat_values': values,
        'enums': enums
    }


def get_enums_flat_list():
    values = read_enums_in_server()['flat_values']
    return values


if __name__ == "__main__":

    enums = read_enums_in_server()['enums']
    values = read_enums_in_server()['flat_values']

    duplicates = [item for item, count in collections.Counter(
        values).items() if count > 1]

    duplicates_usages = dict()

    with open('dist/enums/en-us.json') as f:
        translations = json.load(f)

    for duplicate in duplicates:
        duplicates_usages[duplicate] = {
            "usages": [], "translated_value": translations.get(duplicate)}
        for enum_name, enum_values in enums.items():
            if duplicate in enum_values:
                duplicates_usages[duplicate]["usages"].append(enum_name)

    # Convert the dictionary to a DataFrame
    df = pd.DataFrame.from_dict(duplicates_usages, orient='index')

    # Write the DataFrame to an Excel file
    df.to_excel('my_dict.xlsx')
