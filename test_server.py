# -*- coding: utf-8 -*-

import pytest
import server

@pytest.fixture
def client(request):
    server.app.config['TESTING'] = True
    client = server.app.test_client()

    def teardown():
        pass

    request.addfinalizer(teardown)

    return client


def post_webhook_from_trusted_remote_addr(client):
    return client.post('/webhook', environ_base={'REMOTE_ADDR': '111.11.1.1'})


def post_non_webhook_path(client):
    return client.post('/test')


def test_limit_remote_addr(client):
    rv = post_webhook_from_trusted_remote_addr(client)
    assert rv.status_code == 403

    rv = post_non_webhook_path(client)
    assert rv.status_code != 403