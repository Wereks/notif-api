def test_create_message(client):
    response = client.post('/messages/',
                    json={'text': "First message in examples"})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_create_message_too_short(client):
    response = client.post('/messages/', json={'text': ""})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_create_message_too_long(client):
    response = client.post('/messages/', json={'text': "0123456789"*16+'0'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_delete_message(client):
    response = client.delete('/messages/1')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_delete_message_nonexisting(client):
    response = client.delete('/messages/10')
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_modify_message(client):
    response = client.delete('/messages/1', json={'text': "First message in examples"})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_modify_message_nonexisting(client):
    response = client.delete('/messages/10', json={'text': "First message in examples"})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_modify_message_too_short(client):
    response = client.delete('/messages/1', json={'text': ""})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}

def test_modify_message_too_long(client):
    response = client.delete('/messages/1', json={'text': "0123456789"*16+'0'})
    assert response.status_code == 401
    assert response.json() == {'detail': 'Not authenticated'}


def test_bad_username_password(client):
    response = client.post('/token', data = {
        'username': 'mod',
        'password': 'mod',
    })

    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}

def test_bad_password(client):
    response = client.post('/token', data = {
        'username': 'mod',
        'password': 'admin',
    })

    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}

def test_bad_username(client):
    response = client.post('/token', data = {
        'username': 'admin',
        'password': 'mod',
    })

    assert response.status_code == 401
    assert response.json() == {'detail': 'Incorrect username or password'}

