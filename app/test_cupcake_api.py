import pytest
from app import app, db
from models import Cupcake

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///test_cupcakes_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_patch_cupcake(client):
    """Test updating a cupcake's information."""
    cupcake = Cupcake(flavor="Vanilla", size="Medium", rating=7.5, image="https://example.com/cupcake.jpg")
    db.session.add(cupcake)
    db.session.commit()

    data = {
        "flavor": "Chocolate",
        "size": "Large",
        "rating": 9.0,
        "image": "https://example.com/new-cupcake.jpg"
    }

    response = client.patch(f"/api/cupcakes/{cupcake.id}", json=data)
    json_response = response.get_json()

    assert response.status_code == 200
    assert json_response['cupcake']['flavor'] == "Chocolate"
    assert json_response['cupcake']['size'] == "Large"
    assert json_response['cupcake']['rating'] == 9.0
    assert json_response['cupcake']['image'] == "https://example.com/new-cupcake.jpg"

def test_delete_cupcake(client):
    """Test deleting a cupcake."""
    cupcake = Cupcake(flavor="Vanilla", size="Medium", rating=7.5, image="https://example.com/cupcake.jpg")
    db.session.add(cupcake)
    db.session.commit()

    response = client.delete(f"/api/cupcakes/{cupcake.id}")
    json_response = response.get_json()

    assert response.status_code == 200
    assert json_response['message'] == 'deleted cupcake'
    
    # Confirm the cupcake is deleted
    assert Cupcake.query.get(cupcake.id) is None
