from tinyurl.url import URL
import os, json
import falcon

class TinyURLResource:
    """The tiny-url resource for getting and creating tiny urls."""
    ROUTES = ('/', '/{url_hash}')

    @staticmethod
    def payload(req):
        """Return the POST body from request."""
        try:
            data = req.stream.read().decode('utf-8')
            return json.loads(data)
        except:
            return {}


    def on_get(self, req, resp, url_hash=None):
        """Handle tiny-url retrieval by url hash."""
        resp.status = falcon.HTTP_404
        
        record = URL.find(url_hash)
        if record:
            resp.set_header('Location', record['url'])
            resp.status = falcon.HTTP_301
            

    def on_post(self, req, resp):
        """Handle tiny-url creation."""

        url = TinyURLResource.payload(req) \
            .get('url')

        resp.media = URL.minify(url)
        resp.status = falcon.HTTP_201


# startup our api and expose wsgi
if 'gunicorn' in os.environ.get('SERVER_SOFTWARE',''):
    application = falcon.API()

    for route in TinyURLResource.ROUTES:
        application.add_route(route, TinyURLResource())
