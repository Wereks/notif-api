def test_read(client, token):
    text = "Message to be read"
    response_create = client.post('/messages/',json={'text': text}, headers=token)
    id_create = response_create.json()['id']        
    response = client.get(f'/messages/{id_create}')
    
    assert response.status_code == 200
    assert response.json()['text'] == text

def test_read_nonexist(client):
    response = client.get(f'/messages/{5}')
    
    assert response.status_code == 404

def test_reads(client, token):
    text = "Message to be reads"
    client.post('/messages/', json={'text': text}, headers=token)      
    response = client.get('/messages')
    
    json = response.json()
    assert response.status_code == 200
    assert len(json) == 1
    assert json == [{'id': json[0]['id'], 'text':text, 'views':0}]

def test_reads_nonexist(client):
    response = client.get(f'/messages')
    
    assert response.status_code == 200
    assert response.json() == []
    