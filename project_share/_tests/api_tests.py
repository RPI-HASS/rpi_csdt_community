from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save 
from django.dispatch import receiver
from rest_framework import status
from rest_framework.test import APITestCase, APILiveServerTestCase
from rest_framework.reverse import reverse as api_reverse

from django.core.files import File
from project_share.models import Project

from time import sleep
import sys
import pprint

class ProjectTests(APILiveServerTestCase):
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
        sys.stdout.flush()
    """

  
    def test_upload_file(self):
        """
        Verifies that we can upload a file and get back the URL
          of the uploaded file
        """
        screenshot_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.png'
        url = reverse('file-create')

        with open(screenshot_file) as f:
            self.client.login(username='test', password='test')
            response = self.client.post(url, {'file': f})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.client.logout()

    def test_upload_file_requires_login(self):
        """
        Verifies that we can upload a file and get back the URL
          of the uploaded file
        """
        screenshot_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.png'
        url = reverse('file-create')

        with open(screenshot_file) as f:
            response = self.client.post(url, {'file': f})
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_project(self):
        """
        Verify that we can create a project using the REST API
        """
        project_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.xml'
        screenshot_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.png'
        
        self.client.login(username='test', password='test')

        # Try uploading the screenshot
        image_id = -1
        with open(screenshot_file) as f:
            response = self.client.post(reverse('file-create'), {'file':f})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            image_id = response.data['id']

        # Upload the XML file
        xml_id = -1
        with open(project_file) as f:
            response = self.client.post(reverse('file-create'), {'file':f})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            xml_id = response.data['id']


        ProjectTests.saved = False
        @receiver(pre_save, sender=Project)
        def func(sender, **kwargs):
            ProjectTests.saved = True

        url = reverse('api-projects-list')
        data = {
            'name': 'test_create_project',
            'description': 'Test description',
            'application': 1,
            'tags': 'CC, Default',
            'owner': 1,
            'project': xml_id,
            'screenshot': image_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectTests.saved, True)
        self.client.logout()
    
    def test_can_update_project(self):
        project_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.xml'
        screenshot_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.png'

        self.client.login(username='test', password='test')

        # Try uploading the screenshot
        image_id = -1
        with open(screenshot_file) as f:
            response = self.client.post(reverse('file-create'), {'file':f})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            image_id = response.data['id']

        # Upload the XML file
        xml_id = -1
        with open(project_file) as f:
            response = self.client.post(reverse('file-create'), {'file':f})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            xml_id = response.data['id']


        ProjectTests.saved = False
        @receiver(pre_save, sender=Project)
        def func(sender, **kwargs):
            ProjectTests.saved = True

        url = reverse('api-projects-list')
        data = {
            'name': 'test_create_project',
            'description': 'Test description',
            'application': 1,
            'tags': 'CC, Default',
            'owner': 1,
            'project': xml_id,
            'screenshot': image_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProjectTests.saved, True)

        # Try updating it
        ProjectTests.saved = False
        data['id'] = response.data['id']
        response = self.client.put(url+repr(data['id'])+'/', data, format='json')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ProjectTests.saved, True)

        self.client.logout()

    def test_can_create_project_and_upload_project(self):
        project_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.xml'
        screenshot_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.png'
        self.client.login(username='test', password='test')

        # Try uploading the screenshot
        image_id = -1
        with open(screenshot_file) as f:
            response = self.client.post(reverse('file-create'), {'file':f})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            image_id = response.data['id']

        # Upload the XML file
        xml_id = -1
        with open(project_file) as f:
            response = self.client.post(reverse('file-create'), {'file':f})
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            xml_id = response.data['id']

        # Upload the project
        url = reverse('api-projects-list')
        data = {
            'name': 'test_can_create_project_and_upload_project',
            'description': 'Test description',
            'application': 1,
            'tags': 'CC, Default',
            'owner': 1,
            'project': xml_id,
            'screenshot': image_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


        # Logout
        self.client.logout()

    def test_create_requires_authentication_project(self):
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
            'tags': 'CC, Default'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_projects(self):
        """
        Verify that we can get a list of projects for this user using the REST API
        """
        from django.test import Client
        url = reverse('api-projects-list') + "?owner=1"
        # This doesn't work with the built-in client
        # !! This was fixed in the edge version as of 2014-04-21
        # !! Edge version of Django Rest Framework :)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # verify that all the given projects belong to the given user
        # This is a lazy way of getting absolute reverse URL... Not great
        self_url = 1
        for project in response.data:
          self.assertEqual(project['owner'], self_url)
