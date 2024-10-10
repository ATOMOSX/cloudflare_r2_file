import requests

url = 'http://127.0.0.1:5000/upload'

file_path = 'Laboratorio Sabado Inf. Computacional .pdf'

with open(file_path, 'rb') as file:
    files = {'file': file}

    response = requests.post(url, files=files)

    print(f"Status Code: {response.status_code}")

    try:
        response_json = response.json()
        print(f"Response JSON: {response_json}")
    except ValueError:
        print("Response content is not in JSON format.")
        print(response.text)
