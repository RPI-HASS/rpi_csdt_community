from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
from rest_framework.test import APIClient
from blogposts.models import Post
from comments.models import Comment

User = get_user_model()


class tests(LiveServerTestCase):
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

    def test_blogs(self):
        """Create, visit, comment on, and delete comment"""
        self.user = User.objects.get(username="test")
        self.assertTrue(self.client.login(username='test', password='test'))
        self.post = Post.objects.create(user=self.user, title="example", slug="example", content="example",
                                        publish="2018-02-08")
        self.post = Post.objects.create(user=self.user, title="example2", slug="example2", content="example2",
                                        publish="2018-02-08")
        self.post = Post.objects.create(user=self.user, title="example3", slug="example3", content="example3",
                                        publish="2018-01-08")
        self.post = Post.objects.create(user=self.user, title="example4", slug="example4", content="example4",
                                        publish="2017-02-08")
        self.assertTrue(self.client.login(username='test', password='test'))
        url = '/news/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/news/?tag=Events'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/news/example/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        response = self.client.post(url, {'content_type': 'post', 'object_id': 1,
                                          'content': 'hello'})
        self.assertTrue(response.status_code == 302 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        Comment.objects.create(user=self.user, content_type=self.post.get_content_type, object_id=1, content="example")
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/blogcomments/1/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        url = '/blogcomments/1/delete/'
        self.user = User.objects.create_user(username='test2', email='test2@test.com', password='test2')
        self.assertTrue(self.client.login(username='test2', password='test2'))
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 403,
                        msg="Got code %s on %s" % (response.status_code, url))

        self.user = User.objects.get(username="test")
        self.assertTrue(self.client.login(username='test', password='test'))

        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 300 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        response = self.client.post(url, {})
        self.assertTrue(response.status_code == 302 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))


    def test_blog_forms(self):
        form = PostForm({
            "title": "example",
            "content": "example",
            "image": "",
            "draft": "example",
            "publish": "2018-02-20",
            })
        self.assertTrue(form.is_valid())
        post = form.save()
        self.assertTrue(post.title == "example")
        self.assertTrue(post.content == "example")

    def test_blog_views(self):
        self.user = User.objects.get(username="test")
        self.assertTrue(self.client.login(username='test', password='test'))
        url = '/blogcomments/1000/'
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 404,
                        msg="Got code %s on %s" % (response.status_code, url))
        self.post = Post.objects.create(user=self.user, title="example", slug="example", content="example",
                                        publish="2018-10-08")
        self.assertTrue(self.client.login(username='test', password='test'))
        url = '/news/example/'
        response = self.client.post(url, {})
        self.assertTrue(response.status_code == 302 or response.status_code == 200,
                        msg="Got code %s on %s" % (response.status_code, url))
        self.client.logout()
        response = self.client.get(url, **{'HTTP_REFERER': url})
        self.assertTrue(response.status_code == 404, msg="Got code %s on %s" % (response.status_code, url))
        event_calendar = get_calendar([self.post])
        self.assertTrue(len(event_calendar) == 1, 
            msg="Got length %d on get_calendar" %(len(event_calendar)))