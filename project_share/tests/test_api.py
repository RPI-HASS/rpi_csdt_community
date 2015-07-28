from django.core.urlresolvers import reverse
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.test import APIClient
#from rest_framework.test import APITestCase, APITransactionTestCase
from django.test import LiveServerTestCase
from rest_framework.reverse import reverse as api_reverse

from django.core.files import File
from project_share.models import Project
from django.contrib.auth import get_user_model
User = get_user_model()

from time import sleep
import sys
import pprint

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

    def create_project(self, name="test project", description="test project description"):
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
            'name': name,
            'description': description,
            'application': 1,
            'tags': 'CC, Default',
            'owner': 1,
            'project': xml_id,
            'screenshot': image_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        return response


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

        self.client.login(username='test', password='test')
        project = Project.objects.all()[0]
        original_name = project.name


        data = {
            "name": "Hamburger",
            "id": project.id,
            "application": project.application.id
        }

        # Try updating it
        ProjectTests.saved = False
        url = reverse('api-projects-detail', kwargs={'pk': data['id']})

        response = self.client.put(url, data, format='json')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(original_name != response.data['name'])

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

        self_url = 1
        for project in response.data:
          self.assertEqual(project['owner'], self_url)
		  
    def test_get_teams(self):
        """
        Verify that we can get a list of projects for this user using the REST API
        """
        from django.test import Client
        url = reverse(r'^api/team') + "?owner=1"
        # This doesn't work with the built-in client
        # !! This was fixed in the edge version as of 2014-04-21
        # !! Edge version of Django Rest Framework :)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self_url = 1
        for project in response.data:
          self.assertEqual(project['owner'], self_url)

    def test_saving_published_project_creates_unpublished_project(self):
        """
        This is related to bug #12 (https://github.com/GK-12/rpi_csdt_community/issues/12)
        The test should verify that saving a project that has already been
          published results in a non-published project being created
        """
        # First, create the project
        response = self.create_project()
        response.render()

        self.assertEqual(response.data['approved'], False)

        # Publish the project
        project = Project.objects.get(pk=response.data['id'])
        project.approved = True
        project.save()

        # Try updating the project
        data = {
            'name': project.name,
            'id': project.id,
            'application': project.application.id
        }

        url = reverse('api-projects-detail', kwargs={'pk': data['id']})

        response = self.client.put(url, data, format='json')
        response.render()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify that the primary keys are different
        self.assertTrue(response.data['id'] != project.id)
        self.assertFalse(response.data['approved'])

    def test_republished_project_has_user(self):
      # First, create the project
      response = self.create_project()
      response.render()

      self.assertEqual(response.data['approved'], False)

      # Publish the project
      project = Project.objects.get(pk=response.data['id'])
      project.approved = True
      project.save()

      # Try updating the project
      data = {
          'name': project.name,
          'id': project.id,
          'application': project.application.id
      }

      url = reverse('api-projects-detail', kwargs={'pk': data['id']})

      response = self.client.put(url, data, format='json')
      response.render()
      self.assertEqual(response.status_code, status.HTTP_200_OK)

      # Verify that the primary keys are different
      self.assertTrue(response.data['id'] != project.id)
      self.assertTrue(response.data['owner'] != None)
      self.assertFalse(response.data['approved'])

    def test_saving_published_project_creates_unpublished_project_using_post(self):
      """
      This is related to bug #12 (https://github.com/GK-12/rpi_csdt_community/issues/12)
      The test should verify that saving a project that has already been
        published results in a non-published project being created
      """
      # First, create the project
      response = self.create_project()
      response.render()

      self.assertEqual(response.data['approved'], False)

      # Publish the project
      project = Project.objects.get(pk=response.data['id'])
      project.approved = True
      project.save()

      # Try updating the project
      data = {
          'name': project.name,
          'id': project.id,
          'application': project.application.id
      }

      url = reverse('api-projects-list')

      response = self.client.post(url, data, format='json')
      response.render()
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

      # Verify that the primary keys are different
      self.assertTrue(response.data['id'] != project.id)
      self.assertFalse(response.data['approved'])

    def test_saving_new_project_sets_correct_owner(self):
        """ This is related to bug #41 (https://github.com/GK-12/Snap--Build-Your-Own-Blocks/issues/41)
        The test should verify taht the owner is correctly set when the project is
        first saved from a "raw" application (not another project)
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

        # Upload the project
        url = reverse('api-projects-list')
        data = {
            'name': 'abd',
            'description': '123',
            'application': 1,
            'tags': 'CC, Default',
            'project': xml_id,
            'screenshot': image_id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        project = Project.objects.get(pk=response.data['id'])
        self.assertEqual(project.owner, User.objects.get(username='test'))
