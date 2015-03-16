Python Facebook
---------------

This repository contains an open source Python library that allows you to access Facebook
Platform from your Python app.

Python Facebook is largely inspired from the [Official Facebook PHP SDK](https://github.com/facebook/facebook-php-sdk-v4).
This is a work in progress and only support the Facebook Login for now.


Usage
-----

```
from python_facebook.helpers.login import FacebookRedirectLoginHelper
from python_facebook.session import FacebookSession

app_id = '<your_app_id>'
app_secret = '<your_app_secret>'
redirect_url = 'http://<your_redirect_url>'

graph = FacebookGraph(app_id, app_secret)
login_url = graph.get_login_url(redirect_url)
```

Then in the view of your redirect url:

```
graph.set_session_from_redirect(redirect_url, code, state)
user = graph.get_graph_user()
```
"code" and "state" values are found in the GET parameters of the redirect url.


Getting info with an access_token:

```
access_token_str = u'<access_token_str>'

graph = FacebookGraph(APP_ID, APP_SECRET)
graph.set_access_token(access_token_str)
info = graph.get_access_token_info()
user = graph.get_graph_user()
```
