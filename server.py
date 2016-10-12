import os
from sys import platform as _platform

from flask import Flask, abort, request
from flask import request
app = Flask(__name__)


# 104.192.143.192/28
# 104.192.143.208/28
trusted_remote_addrs = list(map(
    lambda last: '104.192.143.' + str(last),
    list(range(192, 192 + 16)) + list(range(208, 208 + 16))
)) + ['127.0.0.1']


@app.before_request
def limit_remote_addr():
    if request.remote_addr not in trusted_remote_addrs:
        abort(403)


@app.route('/webhook', methods=['GET', 'POST'])
def tracking():
    if request.method == 'POST':
        data = request.get_json()
        commit_author = data['actor']['username']
        commit_hash = data['push']['changes'][0]['new']['target']['hash'][:7]
        commit_url = data['push']['changes'][0]['new']['target']['links']['html']['href']
        print('Webhook received! %s committed %s' % (commit_author, commit_hash))
        return 'OK'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)