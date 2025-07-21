# def test_index():
#     assert not False

def test_index_ok(client):
    response = client.get('/')
    assert response.status_code == 200