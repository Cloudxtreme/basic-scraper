import requests
from bs4 import BeautifulSoup
import sys
import json


def get_search_results(
        query=None, minAsk=None, maxAsk=None, bedrooms=None, use_file=None):
    # print locals().items()
    search_params = {
        key: val for key, val in locals().items() if val is not None
        }
    if not search_params:
        raise ValueError("No valid keywords")
    if use_file:
        with open('craigslist_response.html', 'r') as infile:
            resp = infile.read()
        resp.encode('utf-8')
        return resp, 'utf-8'
        base = 'http://seattle.craigslist.org/search/apa'
        resp = requests.get(base, params=search_params, timeout=3)
        resp.raise_for_status()  # <- no-op if status==200
        return resp.content, resp.encoding


def get_file_search_results(
        query=None, minAsk=None, maxAsk=None, bedrooms=None):
    """
    DEPRECATED.  USE get_search_results instead and pass it a file
    name ifi you want it to search a file.
    """

    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")
    with open('craigslist_response.html', 'r') as infile:
        resp = infile.read()
    resp.encode('utf-8')
    return resp, 'utf-8'


def get_json_search_results(
        query=None, minAsk=None, maxAsk=None, bedrooms=None, use_file=None):
    # print locals().items()
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")
    if use_file:
        with open(use_file, 'r') as infile:
            resp = infile.read()
            return resp
    else:
        base = 'http://seattle.craigslist.org/jsonsearch/apa'
        resp = requests.get(base, params=search_params, timeout=3)
        resp.raise_for_status()  # <- no-op if status==200
        return resp.json()


def parse_source(str):
    return json.loads(str)


def extract_json_listings(parsed):
    all_listings = parsed[0]
    print len(all_listings)

#    return listings


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        html, encoding = get_json_search_results(
            minAsk=500, maxAsk=1000, bedrooms=2, use_file='apa.json'
        )
    else:
        html, encoding = get_json_search_results(
            minAsk=500, maxAsk=1000, bedrooms=2
        )
    doc = parse_source(html, encoding)
    print doc.prettify(encoding=encoding)
