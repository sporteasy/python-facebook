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
            cert='certs/DigiCertHighAssuranceEVRootCA.pem'
        )

        return GraphRawResponse(
            response.headers,
            response.text,
            response.status_code
        )
