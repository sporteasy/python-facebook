Python Facebook
---------------

[![Build Status](https://travis-ci.org/sporteasy/python-facebook.svg?branch=master)](https://travis-ci.org/sporteasy/python-facebook)

This repository contains an open source Python library that allows you to access Facebook
Platform from your Python app.

Python Facebook is largely inspired from the [Official Facebook PHP SDK](https://github.com/facebook/php-graph-sdk).
This is a work in progress and only support the Facebook Login for now.

Installation
------------

pip install -e git+https://github.com/sporteasy/python-facebook.git@master#egg=python_facebook


Usage
-----

Facebook Login:
```
from python_facebook.sdk.facebook import Facebook
from python_facebook.sdk.persistent_data.django_persistent_data_handler import DjangoPersistentDataHandler

app_id = '<your_app_id>'
app_secret = '<your_app_secret>'
redirect_url = 'http://<your_redirect_url>'

fb = Facebook({
    'app_id': app_id,
    'app_secret': app_secret,
    'persistent_data_handler': DjangoPersistentDataHandler(django_session)
})
fbrlh = self.facebook.get_redirect_login_helper()
login_url = fbrlh.get_login_url(redirect_url, scope=['public_profile'])
```

Then in the view of your redirect url:

```
access_token = fbrlh.get_access_token({'code': code, 'state': state}, redirect_url)
```
"code" and "state" values are found in the GET parameters of the redirect url.


Getting User info with an access_token:

```
fb.get(
    '/me?fields=id,name,first_name,last_name',
    access_token=self.access_token
).get_decoded_body()

```
