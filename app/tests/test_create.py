def norm(msg):
    return (msg['text'], msg['views'])

def test_create_message(client, token):
    text = "First message in examples"
    response = client.post('/messages/',
                    json={'text': text},
                    headers=token)

    assert response.status_code == 200

    json = response.json()
    assert { 'id': json['id'], 'text': text, 'views': 0, } == json


def test_create_message2(client, token):
    text = "Second example"
    response = client.post('/messages/',
                    json={'text': text},
                    headers=token)
    assert response.status_code == 200

    json = response.json()
    assert  json == {   'id': json['id'],
                        'text': text,
                        'views': 0, 
                    }

    assert [{   'id': json['id'],
                'text': text,
                'views': 0, }] == client.get('/messages/').json()


def test_create_message3(client, token):
    texts = ['Message1', 'Message2', 'Message3']

    responses = [client.post('/messages/',
                    json={'text': text},
                    headers=token) for text in texts]

    assert all((response.status_code == 200 for response in responses))
    assert len(responses) == 3

    responses_json = [norm(response.json()) for response in responses]
    assert set(responses_json) == set((text, 0) for text in texts)

def test_create_message_too_short(client, token):
    response = client.post('/messages/', 
                            json={'text': ""},
                            headers=token)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "ensure this value has at least 1 characters"

def test_create_message_too_long(client, token):
    response = client.post('/messages/', 
                        json={'text': "0123456789"*16+'0'},
                        headers=token)
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "ensure this value has at most 160 characters"