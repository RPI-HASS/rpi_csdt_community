"""Test the entire site by going through and testing all links."""
from bs4 import BeautifulSoup, SoupStrainer
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client

try:
    from django.contrib.auth import get_user_model

    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class UrlTests(StaticLiveServerTestCase):
    """Test all links."""

    fixtures = ['test_data.json']

    def setUp(self):
        """Create a fake user and fake login."""
        self.user = User.objects.create_user(username='temporary', email='temporary@temp.com', password='temporary')
        self.client = Client()
        self.client.logout()
        self.assertTrue(self.client.login(username='temporary', password='temporary'))
        self.visited = {}

    def test_all_site_links(self, url='/'):
        """Test all links."""
        if url in self.visited:
            return
        self.visited[url] = True

        # Ignore URL's that point elsewhere
        if url.startswith('http://') or url.startswith('http://') or url.startswith('https://') or \
                url.startswith('//'):
            return

        # Ignore mailto links
        if url.startswith('mailto:'):
            return

        # Ignore URL that simply point to media...
        if url.startswith(settings.MEDIA_URL):
            return

        # Ignore URL that simply point to media...
        if url.startswith(settings.STATIC_URL):
            return

        # We need the HTTP_REFERER here to get past Django-likes checking
        response = self.client.get(url, **{'HTTP_REFERER': url})

        self.assertTrue(response.status_code == 200 or response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))
        if hasattr(response, 'content'):
            for link in BeautifulSoup(response.content, 'html.parser', parse_only=SoupStrainer("a")):
                if 'href' in getattr(link, 'attrs', {}):
                    self.test_all_site_links(link['href'])

    def test_API(self):
        url = '/api/demos/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 200 or response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/api/goals/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 200 or response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/api/user/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 200 or response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/api/projects/1/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 200 or response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))

    """
    # For the time being, this test doesn't serve any purpose
    def test_captcha_works(self):
        url = '/accounts/register/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content)
        images = soup.find_all(attrs={'class': 'captcha'})

        for image in images:
            import sys
            sys.stdout.write(str(image))
            sys.stdout.flush()
            response = self.client.get(image.get('src'))
            self.assertEqual(response.status_code, 200)
    """
