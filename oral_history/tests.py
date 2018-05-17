# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.admin.sites import AdminSite
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.test import TestCase
# from urllib import urlencode

from .models import Interview, OralHistory, Tag
from .forms import OHPForm, TagForm, InterviewForm
from .apps import OralHistoryConfig
from .admin import TagAdmin, InterviewAdmin, OHPAdmin

from project_share.models import Project, Application
from django_teams.models import Team

# Create your tests here.


class MockRequest(object):
    pass


request = MockRequest()


class InterviewTestCase(TestCase):
    def setUp(self):
        self.tag_admin = TagAdmin(Tag, AdminSite())
        self.int_admin = InterviewAdmin(Interview, AdminSite())
        self.ohp_admin = OHPAdmin(OralHistory, AdminSite())
        self.user = get_user_model().objects.create_user(username='test-user',
                                                         email='test@test.com',
                                                         password='testpassword')
        self.ohp = OralHistory.objects.create(project_name="Test OHP",
                                              byline="OHP Byline",
                                              summary="OHP Summary",
                                              slug="test-ohp",
                                              is_official=True,
                                              approved=True,
                                              user=self.user)
        app = Application.objects.create(name="test_app", application_type="OHP")
        self.csdt = Project.objects.create(name="csdt_proj", application=app)
        self.interview = Interview.objects.create(project=self.ohp,
                                                  full_name="John Doe",
                                                  date="Nov 20, 2018",
                                                  location="Troy, NY",
                                                  interview_by="Jane Doe",
                                                  birthplace="Anytown, USA",
                                                  occupation="Worker",
                                                  birth_year="1960",
                                                  slug="john-doe",
                                                  approved=True,
                                                  csdt_project=self.csdt,
                                                  user=self.user)
        self.classroom = Team.objects.create()

    def test_unicode_models(self):
        self.assertEqual(self.interview.__unicode__(), "Test OHP => John Doe by test-user")
        self.assertEqual(self.ohp.__unicode__(), "Project: Test OHP by test-user")

    def test_ohp_views(self):
        url = '/oralhistory/test-ohp/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/oralhistory/test-ohp/john-doe'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        # self.assertQuerysetEqual(OralHistory.objects.all(), )

    def test_interview_form(self):
        form_data = {
            'full_name': "Jane Doe",
            'date': 'November',
            'location': 'Troy, NY',
            'interview_by': 'Django',
            'birthplace': 'New York',
            'occupation': 'Teacher',
            'birth_year': '1980',
            'summary': 'Interview summary',
            'user': self.user.pk,
            'project': self.ohp.pk,
            'classroom': self.classroom.pk,
        }
        form = InterviewForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        int_form = form.save(commit=False)
        int_form.project = self.ohp
        int_form.csdt_project = self.csdt
        # team = Team.objects.get()
        # int_form.classroom = team
        form.save()
        int_form.save()
        self.assertEqual(int_form.summary, 'Interview summary')
        self.assertEqual(int_form.birth_year, '1980')
        self.assertEqual(int_form.occupation, 'Teacher')
        self.assertEqual(int_form.birthplace, 'New York')
        self.assertEqual(int_form.interview_by, 'Django')
        self.assertEqual(int_form.location, 'Troy, NY')
        self.assertEqual(int_form.date, 'November')
        self.assertEqual(int_form.full_name, 'Jane Doe')
        self.assertEqual(int_form.slug, 'jane-doe')
        # test admin actions:
        queryset = Interview.objects.all()
        self.int_admin.actions[0](self.int_admin, request, queryset)
        self.assertTrue(Interview.objects.get(slug='jane-doe').approved)
        self.int_admin.actions[1](self.int_admin, request, queryset)
        self.assertFalse(Interview.objects.get(slug='jane-doe').approved)

        # test update view

        form_data2 = {
            'full_name': "Joe Doe",
            'date': 'October',
            'location': 'Albany, NY',
            'interview_by': 'Mr. Noone',
            'birthplace': 'Mexico',
            'occupation': 'Writer',
            'birth_year': '1955',
            'summary': 'Summary of Interview',
            'user': self.user.pk,
            'project': self.ohp.pk,
            'classroom': self.classroom.pk,
        }
        self.assertTrue(self.client.login(username='test-user', password='testpassword'))

        response = self.client.post(reverse('oral_history:interview_update',
                                            kwargs={'slug': 'test-ohp',
                                                    'slug_interview': 'jane-doe'}),
                                    data=form_data2, follow=True)
        self.assertTrue(response.status_code == 200,
                        msg="Got code %s" % (response.status_code))

        self.assertContains(response, 'Thank you')

        self.assertEqual(Interview.objects.all().count(), 2)

    def test_oralhistory_form(self):
        form_data = {
            'is_official': False,
            'project_name': 'test-OHP',
            'byline': 'new oralhistory project',
            'summary': 'ohp summary',
            'slug': 'test-ohp-2',
            'user': self.user.pk}
        form = OHPForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        ohp_form = form.save()
        self.assertEqual(ohp_form.summary, 'ohp summary')
        self.assertEqual(ohp_form.byline, 'new oralhistory project')
        self.assertEqual(ohp_form.slug, 'test-ohp-2')
        self.assertEqual(ohp_form.project_name, 'test-OHP')
        self.assertEqual(ohp_form.approved, False)
        self.assertEqual(ohp_form.is_official, False)
        self.assertEqual(ohp_form.user, self.user)
        # test admin actions:
        queryset = OralHistory.objects.all()
        self.ohp_admin.actions[0](self.ohp_admin, request, queryset)
        self.assertTrue(OralHistory.objects.get(slug='test-ohp-2').approved)
        self.ohp_admin.actions[1](self.ohp_admin, request, queryset)
        self.assertFalse(OralHistory.objects.get(slug='test-ohp-2').approved)

        form_data2 = {
            'is_official': False,
            'project_name': 'test-OHP-3',
            'byline': 'new oralhistory project',
            'summary': 'ohp summary',
            'slug': 'test-ohp-3',
            'user': self.user.pk}
        self.assertTrue(self.client.login(username='test-user', password='testpassword'))

        response = self.client.post(reverse('oral_history:upload_ohp'),
                                    data=form_data2, follow=True)
        self.assertTrue(response.status_code == 200,
                        msg="Got code %s" % (response.status_code))
        # print response.content

        self.assertContains(response, 'Thank you')

        self.assertEqual(OralHistory.objects.all().count(), 3)

        form_data2 = {
            'is_official': False,
            'project_name': 'test-OHP-4',
            'byline': 'new oralhistory project',
            'summary': 'ohp summary',
            'slug': 'test-ohp-4',
        }
        response = self.client.post(reverse('oral_history:upload_ohp'),
                                    data=form_data2, follow=True)
        self.assertTrue(response.status_code == 200,
                        msg="Got code %s" % (response.status_code))
        self.assertContains(response, 'error')
        self.assertEqual(OralHistory.objects.all().count(), 3)

    def test_tag_form(self):
        interv = Interview.objects.get(slug="john-doe")
        # Interview.objects.get(slug='john-doe')
        form_data = {'hours': 0,
                     'mins': 1,
                     'secs': 25,
                     'tag': 'talks about the city',
                     'honeypot': '',
                     'approved': True}
        form = TagForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        tag_form = form.save(commit=False)
        tag_form.timestamp = 85
        tag_form.approved = True
        tag_form.interview = interv
        form.save()
        tag_form.save()
        self.assertEqual(tag_form.tag, 'talks about the city')
        self.assertEqual(tag_form.timestamp, 85)
        self.assertEqual(tag_form.interview, self.interview)
        self.assertEqual(tag_form.approved, True)
        self.assertEqual(tag_form.__unicode__(),
                         "Tag: Test OHP: John Doe => \"talks about the city\", 85 secs")
        self.assertEqual(tag_form.to_timestamp(), "01:25")
        tag_form.timestamp = 3601
        tag_form.save()
        self.assertEqual(tag_form.to_timestamp(), "01:00:01")
        # test honeypot
        form_data2 = {'hours': 0,
                      'mins': 1,
                      'secs': 25,
                      'tag': 'talks about the city',
                      'honeypot': 'male',
                      'approved': True}
        form2 = TagForm(data=form_data2)
        with self.assertRaises(ValueError):
            form2.save()
        self.assertEqual(Tag.objects.filter(
            tag='talks about the city').count(), 1)
        # test admin:
        queryset = Tag.objects.filter(pk=1)
        self.tag_admin.actions[0](self.tag_admin, request, queryset)
        self.assertTrue(Tag.objects.get(pk=1).approved)
        self.tag_admin.actions[1](self.tag_admin, request, queryset)
        self.assertFalse(Tag.objects.get(pk=1).approved)

        form_data3 = {'hours': 0,
                      'mins': 1,
                      'secs': 26,
                      'tag': 'talks about the city',
                      'honeypot': '',
                      'approved': True}

        response = self.client.post(reverse('oral_history:interview',
                                            kwargs={'slug': self.ohp.slug,
                                                    'slug_interview': interv.slug}),
                                    data=form_data3, follow=True)
        self.assertTrue(response.status_code == 200,
                        msg="Got code %s" % (response.status_code))

        self.assertContains(response, 'Thank you')
        self.assertEqual(Tag.objects.all().count(), 2)

        form_data4 = {'hours': 0,
                      'mins': 1,
                      'secs': 26,
                      'tag': 'talks about the city',
                      'honeypot': 'shouldnt be here',
                      'approved': True}
        # self.assertTrue(self.client.login(username='test-user', password='testpassword'))

        response = self.client.post(reverse('oral_history:interview',
                                            kwargs={'slug': self.ohp.slug,
                                                    'slug_interview': interv.slug}),
                                    data=form_data4, follow=True)
        self.assertTrue(response.status_code == 200,
                        msg="Got code %s" % (response.status_code))

        self.assertContains(response, 'error')
        self.assertEqual(Tag.objects.all().count(), 2)

        # logged in auto approves
        self.assertTrue(self.client.login(username='test-user', password='testpassword'))
        form_data5 = {'hours': 0,
                      'mins': 1,
                      'secs': 27,
                      'tag': 'talks about the city',
                      'honeypot': '',
                      'approved': True}

        response = self.client.post(reverse('oral_history:interview',
                                            kwargs={'slug': self.ohp.slug,
                                                    'slug_interview': interv.slug}),
                                    data=form_data5, follow=True)
        self.assertTrue(response.status_code == 200,
                        msg="Got code %s" % (response.status_code))
        self.assertContains(response, 'Thank you')
        self.assertEqual(Tag.objects.all().count(), 3)

    def test_uploadinterview_post_form(self):
        pass

    def test_apps(self):
        self.assertEqual(OralHistoryConfig.name, 'oral_history')
        # self.assertEqual(apps.get_app_config('oral_history').name, 'oral_history')
