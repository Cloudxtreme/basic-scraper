import pytest
slow = pytest.mark.slow


def test_json_search_results_file():
    import basic_scraper as bs
    list_title = '3 Bedroom Across from Food Forest'
    results = bs.get_json_search_results(use_file="apa.json")
    assert results[0][1]['PostingTitle'] == list_title


def test_extract_json_listings():
    import basic_scraper as bs
    results = bs.get_json_search_results(use_file='apa.json')
    listings = bs.extract_json_listings(results, no_geoclusters=True)
    assert listings[0]['description'] == '3 Bedroom Across from Food Forest'
    assert listings[0]['link'] == '/see/apa/4525143645.html'
    assert listings[0]['location']['data-latitude'] == 47.569878
    assert listings[0]['location']['data-longitude'] == -122.313483
    assert listings[0]['price'] == '1300'
    assert listings[0]['size'] == '3'


def test_add_address():
    import basic_scraper as bs
    results = bs.get_json_search_results(use_file='apa.json')
    listings = bs.extract_json_listings(results, no_geoclusters=True)
    listing = bs.add_address(listings[0])
    assert 'address' in listing
    assert listing['address'] != 'unavailable'


@slow
def test_json_search_results_live_still_have_format():
    print "in live test"
    import basic_scraper as bs
    result = bs.get_json_search_results(
        minAsk=500,
        maxAsk=1000, bedrooms=2)
    listings = bs.extract_json_listings(result)
    print listings
    assert ('Ask' in result[0][2]) or ('GeoCluster' in result[0][2])
    assert ('Bedrooms' in result[0][2]) or ('GeoCluster' in result[0][2])
    assert ('PostingTitle' in result[0][2]) or ('GeoCluster' in result[0][2])
    assert ('Longitude' in result[0][2]) or ('GeoCluster' in result[0][2])
    assert ('Latitude' in result[0][2]) or ('GeoCluster' in result[0][2])
    assert ('PostingURL' in result[0][2]) or ('GeoCluster' in result[0][2])
    assert ('PostingTitle' in result[0][2]) or ('GeoCluster' in result[0][2])
