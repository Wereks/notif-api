def test_update(client, token):
    text = "Message to be updated"
    response_create = client.post('/messages/',
                                  json={'text': text},
                                  headers=token)
    id_create = response_create.json()['id']

    text_updated = "Message already updated"
    response_update = client.put(f'/messages/{id_create}',
                                 json={'text': text_updated},
                                 headers=token)

    assert response_update.status_code == 200

    response_read = client.get(f'/messages/{id_create}')
    assert response_read.status_code == 200

    json = response_read.json()
    json['views'] = json['views'] - 1
    assert json == response_update.json()


def test_update_nonexist(client, token):
    text = "test_update_nonexist"
    response = client.put('/messages/13',
                          json={'text': text},
                          headers=token)

    assert response.status_code == 404


def test_update_message_too_short(client, token):
    response = client.post('/messages/',
                           json={'text': "abc"},
                           headers=token)

    id_create = response.json()['id']
    response = client.put(f'/messages/{id_create}',
                          json={'text': ''},
                          headers=token)

    assert response.status_code == 422
    assert response.json()[
        'detail'][0]['msg'] == "ensure this value has at least 1 characters"


def test_update_message_too_long(client, token):
    response = client.post('/messages/',
                           json={'text': "abc"},
                           headers=token)

    id_create = response.json()['id']
    response = client.put(f'/messages/{id_create}',
                          json={'text': "0123456789"*16+'0'},
                          headers=token)

    assert response.status_code == 422
    assert response.json()[
        'detail'][0]['msg'] == "ensure this value has at most 160 characters"
