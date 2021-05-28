import requests
from django.conf import settings
import json


def register(api_key, secret_key, **kwargs):
    endpoint = f'{settings.API_HOST}register/'
    first_name = kwargs.get('first_name')
    email = kwargs.get('email')
    last_name = kwargs.get('last_name')
    password = kwargs.get('password')
    payload = {
        "api_key": api_key,
        "secret_key": secret_key,
        "user": {
            "password": password,
            "email": email,
            "first_name": first_name,
            "last_name": last_name
        }

    }
    headers = {
        'Content-Type': 'application/json',

    }
    response = requests.request("POST", endpoint, headers=headers, data=json.dumps(payload))
    if response.status_code == 201:
        return "User Registered", True
    return json.loads(response.text)['error'], False


def login(username, password):
    endpoint = f'{settings.API_HOST}login/'

    payload = {

        "password": password,
        "username": username,

    }
    headers = {
        'Content-Type': 'application/json',

    }
    response = requests.request("POST", endpoint, headers=headers, data=json.dumps(payload))

    if response.status_code == 200:
        return json.loads(response.text), True
    return "invalid credentials", False


def get_currency(token):
    endpoint = f'{settings.API_HOST}currency/'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'

    }
    response = requests.request("GET", endpoint, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text), True
    return "Error occured on server side", False


def insert_input(account, token, start_date, **kwargs):
    currency = kwargs.get("currency")
    end_date = kwargs.get("end_date")
    category = kwargs.get("category")
    exchange = kwargs.get("exchange")

    endpoint = f'{settings.API_HOST}input/'

    payload = {

        "account": int(account),
        "start_date": start_date,
        "currency": int(currency),
        "end_date": end_date,
        "category": category,
        "exchange": exchange

    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'

    }
    response = requests.request("POST", endpoint, headers=headers, data=json.dumps(payload))
    print("this is the response", response)
    if response.status_code == 201:
        return json.loads(response.text), True
    return "Error occured on server side", False


def update_input(account, token, start_date, input_id, **kwargs):
    currency = kwargs.get("currency")
    end_date = kwargs.get("end_date")
    category = kwargs.get("category")
    exchange = kwargs.get("exchange")

    endpoint = f'{settings.API_HOST}input/update/{input_id}'

    payload = {

        "account": int(account),
        "start_date": start_date,
        "currency": int(currency),
        "end_date": end_date,
        "category": category,
        "exchange": exchange

    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'

    }
    response = requests.request("PUT", endpoint, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return json.loads(response.text), True
    return "Error occured on server side", False


def get_input_data(token, input_id):
    endpoint = f'{settings.API_HOST}retrieve/input/{input_id}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'

    }
    response = requests.request("GET", endpoint, headers=headers)
    if response.status_code == 200:
        return json.loads(response.text), True
    return "Error occured on server side", False


def get_account_detail(token, account_id):
    endpoint = f'{settings.API_HOST}account/{account_id}'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'

    }
    response = requests.request("GET", endpoint, headers=headers)
    print("this is the update_input response", response)
    if response.status_code == 200:
        return json.loads(response.text), True
    return "Error occured on server side", False


def update_account_detail(account_id, token, **kwargs):
    secret_key = kwargs.get("secret_key")
    api_key = kwargs.get("api_key")

    endpoint = f'{settings.API_HOST}account/{account_id}'

    payload = {

        "api_key": api_key,
        "secret_key": secret_key

    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'

    }
    response = requests.request("PUT", endpoint, headers=headers, data=json.dumps(payload))
    if response.status_code == 200:
        return json.loads(response.text), True
    return "Error occured on server side", False


def get_exchange(token):
    endpoint = f'{settings.API_HOST}exchange/'

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Token {token}'

    }
    response = requests.request("GET", endpoint, headers=headers)

    if response.status_code == 200:
        return json.loads(response.text), True
    return "Error occured on server side", False
