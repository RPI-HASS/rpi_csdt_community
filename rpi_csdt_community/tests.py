from django.test import TestCase
from django.test.client import Client
from django.conf import settings

from BeautifulSoup import BeautifulSoup, SoupStrainer

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class UrlTests(TestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client = Client()
        self.client.login(username='temporary', password='temporary')
        self.visited = {}

    def test_all_site_links(self, url='/'):
        if url in self.visited:
            return
        self.visited[url] = True

        # Ignore URL that simply point to media...
        if url.startswith(settings.MEDIA_URL):
            return

        response = self.client.get(url)

        self.assertTrue(response.status_code == 200 or response.status_code == 302)

        for link in BeautifulSoup(response.content, parseOnlyThese=SoupStrainer('a')):
            if any('href' in el for el in link.attrs):
                self.test_all_site_links(link['href'])
