from ConfigParser import ConfigParser
import requests
from bs4 import BeautifulSoup


configer = ConfigParser()
configer.read('config.cfg')
error_url = configer.get('Server_info', 'error_url')


def get_error_page(url=error_url):
    response = requests.get(url,)
    return response.text

def get_error_list(html):
    error_list = []
    
    soup = BeautifulSoup(html, 'html.parser')
    raw_list = soup.find('tbody').find_all('tr')
    
    for tr in raw_list:
        tds = tr.find_all('td')
        if tds:
            error_list.append((tds[0].string, tds[1].string))

    return tuple(error_list)


if __name__ == '__main__':

    errors = get_error_list(get_error_page())
    for error in errors:
        print(error[0], error[1])
