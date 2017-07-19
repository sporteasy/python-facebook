from python_facebook.sdk.http.graph_raw_response import GraphRawResponse


class FooClientInterface(object):

    def send(self, url, method, body, headers, timeout):
        return GraphRawResponse(
            "HTTP/1.1 1337 OK\r\nDate: Mon, 19 May 2014 18:37:17 GMT",
            '{"data":[{"id":"123","name":"Foo"},{"id":"1337","name":"Bar"}]}'
        )
