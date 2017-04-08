from BeautifulSoup import BeautifulSoup, SoupStrainer
from django.conf import settings
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class UrlTests(StaticLiveServerTestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client = Client()
        self.client.login(username='temporary', password='temporary')
        self.visited = {}

    def test_all_site_links(self, url='/'):
        if url in self.visited:
            return
        self.visited[url] = True

        # Ignore URL's that point elsewhere
        if url.startswith('http://') or url.startswith('http://') or url.startswith('https://') or\
           url.startswith('//'):
            return

        # Ignore URL that simply point to media...
        if url.startswith(settings.MEDIA_URL):
            return

        # We need the HTTP_REFERER here to get past Django-likes checking
        response = self.client.get(url, **{'HTTP_REFERER': url})

        """
        import sys
        sys.stdout.write(url + '->' + repr(response.status_code)+'\n')
        sys.stdout.flush()
        """

        self.assertTrue(response.status_code == 200 or response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))

        for link in BeautifulSoup(response.content, parseOnlyThese=SoupStrainer('a')):
            if any('href' in el for el in link.attrs):
                self.test_all_site_links(link['href'])

    """
    # For the time being, this test doesn't serve any purpose
    def test_captcha_works(self):
        url = '/accounts/register/'

        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        soup = BeautifulSoup(response.content)
        images = soup.findAll(attrs={'class': 'captcha'})

        for image in images:
            import sys
            sys.stdout.write(str(image))
            sys.stdout.flush()
            response = self.client.get(image.get('src'))
            self.assertEqual(response.status_code, 200)
    """
