import re
from functools import reduce
from ipaddress import ip_network as parse_addr

from flask import Flask
from flask import abort
from flask import request

from alertserver.config import Bitbucket as config_bitbucket

app = Flask(__name__)

trusted_remote_addrs = list(reduce(
    lambda l1, l2: l1 + l2,
    map(
        lambda addr_str: [str(network) for network in parse_addr(addr_str)],
        re.sub(r'\s', '', config_bitbucket.trusted_remote_addrs).split(',')
    )
))


def is_trusted_remote_addrs(addr):
    return addr in trusted_remote_addrs


def webhook_routine():
    if not is_trusted_remote_addrs(request.remote_addr):
        abort(403)

    data = request.get_json()

    commit_author = data['actor']['username']

    is_branch_created = data['push']['changes'][0]['created']
    is_branch_closed = data['push']['changes'][0]['closed']
    if is_branch_created:
        # TODO: Alert branch created.
        print('Webhook received! %s created branch' % commit_author)
        pass
    elif is_branch_closed:
        # TODO: Alert branch closed.
        print('Webhook received! %s deleted branch' % commit_author)
    else:
        # TODO: Alert commits.
        commit_hash = data['push']['changes'][0]['new']['target']['hash'][:7]
        commit_url = data['push']['changes'][0]['new']['target']['links']['html']['href']
        print('Webhook received! %s committed %s' % (commit_author, commit_hash))
    return 'OK'


webhook_paths = re.sub(r'\s', '', config_bitbucket.webhook_paths).split(',')

for webhook_path in webhook_paths:
    app.route(webhook_path, methods=['POST'])(webhook_routine)

if __name__ == '__main__':
    app.run(host=config_bitbucket.webhook_host, port=int(config_bitbucket.webhook_port), debug=True)
