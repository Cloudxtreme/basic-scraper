import requests
import sys
import json
import pprint


def get_json_search_results(
        query=None, minAsk=None, maxAsk=None, bedrooms=None, use_file=None):
    # print "in get_json_search_results"
    search_params = {
        key: val for key, val in locals().items() if val is not None
    }
    if not search_params:
        raise ValueError("No valid keywords")
    if use_file is not None:
        with open(use_file, 'r') as infile:
            resp = json.load(infile)
        return resp
    else:
        base = 'http://seattle.craigslist.org/jsonsearch/apa'
        resp = requests.get(base, params=search_params, timeout=3)
        resp.raise_for_status()  # <- no-op if status==200
        return resp.json()


def extract_json_geocluster_listings(geocluster):
    # print "in geocluster listings"
    base = 'http://seattle.craigslist.org'
    resp = requests.get(base + geocluster['url'], timeout=3)
    resp.raise_for_status()
    results = resp.json()
    listings = [{
                'description': item['PostingTitle'],
                'link': item['PostingURL'],
                'location': {
                    'data-latitude': item['Latitude'],
                    'data-longitude': item['Longitude']
                    },
                'price': item['Ask'],
                'size': item['Bedrooms']
                } for item in results if 'PostingTitle' in item]
    return listings


def extract_json_listings(parsed, no_geoclusters=False):
    all_listings = parsed[0]
    listings = []
    for item in all_listings:
        if 'PostingTitle' in item:
            listings.append({
                            'description': item['PostingTitle'],
                            'link': item['PostingURL'],
                            'location': {
                                'data-latitude': item['Latitude'],
                                'data-longitude': item['Longitude']
                                },
                            'price': item['Ask'],
                            'size': item['Bedrooms']
                            })
        # look for GeoClusters to extract (won't run if in test mode)
        #    print "test mode is: {}".format(test_mode)
        elif 'GeoCluster' in item and not no_geoclusters:
            listings = listings + extract_json_geocluster_listings(item)
        """
        else:
            print "This item was not extracted (this may be because you are" \
                "running test mode):"
            pprint.pprint(item)
            print '\n'
        """
    return listings


def add_address(entry):
    """
    format the location data provided in that listing properly.
    make a reverse geocoding lookup using the google api above.
    add the best available address to the listing.
    return the updated listing.
    """
    url = "http://maps.googleapis.com/maps/api/geocode/json"
    location = entry['location']
    latlng = "{0},{1}".format(
        location['data-latitude'], location['data-longitude'])
    parameters = {'latlng': latlng, 'sensor': 'false'}
    resp = requests.get(url, params=parameters)
    # below is a no-op if all is well
    resp.raise_for_status()
    data = json.loads(resp.text)
    if data['status'] == 'OK':
        entry['address'] = data['results'][0]['formatted_address']
        # print entry
    else:
        entry['address'] = 'unavailable'
    return entry


if __name__ == '__main__':

    params = {'minAsk': 500, 'maxAsk': 1000, 'bedrooms': 2}
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        params['use_file'] = 'apa.json'
    json_data = get_json_search_results(**params)
    # print "json_data[0][1] is: {}".format(json_data[0][1]['PostingTitle'])
    listings = extract_json_listings(json_data, no_geoclusters=True)
#    print len(listings)
    add_address(listings[0])
    pprint.pprint(listings[0])
