import argparse
import json
import requests


def get_arguments():
    """get the arguments from the console

    Returns:
        [string]: [search query],
        [string]: [type of search],
        [int]: [number of items]

    """
    parser = argparse.ArgumentParser(description='Youtube Search')
    parser.add_argument('query', help='Search Query', type=str)
    parser.add_argument('--type', help="Search type: video/channel", type=str)
    parser.add_argument('--mr', help="Max Results (number of item)", type=int)
    args = parser.parse_args()
    query = args.query
    search_type = args.type
    max_result = args.mr
    return query, search_type, max_result


def get_api_key(file_name):
    """ Extract configrations from the config file

    Args:
        file_name ([string]): [configration file name]

    Returns:
        [string]: [api key]
    """
    file = open(file_name)
    config = json.load(file)
    return config.get('apiKey')


def get_search_results(api_key, search_query, search_type, max_results):
    """get the search results

    Args:
        api_key ([string]): [the api key]
        search_query ([string]): [search query]
        search_type ([string]): [type of the search results]
        max_results ([int]): [number of items]

    Returns:
        [list]: [search results]
    """
    # if the user dosen't enter the search_type or max_result leave them with default values
    if search_type is None:
        search_type = 'video'
    if max_results is None:
        max_results = 20

    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults={max_results}&q={search_query}&type={search_type}&key={api_key}"
    response = requests.get(url).json()
    search_results = response.get('items')
    return search_results


def write_to_file(file_name, search_results):
    """write to file

    Args:
        file_name ([string]): [name of the file that we want to write on it]
        search_results ([list]): [results of the search operation]
    """
    with open(file_name, 'w') as file:
        json.dump(search_results, file)


def main():

    # get the args from the console
    query, search_type, max_results = get_arguments()
    # get the apiKey from the configuration file
    api_key = get_api_key('config.json')
    # get the search results as a list
    search_results = get_search_results(
        api_key, query, search_type, max_results)
    # write the results to a file
    write_to_file('results.json', search_results)


if __name__ == '__main__':

    main()
