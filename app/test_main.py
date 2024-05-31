from .main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_obter_produtos():
    response = client.get("/api/v1/produtos")
    assert response.status_code == 200
    assert response.json() is not None


def test_obter_produto_por_tipo():
    tipo = "Geociências"
    response = client.get(f"/api/v1/produtos/portipo/{tipo}")
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()[0]["tipo"] == tipo


def test_obter_produto_por_cat_id():
    cat_id = 2024
    response = client.get(f"/api/v1/produtos/porcatid/{cat_id}")
    assert response.status_code == 200
    assert response.json() is not None
    assert response.json()[0]["catId"] == cat_id


    