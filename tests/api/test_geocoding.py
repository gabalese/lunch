import location.find


def test_geocoding_works():
    point = location.find.search('Viale Tito Labieno Roma')
    assert point
    assert point.lon == 12.567068
    assert point.lat == 41.8532771
