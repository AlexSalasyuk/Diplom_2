import requests
from urls import REGISTER_USER_URL, LOGIN_USER_URL, USER_URL, ORDER_URL

def register_user(user_data):
    return requests.post(REGISTER_USER_URL, json=user_data)

def login_user(credentials):
    return requests.post(LOGIN_USER_URL, json=credentials)

def delete_user(token):
    return requests.delete(USER_URL, headers={'Authorization': token})

def update_user(token, data):
    return requests.patch(USER_URL, json=data, headers={'Authorization': token})

def create_order(token, ingredients):
    headers = {'Authorization': token} if token else {}
    return requests.post(ORDER_URL, json={'ingredients': ingredients}, headers=headers)

def get_user_orders(token):
    headers = {'Authorization': token} if token else {}
    return requests.get(ORDER_URL, headers=headers)
