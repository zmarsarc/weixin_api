import requests
import json
from ConfigParser import ConfigParser

configer = ConfigParser()
configer.read('config.cfg')
api_url = configer.get('Server_info', 'api_base_url')

def get_access_token(appid, secret):
    params = {'grant_type': 'client_credential',
              'appid': appid,
              'secret': secret}
    response = requests.get(api_url + 'token', params=params)
    formated_response = json.loads(response.content)
    token = {'token': formated_response['access_token'],
             'expires_in': formated_response['expires_in'],
             'update_time': time.time()}
    return token

def get_server_ip(token):
    params = {'access_token': token}
    response = requests.get(api_url + 'getcallbackip', params=params)
    return json.loads(response.content)['ip_list']

