'''Tests for RPI CSDT'''

# from django.test import TestCase

from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client
try:
    from django.contrib.auth import get_user_model
    USER = get_user_model()
except ImportError:
    # from django.contrib.auth.models import User

    from BeautifulSoup import BeautifulSoup, SoupStrainer


class UrlTests(StaticLiveServerTestCase):
    ''' Test of URLs'''
    fixtures = ['test_data.json']

    def setUp(self):
        # user = USER.objects.create_user('temporary',
        # 'temporary@gmail.com', 'temporary')
        self.client = Client()
        self.client.login(username='temporary', password='temporary')
        self.visited = {}

    def test_all_site_links(self, url='/'):
        '''Test All Site Links'''
        if url in self.visited:
            return
        self.visited[url] = True

        # Ignore URL's that point elsewhere
        if url.startswith('http://') or url.startswith('http://') \
                or url.startswith('https://') or url.startswith('//'):
            return

        # Ignore URL that simply point to media...
        if url.startswith(settings.MEDIA_URL):
            return

        # We need the HTTP_REFERER here to get past Django-likes checking
        response = self.client.get(url, **{'HTTP_REFERER': url})

        self.assertTrue(response.status_code == 200
                        or response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))

        for link in BeautifulSoup(response.content,
                                  parseOnlyThese=SoupStrainer('a')):
            if any('href' in el for el in link.attrs):
                self.test_all_site_links(link['href'])
