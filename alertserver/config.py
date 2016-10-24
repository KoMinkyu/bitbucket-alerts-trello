import codecs
import configparser
from easydict import EasyDict

_config = configparser.ConfigParser()
# _config.read('config.sample.ini')
_config.read_file(codecs.open('config.sample.ini', 'r', 'utf8'))

Bitbucket = EasyDict(_config['Bitbucket'])
Trello = EasyDict(_config['Trello'])