from fastapi.testclient import TestClient
from modelo_app_html import app
import requests

client = TestClient(app)

# Test para la ruta raíz
def test_get_index():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

# Test para agregar teorema exitoso
def test_add_theorem_success():
    payload = {"teorema": "Teorema de Pitágoras"}
    response = client.post("/add_theorem", json=payload)
    assert response.status_code == 200
    json_response = response.json()
    assert "teorema" in json_response
    assert json_response["teorema"] == "Teorema de Pitágoras"
    assert "explicacion" in json_response
    assert "conocimientos_previos" in json_response
    assert "ejemplo" in json_response

# Test para agregar teorema sin datos
def test_add_theorem_no_data():
    response = client.post("/add_theorem", json={})
    assert response.status_code == 422

# Test para agregar teorema con datos incorrectos
def test_add_theorem_invalid_data():
    payload = {"wrong_key": "Teorema de Pitágoras"}
    response = client.post("/add_theorem", json=payload)
    assert response.status_code == 422

# Test para agregar teorema con URL
def test_add_theorem():
    # Define the URL for the add_theorem endpoint
    url = "http://localhost:8000/add_theorem"

    # Create a sample payload (theorem)
    data = {
        "teorema": "El teorema de Pitágoras"
    }
    # Send a POST request to the FastAPI server
    response = requests.post(url, json=data)

    # Assertions to validate the test
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
