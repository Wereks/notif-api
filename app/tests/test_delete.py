import pytest

def test_delete(client, token):
    text = "Message to be deleted"
    response_create = client.post('/messages/',
                    json={'text': text},
                    headers=token)
    id_create = response_create.json()['id']

    response_del = client.delete(f'/messages/{id_create}', headers=token)

    assert response_create.json() == response_del.json()
                
    response = client.get(f'/messages/{id_create}')
    
    assert response.status_code == 404
    
def test_delete_nonexisting(client, token):
    response = client.delete('/messages/1', headers=token)    

    assert response.status_code == 404


    