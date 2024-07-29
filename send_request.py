import os
import json
import requests

def send_request():
    # Load the payload from the environment variable
    requests_json = os.getenv('REQUESTS_JSON')
    payload = json.loads(requests_json)

    # Ensure the payload is in the correct format
    if not isinstance(payload, dict) or 'requests' not in payload:
        payload = {'requests': [payload]}

    url = "https://datasetparser.onrender.com/parse/"
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        # The response is already a JSON string, so we can write it directly
        with open('response.json', 'w') as f:
            f.write(response.text)
        print("API request successful. Response saved to response.json")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)

if __name__ == "__main__":
    send_request()
