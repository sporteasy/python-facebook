Python Facebook
---------------

This repository contains an open source Python library that allows you to access Facebook
Platform from your Python app.

Python Facebook is largely inspired from the Official Facebook PHP SDK.
This is a work in progress and only support the Facebook Login for now.


Usage
-----

```
from python_facebook.helpers.login import FacebookRedirectLoginHelper
from python_facebook.session import FacebookSession

app_id = '<your_app_id>'
app_secret = '<your_app_secret>'
redirect_url = 'http://<your_redirect_url>'

FacebookSession.set_default_application(app_id, app_secret)

fbrlh = FacebookRedirectLoginHelper(redirect_url)
login_url = fbrlh.get_login_url()
```

Then in the view of your redirect url:

```
fbrlh = FacebookRedirectLoginHelper(redirect_url)
session = fbrlh.get_session_from_redirect(code, state)
user_profile = FacebookRequest(
    session,
    'GET',
    '/me'
).execute().get_graph_object(GraphUser)
```

"code" and "state" values are found in the GET parameters of the redirect url.
