import requests
import json

def test_produce_sentences():
    # API URL
    url = "http://127.0.0.1:5001/produce_sentences"

    # Test input
    input_data = {
        "fulltext": (
            "This is the first sentence. This is the second sentence. "
            "Here comes the third one. Finally, this is the last sentence."
        )
    }

    # Send POST request
    response = requests.post(url, json=input_data)

    # Validate response
    if response.status_code == 200:
        print("Test Passed!")
        print("Response JSON:")
        print(json.dumps(response.json(), indent=4))
    else:
        print("Test Failed!")
        print(f"Status Code: {response.status_code}")
        print(f"Error: {response.text}")

# Run the test
if __name__ == "__main__":
    test_produce_sentences()
