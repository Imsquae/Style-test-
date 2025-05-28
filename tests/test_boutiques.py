def test_user_boutiques(client, auth, app):
    auth.login()
    # Avant refactor: assert len(current_user.boutiques.all()) == 0
    assert len(current_user.owned_boutiques.all()) == 0
    
    # Créer une boutique
    response = client.post('/boutiques/new', data={
        'name': 'Test Boutique',
        'description': 'Test Description',
        'address': 'Test Address',
        'category_id': 1
    })
    assert response.status_code == 302
    
    # Vérification de création boutique
    # Avant refactor: assert len(current_user.boutiques.all()) == 1
    assert len(current_user.owned_boutiques.all()) == 1 