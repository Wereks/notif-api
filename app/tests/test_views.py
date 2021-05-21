def test_views_read(client, token):
    text = "Message to be viewed"
    response_create = client.post('/messages/',
                    json={'text': text},
                    headers=token)

    id_ = response_create.json()['id']

    for i in range(10):
        assert client.get(f'/messages/{id_}').json()['views'] == i


def test_views_reads(client, token):
    texts = ["Message to be viewed " + str(i) for i in range(3)]
    for text in texts:
        client.post('/messages/',
                    json={'text': text},
                    headers=token)
    
    for i in range(10):
        res = client.get('/messages/')
        assert all(msg['views'] == i for msg in res.json())