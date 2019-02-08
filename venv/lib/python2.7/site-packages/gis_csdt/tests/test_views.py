from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from gis_csdt.models import DataPoint, Dataset, Location, MapPoint, PhoneNumber, Sensor
from django.contrib.auth.models import User
from gis_csdt.views import DataToGSM7
from django.contrib.auth import get_user_model
from django.test import LiveServerTestCase
import urllib

User = get_user_model()


class AllViewTestsNoData(APITestCase):
    def test_no_datasets(self):
        response = self.client.get('/api-ds/')
        self.assertEqual(response.status_code, 200)

    def test_no_mappoints(self):
        response = self.client.get('/api-mp/')
        self.assertEqual(response.status_code, 200)

    def test_no_newtags(self):
        response = self.client.get('/api-newtag/')
        self.assertEqual(response.status_code, 200)

    def test_no_polygons(self):
        response = self.client.get('/api-poly/')
        self.assertEqual(response.status_code, 200)

    def test_no_mappoints_geojson(self):
        response = self.client.get('/api-test/')
        self.assertEqual(response.status_code, 200)

    def test_no_mappolygons_count_of_points(self):
        response = self.client.get('/api-count/')
        self.assertEqual(response.status_code, 200)

    def test_no_mappolygons_analysis_around_point(self):
        response = self.client.get('/api-dist/')
        self.assertEqual(response.status_code, 400)


class SMSCreateData(LiveServerTestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='test',
                                                  email='test@test.test',
                                                  password='test')
        self.assertTrue(self.client.login(username='test', password='test'))

    def test_SMS(self):
        set = Dataset.objects.create(name='test')
        set.save()
        mappoint = MapPoint.objects.create(lat=0, lon=0)
        mappoint.save()
        sensor = Sensor.objects.create(name='test', mappoint=mappoint, user=self.user)
        sensor.save()
        phNum = PhoneNumber.objects.create(phone_number=11111111111, user=self.user)
        phNum.save()
        data = [1, 0, 128, 129, 300, 10001]
        data[0] = sensor.id
        string = DataToGSM7(data)
        postData = {'Body': string.encode('utf-8'), 'From': phNum.phone_number}
        response = self.client.post('/api-SMS/', urllib.urlencode(postData), content_type='application/x-www-form-urlencoded')
        self.assertEqual(DataPoint.objects.get(pk=6).value, 10001)


class TestAddMapPointAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='test',
                                                  email='test@test.test',
                                                  password='test')
        self.assertTrue(self.client.login(username='test', password='test'))

    def test_api_can_add_mappoint(self):
        original_count = MapPoint.objects.all().count()
        self.mp_data = {'lat': 31.7, 'lon': 68.9}
        self.response = self.client.post('/api-addmp/', self.mp_data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MapPoint.objects.all().count(), original_count + 1)


class TestAddDatasetAPI(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(username='test',
                                                  email='test@test.test',
                                                  password='test')
        self.assertTrue(self.client.login(username='test', password='test'))

    def test_api_can_add_dataset(self):
        original_count = Dataset.objects.all().count()
        location = Location.objects.create(state_field='NY')
        location.save()
        self.ds_data = {'name': 'Catskill', 'location_id': location.id}
        self.response = self.client.post('/api-addds/', self.ds_data, format="json")
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dataset.objects.all().count(), original_count + 1)
        self.assertEqual(Dataset.objects.get(name='Catskill').location.state_field, 'NY')


class TestAroundPointView(TestCase):

    def test_can_load_page(self):
        response = self.client.get('/around-point/')
        self.assertEqual(response.status_code, 200)

    def test_contains_mappoint(self):
        mp1 = MapPoint(lat=43.0831, lon=73.7846)
        mp1.save()
        mp2 = MapPoint(lat=20.1515, lon=25.2523)
        mp2.save()
        response = self.client.get('/api-dist/', {'min_lat': 12.12, 'max_lat': 108.00, 'dataset': '1,2', 'unit': 'km'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(mp1))
        response = self.client.get('/around-point/%d/' % mp2.id)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(mp2))


class TestAroundPointNoValueView(TestCase):

    def test_can_load_page(self):
        self.user = User.objects.create_superuser(username='test',
                                                  email='test@test.test',
                                                  password='test')
        self.assertTrue(self.client.login(username='test', password='test'))
        mp1 = MapPoint(lat=43.0831, lon=73.7846)
        mp1.save()
        response = self.client.get('/api-dist2/', {'min_lat': 12.12, 'max_lat': 108.00, 'dataset': '1,2', 'unit': 'km'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(mp1))
        response = self.client.get('/api-dist2/', {'min_lat': 12.12, 'max_lat': 108.00, 'dataset': '1,2', 'unit': ['km', 'm']})
        self.assertEqual(response.status_code, 400)


class TestCountPointsInPolygonView(TestCase):

    def test_can_load_page(self):
        mp1 = MapPoint(lat=43.0831, lon=73.7846)
        mp1.save()
        response = self.client.get('/api-count/', {'min_lat': 12.12, 'max_lat': 108.00, 'dataset': '1,2',
                                                   'unit': 'km', 'state': 'NY'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, str(mp1))
