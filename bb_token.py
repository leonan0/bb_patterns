import configparser
import json
import requests

def set_auth_token():
    # CREATE OBJECT
    config_file = configparser.ConfigParser()

    # READ CONFIG FILE
    config_file.read("./config.ini")

    bbtips = config_file['bbtips']

    url = bbtips['login_url']

    payload = json.dumps({
        "username": bbtips['username'],
        "password": bbtips['password']
    })

    headers = {
        'authority': 'api.bbtips.com.br',
        'content-type': 'application/json',
    }

    response = requests.post(url, headers=headers, data=payload)

    config_file['bbtips']['auth_token'] = f"Bearer {response.json()['Payload']['accessToken']}"

    with open("config.ini","w") as file_object:
        config_file.write(file_object)
        
    print('Token atualizado')

if __name__ == '__main__':
    set_auth_token()