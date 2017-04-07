from django.test import TestCase
from project_share.models import Project


class ProjectTests(TestCase):
    fixtures = ['default.json']

    def test_only_shows_published_projects(self):
        projects = Project.approved_projects().all()
        for project in projects:
            self.assertTrue(project.approved)
