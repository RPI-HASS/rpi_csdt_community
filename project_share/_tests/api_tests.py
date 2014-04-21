from django.core.urlresolvers import reverse
from django.conf import settings
from rest_framework import status
from rest_framework.test import APITestCase

from django.core.files import File

class ProjectTests(APITestCase):
    fixtures = ['test_data.json']
    def test_create_project(self):
        """
        Verify that we can create a project using the REST API
        """
        project_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.xml'
        screenshot_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.png'

        url = reverse('project-create')
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
