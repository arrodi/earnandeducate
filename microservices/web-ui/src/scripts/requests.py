import requests

def get(api_url, api_endpoint):
    
    response = requests.get(f'{api_url}/{api_endpoint}')

    return response.json()

def post(api_url, api_endpoint, json_data):

    response = requests.post(f'{api_url}/{api_endpoint}', json=json_data)

    return response.json()
