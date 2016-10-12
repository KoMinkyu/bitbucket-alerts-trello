from flask import Flask, abort, request
from flask import request

app = Flask(__name__)

# 104.192.143.192/28
# 104.192.143.208/28
trusted_remote_addrs = list(map(
    lambda last: '104.192.143.' + str(last),
    list(range(192, 192 + 16)) + list(range(208, 208 + 16))
))

BITBUCKET_WEBHOOK_PATH = '/webhook'

webhook_paths = [
    BITBUCKET_WEBHOOK_PATH,
]


@app.before_request
def limit_remote_addr():
    if (is_webhook_path(request.path) and
            not is_trusted_remote_addrs(request.remote_addr)):
        abort(403)


def is_webhook_path(path):
    return path in webhook_paths


def is_trusted_remote_addrs(remote_addr):
    return remote_addr in trusted_remote_addrs


@app.route(BITBUCKET_WEBHOOK_PATH, methods=['GET', 'POST'])
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
