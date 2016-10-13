# bitbucket_alerts_trello
Developer's bitbucket activities are going to be written as `Activity` on specified `Trello Card`

# Usage
Step 1. Setup virtualenv and required environments.

``` sh
virtualenv env
source env/bin/activate
source flask_env
```

Step 2. Run flask server.

``` sh
flask run
```

# Tests

``` sh
pytest alertserver/test_server.py
```