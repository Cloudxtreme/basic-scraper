import requests
from bs4 import BeautifulSoup


def get_search_results(query=None, minAsk=None, maxAsk=None, bedrooms=None):
    print locals().items()
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")

    base = 'http://seattle.craigslist.org/search/apa'
    resp = requests.get(base, params=search_params, timeout=3)
    resp.raise_for_status()  # <- no-op if status==200
    return resp.content, resp.encoding


def get_file_search_results(
        query=None, minAsk=None, maxAsk=None, bedrooms=None):
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")
    with open('craigslist_response.html', 'r') as infile:
        resp = infile.read()
    resp.encode('utf-8')
    return resp, 'utf-8'


def parse_source(body, encoding='utf-8'):
    parsed = BeautifulSoup(body, encoding)
    print "parsed len is: {}".format(len(parsed))
