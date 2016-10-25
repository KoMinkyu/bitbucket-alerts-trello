import re
from functools import reduce
from ipaddress import ip_network as parse_addr

from easydict import EasyDict
from flask import Flask
from flask import abort
from flask import request

from alertserver.config import Bitbucket as config_bitbucket
from alertserver.trello_client import post_branch_activity, post_commit_activity, post_merge_activity

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


def parse_commit_message(commit_message):
    return tuple(re.split(r'^#?([0-9]+)\s?', commit_message)[1:3])


def parse_branch_name(branch_name):
    splitted = re.split(r'^([0-9]+)(-?_?\s?)(.*)', branch_name)
    if len(splitted) < 2:
        return tuple([None, splitted[0]])
    return tuple([splitted[1], splitted[3]])


def webhook_routine():
    if not is_trusted_remote_addrs(request.remote_addr):
        abort(403)

    data = EasyDict(request.get_json())

    commit_author = data.actor.username

    for change in data.push.changes:
        commit = change.commits[0]
        commit_message = commit.message
        commit_hash = commit.hash[:7]
        commit_url = change.links.html.href

        card_id1, commit_message = parse_commit_message(commit_message)

        card_id2, branch_name = parse_branch_name(change.new.name)

        if card_id2 is None:
            card_id = card_id1
        elif card_id1 is None:
            card_id = card_id2
        elif card_id2 is not None and card_id1 is not None:
            card_id = card_id2
        else:
            continue

        if change.created and change.new.type == 'branch':
            post_branch_activity(card_id, branch_name, commit_url)
        # elif change.closed and change.new.type == 'branch':
        #     post_merge_activity(card_id, branch_name, commit_url)
        elif branch_name == 'develop' and change.new.type == 'branch':
            post_merge_activity(card_id, branch_name, commit_url)
        else:
            post_commit_activity(card_id, branch_name, commit_message, commit_url)

    return 'OK'


webhook_paths = re.sub(r'\s', '', config_bitbucket.webhook_paths).split(',')

for webhook_path in webhook_paths:
    app.route(webhook_path, methods=['POST'])(webhook_routine)

if __name__ == '__main__':
    app.run(host=config_bitbucket.webhook_host, port=int(config_bitbucket.webhook_port), debug=True)
