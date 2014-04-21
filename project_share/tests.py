from django.test import TestCase
from django.test.client import Client
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.files import File

from project_share.models import Project

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


class ApprovalTests(TestCase):
    fixtures = ['test_data.json']
    def setUp(self):
        user = User.objects.create_user('temporary', 'temporary@gmail.com', 'temporary')
        self.client = Client()
        self.client.login(username='temporary', password='temporary')

    def test_new_project_needs_approval(self):
        original_approved = Project.approved_objects.count()
        project_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.xml'
        screenshot_file = settings.PROJECT_ROOT + '/samples/CC/CC-Default.png'
        result = self.client.post(reverse('project-create'), {
            'name': 'TestProject',
            'description': 'Test description',
            'application': '1',
            'project': File(open(project_file)),
            'screenshot': File(open(screenshot_file)),
            'tags': 'CC, Default'
        }, follow=True)

        self.assertEqual(result.status_code, 200)

        # There should only be the one approved project in the list of project
        self.assertEquals(Project.approved_objects.count(), original_approved)

from _tests.api_tests import *
