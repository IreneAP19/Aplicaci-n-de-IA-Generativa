
import requests


def test_add_theorem():
    # Define the URL for the add_theorem endpoint
    url = "http://localhost:8000/add_theorem"

    # Create a sample payload (theorem)
    data = {
        "teorema": "El teorema de Pitagoras"
    }
    # Send a POST request to the FastAPI server
    response = requests.post(url, json=data)

    # Assertions to validate the test
    assert response.status_code == 200
    assert isinstance(response.json(),str)
