from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.views import APIView
from gis_csdt.models import DataElement, DataField, Dataset, DatasetNameField, MapElement, MapPoint, MapPolygon, Tag, TagIndiv
from gis_csdt.serializers import AnalyzeAreaNoValuesSerializer, AnalyzeAreaSerializer, CountPointsSerializer, DataPointSerializer, DatasetSerializer, NewTagSerializer, SensorSerializer, TestSerializer
from django.contrib.gis.geos import Polygon, MultiPolygon, Point, fromstr, GEOSGeometry
from django.contrib.auth import get_user_model
from django.http import HttpRequest, QueryDict

User = get_user_model()


class TestDatasetSerializer(TestCase):
    def test_dataset_serializer(self):
        ds = Dataset(name="RPI")
        ds.save()
        data = {'name': 'RPI'}
        serializer = DatasetSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.get_count(ds), 0)
        me = MapElement(dataset=ds)
        me.save()
        self.assertEqual(serializer.get_count(ds), 1)


class TestTestSerializer(TestCase):
    fixtures = ['test_data.json']

    def test_can_create_serializer(self):
        mp = MapPoint.objects.get(pk=1)
        setattr(mp, "field1", "mp_field1")
        setattr(mp, "field2", "mp_field2")
        names = DatasetNameField(field1_name="field1", field2_name="field2", field3_name="field3")
        names.save()
        ds = Dataset(name="ds", names=names)
        ds.save()
        p1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
        p2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
        mpoly = MultiPolygon(p1, p2)
        polygon = MapPolygon(lat='42.7302', lon='73.6788', field1=1.0, field2=2.0, mpoly=mpoly, dataset=ds)
        polygon.save()
        me = MapElement(dataset=ds, mappoint=mp, mappolygon=polygon)
        me.save()
        df = DataField(dataset=ds, field_type='I', field_name='int_data', field_en='test')
        df.save()
        element = DataElement(mapelement=me, datafield=df, int_data=23)
        element.save()
        request = RequestFactory().put('/?data=all')
        self.user = User.objects.get(username='test')
        request.user = self.user
        # convert the HTTP Request object to a REST framework Request object
        self.request = APIView().initialize_request(request)
        serializer = TestSerializer(context={'request': self.request})
        expected_address = {"street": "", "city": "Troy", "state": "NY", "zipcode": "", "county": ""}
        self.assertEqual(serializer.get_address(me), expected_address)
        self.assertEqual(serializer.get_data(me)['test'], 23)
        self.assertEqual(serializer.get_geom(me)['type'], 'MultiPolygon')

        tag1 = Tag(dataset=ds, tag='tag1', approved=True, count=1)
        tag1.save()
        tag2 = Tag(dataset=ds, tag='tag2', approved=True, count=1)
        tag2.save()
        tagindiv1 = TagIndiv(tag=tag1, mapelement=me)
        tagindiv1.save()
        tagindiv2 = TagIndiv(tag=tag2, mapelement=me)
        tagindiv2.save()
        self.assertTrue('tag1' in serializer.get_tags(me))
        self.assertTrue('tag2' in serializer.get_tags(me))


class TestCountPointsSerializer(TestCase):
    fixtures = ['test_data.json']

    def test_can_create_serializer(self):
        ds = Dataset.objects.get(pk=1)
        names = DatasetNameField(field1_en='en1', field2_en='en2')
        names.save()
        setattr(ds, "names", names)
        p1 = Polygon(((0, 0), (0, 1), (1, 1), (0, 0)))
        p2 = Polygon(((1, 1), (1, 2), (2, 2), (1, 1)))
        mpoly = MultiPolygon(p1, p2)
        polygon = MapPolygon(lat='42.7302', lon='73.6788', field1=1.0, field2=2.0, mpoly=mpoly, dataset=ds)
        polygon.save()

        df1 = DataField(dataset=ds, field_type='I', field_name='int_data', field_en='test1')
        df1.save()
        df2 = DataField(dataset=ds, field_type='F', field_name='float_data', field_en='test2')
        df2.save()
        df3 = DataField(dataset=ds, field_type='C', field_name='char_data', field_en='test3')
        df3.save()

        tag1 = Tag(dataset=ds, tag="tag1")
        tag1.save()
        tag2 = Tag(dataset=ds, tag="tag2")
        tag2.save()
        tag3 = Tag(dataset=ds, tag="tag3")
        tag3.save()

        element1 = DataElement(mapelement=polygon, datafield=df1, int_data=23)
        element1.save()
        element2 = DataElement(mapelement=polygon, datafield=df2, float_data=2.34)
        element2.save()
        element3 = DataElement(mapelement=polygon, datafield=df3, char_data='abc')
        element3.save()

        request = HttpRequest()
        qdict = QueryDict('', mutable=True)
        qdict.update({'tags': 'tag1,tag2,tag3'})
        qdict.update({'street': '8th St', 'city': 'Troy', 'state': 'NY'})
        qdict.update({'max_lat': '52.5', 'min_lat': '18.9', 'max_lon': '108.1', 'min_lon': '22.1'})
        qdict.update({'radius': 5, 'center': '42.7302,73.6788'})
        request.GET = qdict
        # convert the HTTP Request object to a REST framework Request object
        self.request = APIView().initialize_request(request)
        serializer = CountPointsSerializer(context={'request': self.request})
        count = serializer.get_count(polygon)
        self.assertEqual(count['test1'], 23)
        self.assertEqual(count['test2'], 2.34)
        self.assertEqual(count['en2'], 2.0)


class TestAnalyzeAreaSerializer(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        ds = Dataset.objects.get(pk=3)
        self.mp = MapPoint.objects.get(pk=1)
        self.mp.dataset = ds
        self.mp.point = Point(5, 23)
        MapPoint(lat=23.41, lon=98.0, dataset=ds, point=Point(5, 23)).save()
        tag1 = Tag(dataset=ds, tag='tag1', approved=True, count=1)
        tag1.save()
        tag2 = Tag(dataset=ds, tag='tag2', approved=True, count=1)
        tag2.save()
        tagindiv1 = TagIndiv(tag=tag1, mapelement=self.mp)
        tagindiv1.save()
        tagindiv2 = TagIndiv(tag=tag2, mapelement=self.mp)
        tagindiv2.save()
        p1 = GEOSGeometry("SRID=4326;POLYGON ((5 23.00902982868961, 5.004877257506506 23.00781998654152, 5.00844745207902 23.00451469036915, 5.009753953024734 22.99999969967893, 5.008446890194161 22.99548485657674, 5.004876695621637 22.99217985558042, 5 22.99097016102037, 4.995123304378363 22.99217985558042, 4.991553109805839 22.99548485657674, 4.990246046975266 22.99999969967893, 4.99155254792098 23.00451469036915, 4.995122742493493 23.00781998654153, 5 23.00902982868961))")
        p2 = GEOSGeometry("SRID=4326;POLYGON ((5 23.02708945518625, 5.014633459242311 23.02345948568706, 5.025344042308789 23.01354271143227, 5.029261858728946 22.99999729711045, 5.025338985345226 22.98645321108062, 5.014628402277986 22.97653909341024, 5 22.97291045220348, 4.985371597722013 22.97653909341024, 4.974661014654773 22.98645321108062, 4.970738141271054 22.99999729711045, 4.974655957691211 23.01354271143227, 4.985366540757689 23.02345948568706, 5 23.02708945518625))")
        p3 = GEOSGeometry("SRID=4326;POLYGON ((5 23.0451490404854, 5.024391911722986 23.03909835241012, 5.042242881329157 23.02256891874033, 5.048769763397385 22.99999249197385, 5.042228834209113 22.97741975490609, 5.024377864597061 22.96089770063709, 5 22.95485070226389, 4.975622135402939 22.96089770063709, 4.957771165790887 22.97741975490609, 4.951230236602615 22.99999249197385, 4.957757118670842 23.02256891874033, 4.975608088277014 23.03909835241012, 5 23.0451490404854))")
        mpoly1 = MultiPolygon(fromstr(str(p1)))
        polygon1 = MapPolygon(lat='50', lon='22', field1=1.0, field2=2.0, mpoly=mpoly1, dataset=ds, remote_id=10)
        polygon1.save()
        mpoly2 = MultiPolygon(fromstr(str(p2)))
        polygon2 = MapPolygon(lat='12', lon='17', field1=1.0, field2=2.0, mpoly=mpoly2, dataset=ds, remote_id=9)
        polygon2.save()
        mpoly3 = MultiPolygon(fromstr(str(p3)))
        polygon3 = MapPolygon(lat='23', lon='27', field1=1.0, field2=2.0, mpoly=mpoly3, dataset=ds, remote_id=9)
        polygon3.save()


        self.request = HttpRequest()
        qdict = QueryDict('', mutable=True)
        qdict.update({'year': '2010'})
        qdict.update({'year': '2014'})
        qdict.update({'year': '2016'})
        qdict.update({'unit': 'km'})
        self.request.GET = qdict
        self.serializer = AnalyzeAreaSerializer(context={'request': self.request})

    def test_can_get_areaAroundPoint(self):
        data = self.serializer.get_areaAroundPoint(self.mp)
        self.assertEqual(data['point id(s)'], '2')
        self.assertTrue(data.get('1.000000 km'))
        self.assertTrue(data.get('3.000000 km'))
        self.assertTrue(data.get('5.000000 km'))

    def test_can_get_areaAroundPoint2(self):
        data = self.serializer.get_areaAroundPoint2(self.mp)
        self.assertTrue(data.get('1.000000 km'))
        self.assertTrue(data.get('3.000000 km'))
        self.assertTrue(data.get('5.000000 km'))


class TestAnalyzeAreaNoValuesSerializer(TestCase):
    fixtures = ['test_data.json']

    def setUp(self):
        ds = Dataset.objects.get(pk=3)
        self.mp = MapPoint.objects.get(pk=1)
        setattr(self.mp, 'dataset', ds)
        self.mp.point = Point(5, 23)
        MapPoint(lat=23.41, lon=98.0, dataset=ds, point=Point(5, 23), state='NY', city='NYC').save()
        tag1 = Tag(dataset=ds, tag='tag1', approved=True, count=1)
        tag1.save()
        tag2 = Tag(dataset=ds, tag='tag2', approved=True, count=1)
        tag2.save()
        tagindiv1 = TagIndiv(tag=tag1, mapelement=self.mp)
        tagindiv1.save()
        tagindiv2 = TagIndiv(tag=tag2, mapelement=self.mp)
        tagindiv2.save()
        p1 = GEOSGeometry("SRID=4326;POLYGON ((5 23.00902982868961, 5.004877257506506 23.00781998654152, 5.00844745207902 23.00451469036915, 5.009753953024734 22.99999969967893, 5.008446890194161 22.99548485657674, 5.004876695621637 22.99217985558042, 5 22.99097016102037, 4.995123304378363 22.99217985558042, 4.991553109805839 22.99548485657674, 4.990246046975266 22.99999969967893, 4.99155254792098 23.00451469036915, 4.995122742493493 23.00781998654153, 5 23.00902982868961))")
        p2 = GEOSGeometry("SRID=4326;POLYGON ((5 23.02708945518625, 5.014633459242311 23.02345948568706, 5.025344042308789 23.01354271143227, 5.029261858728946 22.99999729711045, 5.025338985345226 22.98645321108062, 5.014628402277986 22.97653909341024, 5 22.97291045220348, 4.985371597722013 22.97653909341024, 4.974661014654773 22.98645321108062, 4.970738141271054 22.99999729711045, 4.974655957691211 23.01354271143227, 4.985366540757689 23.02345948568706, 5 23.02708945518625))")
        p3 = GEOSGeometry("SRID=4326;POLYGON ((5 23.0451490404854, 5.024391911722986 23.03909835241012, 5.042242881329157 23.02256891874033, 5.048769763397385 22.99999249197385, 5.042228834209113 22.97741975490609, 5.024377864597061 22.96089770063709, 5 22.95485070226389, 4.975622135402939 22.96089770063709, 4.957771165790887 22.97741975490609, 4.951230236602615 22.99999249197385, 4.957757118670842 23.02256891874033, 4.975608088277014 23.03909835241012, 5 23.0451490404854))")
        mpoly1 = MultiPolygon(fromstr(str(p1)))
        polygon1 = MapPolygon(lat='50', lon='22', field1=1.0, field2=2.0, mpoly=mpoly1, dataset=ds, remote_id=10)
        polygon1.save()
        mpoly2 = MultiPolygon(fromstr(str(p2)))
        polygon2 = MapPolygon(lat='12', lon='17', field1=1.0, field2=2.0, mpoly=mpoly2, dataset=ds, remote_id=9)
        polygon2.save()
        mpoly3 = MultiPolygon(fromstr(str(p3)))
        polygon3 = MapPolygon(lat='23', lon='27', field1=1.0, field2=2.0, mpoly=mpoly3, dataset=ds, remote_id=9)
        polygon3.save()

        self.request = HttpRequest()
        qdict = QueryDict('', mutable=True)
        qdict.update({'year': '2014'})
        qdict.update({'year': '2016'})
        qdict.update({'unit': 'km'})
        self.request.GET = qdict
        self.serializer = AnalyzeAreaNoValuesSerializer(context={'request': self.request})

    def test_can_get_areaAroundPoint(self):
        data = self.serializer.get_areaAroundPoint(self.mp)
        self.assertEqual(data['1.000000 km'], {'land_area': 1, 'polygons': {u'10': 1.0}})
        self.assertEqual(data['points'][0]['state'], 'NY')
        self.assertEqual(data['points'][0]['city'], 'NYC')


class TestSensorSerializer(TestCase):
    fixtures = ['test_data.json']

    def test_can_create_sensor_model(self):
        request = RequestFactory().get('/?data=all')
        self.user = User.objects.get(username='test')
        request.user = self.user

        attrs = {'name': 'sensor2', 'supplier': 'sss', 'model_number': 123, 'metric': 'm', 'accuracy': 0.001}
        serializer = SensorSerializer(context={'request': request})
        sensor = serializer.create(attrs)
        self.assertEqual(sensor.name, 'sensor2')
        self.assertEqual(sensor.accuracy, 0.001)
        self.assertEqual(sensor.model_number, 123)


class TestDataPointSerializer(TestCase):

    def test_can_create_datapoint_model(self):

        serializer = DataPointSerializer()
        attrs = {'value': 212}
        point = serializer.create(attrs)
        self.assertEqual(point.value, 212)


class TestNewTagSerializer(TestCase):
    fixtures = ['test_data.json']

    def test_can_create_serializer(self):
        ds = Dataset.objects.get(pk=2)
        me = MapElement(name="abc", dataset=ds)
        me.save()
        tag1 = Tag(dataset=ds, tag='test', approved=True)
        tag1.save()
        tag2 = Tag(dataset=ds, tag='test', approved=True)
        tag2.save()
        serializer = NewTagSerializer()
        validated_data = {'mapelement_id': me.id, 'tag': 'test'}
        tagindiv = serializer.create(validated_data)
        self.assertTrue(isinstance(tagindiv, TagIndiv))
        self.assertEqual(tagindiv.tag, tag1)
        self.assertEqual(tagindiv.mapelement, me)
        self.assertEqual(serializer.validate_tag(' test '), 'test')
