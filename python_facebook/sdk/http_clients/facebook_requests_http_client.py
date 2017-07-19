import os
import requests

from python_facebook.sdk.http.graph_raw_response import GraphRawResponse


class FacebookRequestsHttpClient(object):

    def send(self, url, method, body, headers, timeout):
        method = getattr(requests, method.lower())

        response = method(
            url,
            data=body,
            headers=headers,
            timeout=timeout,
            verify=os.path.join(os.path.dirname(__file__), 'certs/DigiCertHighAssuranceEVRootCA.pem')
        )

        return GraphRawResponse(
            response.headers,
            response.text,
            response.status_code
        )
