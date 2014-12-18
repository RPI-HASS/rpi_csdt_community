from django.test import TestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test.client import Client

from project_share.models import *

class ProjectTests(TestCase):
    fixtures = ['default.json']

    def test_only_shows_published_projects(self):
        projects = Project.approved_objects.all()

        for project in projects:
            self.assertTrue(project.approved)
