from django.contrib.auth import get_user_model
# from rest_framework.test import APITestCase, APITransactionTestCase
from django.test import LiveServerTestCase
from rest_framework.test import APIClient
from django_teams.models import Team

User = get_user_model()


class ProjectTests(LiveServerTestCase):
    fixtures = ['default.json']

    """@staticmethod
    def setUpClass():
        settings.DEBUG = True

    def tearDown(self):
        sys.stdout.write("Tear down\n")
        sys.stdout.flush()
        from django.db import connection
        pp = pprint.PrettyPrinter(indent=4)
        sys.stdout.write("SQL: ")
        pp.pprint(connection.queries)
        sys.stdout.flush()"""

    def setUp(self):
        self.client = APIClient()

    def test_project_views(self):
        """Go to update, unpublish, etc."""
        self.assertTrue(self.client.login(username='test', password='test'))
        self.team = Team.objects.create()
        url = '/projects/?filter=1&orderby=-id&q=test'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/projects/1/run'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/projects/1/edit'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        response = self.client.post(url, {'publish_project': 'publish_project', 'team': self.team})
        self.assertTrue(response.status_code == 302 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/projects/1/unpublish'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        response = self.client.post(url, {'Unpublish': 'Unpublish'})
        self.assertTrue(response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/projects/1/delete'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/projects/1/publish'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        response = self.client.post(url, response.content, content_type="application/x-www-form-urlencoded")
        self.assertTrue(response.status_code == 302,
                        msg="Got code %s on %s" % (response.status_code, url))

    def test_user_views(self):
        """update your profile"""
        self.assertTrue(self.client.login(username='test', password='test'))
        url = '/users/edit/1'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        self.user = User.objects.get(username="test")
        with open('project_share/fixtures/test.jpg') as file:
            data = {u'username': [u'test'], u'bio': [u'I am the best.'],
                    u'display_name': [u'test'], u'gender': [u'test'], u'age': [u'1'],
                    u'race': [u'test'], u'avatar': file, u'email': [u'test@test.com']}
            response = self.client.post(url, data)
            self.assertTrue(response.status_code == 302,
                            msg="Got code %s on %s" % (response.status_code, url))
        self.superUser = User.objects.create_superuser(username="test2", password='test2')
        self.assertTrue(self.superUser.is_superuser) 

    def test_application_view(self):
        """update your profile"""
        self.assertTrue(self.client.login(username='test', password='test'))
        url = '/applications/1/run'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
