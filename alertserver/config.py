import configparser
from easydict import EasyDict

_config = configparser.ConfigParser()
_config.read('config.sample.ini')

Bitbucket = EasyDict(_config['Bitbucket'])
Trello = EasyDict(_config['Trello'])