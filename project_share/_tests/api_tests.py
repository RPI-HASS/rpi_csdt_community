from django.core.urlresolvers import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase, APILiveServerTestCase
from rest_framework.reverse import reverse as api_reverse

from django.core.files import File

class ProjectTests(APILiveServerTestCase):
    fixtures = ['test_data.json']
    def test_create_project(self):
        """
        Verify that we can create a project using the REST API
        """
        project_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.xml'
        screenshot_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.png'

        url = reverse('api-projects-list')
        data = {
            'name': 'TestProject',
            'description': 'Test description',
            'application': '1',
            'project': File(open(project_file)),
            'screenshot': File(open(screenshot_file)),
            'tags': 'CC, Default'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
    def test_get_projects(self):
        """
        Verify that we can get a list of projects for this user using the REST API
        """
        from django.test import Client
        url = reverse('api-projects-list') + "?owner=1"
        # This doesn't work with the built-in client
        # !! This was fixed in the edge version as of 2014-04-21
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verify that all the given projects belong to the given user
        # This is a lazy way of getting absolute reverse URL... Not great
        self_url = 'http://testserver' + reverse('extendeduser-detail', kwargs={'pk':1})
        for project in response.data:
          self.assertEqual(project['owner'], self_url)
