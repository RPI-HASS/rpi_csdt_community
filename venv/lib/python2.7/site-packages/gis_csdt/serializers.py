from gis_csdt.models import Dataset, MapElement, MapPoint, Tag, TagIndiv, MapPolygon, DataField, DataElement, Sensor, DataPoint
from gis_csdt.filter_tools import filter_request, neighboring_points, unite_radius_bubbles
from gis_csdt.settings import CENSUS_API_KEY
from rest_framework import serializers
from rest_framework_gis import serializers as gis_serializers
from django.contrib.gis.measure import Distance
from django.contrib.gis.geos import GEOSGeometry
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django import VERSION as DJANGO_VERSION
import copy
import json
import urllib

CIRCLE_EDGES = 12  # number of edges on polygon estimation of a circle
if DJANGO_VERSION[0] >= 1 and DJANGO_VERSION[1] >= 7:
    def get_function(function_name):
        if function_name[:4] == 'get_':
            return
else:
    def get_function(function_name):
        return function_name

'''class TagSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(TagSerializer, self).__init__(many=many, *args, **kwargs)

    class Meta:
        model = TagIndiv
        fields = ('mappoint','mappolygon','tag')'''

'''class MapElementIdField(serializers.WritableField):
    def __init__(self, *args,**kwargs):
        self.field = kwargs.pop('field')
        super(MapElementIdField, self).__init__(*args, **kwargs)
    def to_native(self, obj):
        try:
            r = getattr(obj,self.field)
            return r.id
        except ObjectDoesNotExist:
            return None
    def from_native(self, data):
        try:
            return MapElement.objects.get(id=int(data))
        except (ObjectDoesNotExist, ValueError):
            return None'''


class NewTagSerializer(serializers.ModelSerializer):
    # mappolygon = MapElementIdField(required=False,
    #                                source='mapelement_id',
    #                                field='mappolygon')
    mapelement = serializers.IntegerField(source='mapelement_id')
    tag = serializers.CharField()

    class Meta:
        model = TagIndiv
        fields = ('mapelement', 'tag')

    def validate_tag(self, value):
        if ',' in value or type(value) is list:
            raise serializers.ValidationError('No more than one tag should '
                                              'be POSTed at once. Commas '
                                              'are not allowed in tags.')
        return value.strip().lower()

    def create(self, validated_data):
        me = validated_data.pop('mapelement_id')
        try:
            me = MapElement.objects.get(id=me)
        except Exception:
            raise serializers.ValidationError('No MapElement found with ID',
                                              str(me))
        tag_txt = validated_data.pop('tag')
        tags = Tag.objects.filter(dataset=me.dataset, tag=tag_txt)

        len_tags = len(tags)
        if len_tags == 0:
            tag = Tag(dataset=me.dataset, tag=tag_txt)
            tag.save()
        elif len_tags == 1:
            tag = tags[0]
        else:
            approved_tags = tags.filter(approved=True)
            if len(approved_tags) > 0:
                tag = approved_tags[0]
            else:
                tag = tags[0]
        return TagIndiv.objects.create(mapelement=me, tag=tag)


class TagCountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Tag
        fields = ['dataset', 'tag', 'count']


class DatasetSerializer(serializers.ModelSerializer):
    tags = serializers.SerializerMethodField(get_function('get_tags'))
    count = serializers.SerializerMethodField(get_function('get_count'))

    def get_tags(self, dataset):
        # build nested distinct list
        return Tag.objects.filter(approved=True, dataset=dataset) \
               .order_by('-count').values_list('tag', flat=True)

    def get_count(self, dataset):
        # build nested distinct list
        return MapElement.objects.filter(dataset=dataset).count()

    class Meta:
        model = Dataset
        fields = ('id', 'name', 'cached', 'count', 'tags', 'name_field')


class LocationSerializer(serializers.ModelSerializer):
    street = serializers.CharField(source='location.street')
    city = serializers.CharField(source='location.city')
    state = serializers.CharField(source='location.state')
    zipcode = serializers.CharField(source='location.zipcode')
    county = serializers.CharField(source='location.county')


class GeoCoordinatesSerializer(serializers.ModelSerializer):
    latitude = serializers.DecimalField(source='geocoor.lat', max_digits=18,
                                        decimal_places=15)
    longitude = serializers.DecimalField(source='geocoor.lon', max_digits=18,
                                         decimal_places=15)


class DatasetNameFieldSerializer(serializers.ModelSerializer):
    field1_en = serializers.CharField(source='ds_names.field1_en')
    field2_en = serializers.CharField(source='ds_names.field2_en')
    field3_en = serializers.CharField(source='ds_names.field3_en')
    field1_name = serializers.CharField(source='ds_names.field1_name')
    field2_name = serializers.CharField(source='ds_names.field2_name')
    field3_name = serializers.CharField(source='ds_names.field3_name')


class MapPointSerializer(serializers.HyperlinkedModelSerializer):
    latitude = serializers.DecimalField(source='mappoint.lat', max_digits=18,
                                        decimal_places=15)
    longitude = serializers.DecimalField(source='mappoint.lon', max_digits=18,
                                         decimal_places=15)
    street = serializers.CharField(source='mappoint.street')
    city = serializers.CharField(source='mappoint.city')
    state = serializers.CharField(source='mappoint.state')
    zipcode = serializers.CharField(source='mappoint.zipcode')
    county = serializers.CharField(source='mappoint.county')
    field1 = serializers.CharField(source='mappoint.field1')
    field2 = serializers.CharField(source='mappoint.field2')
    field3 = serializers.CharField(source='mappoint.field3')

    tags = serializers.SerializerMethodField(get_function('get_tags'))

    def get_tags(self, mappoint):
        # build nested distinct list
        return Tag.objects.filter(approved=True,
                                  tagindiv__mapelement=mappoint) \
                          .distinct('id', 'tag') \
                          .values_list('tag', flat=True)

    class Meta:
        # id_field = False
        # geo_field = 'point'
        model = MapPoint
        fields = ('dataset', 'id', 'name', 'latitude', 'longitude', 'street',
                  'city', 'state', 'zipcode', 'county', 'field1',
                  'field2', 'field3', 'tags')


class TestSerializer(gis_serializers.GeoFeatureModelSerializer):
    address = serializers.SerializerMethodField(get_function('get_address'))
    data = serializers.SerializerMethodField(get_function('get_data'))
    tags = serializers.SerializerMethodField(get_function('get_tags'))
    geom = serializers.SerializerMethodField(get_function('get_geom'))

    def get_address(self, mapelement):
        if hasattr(mapelement, 'mappoint'):
            return {'street': mapelement.mappoint.street,
                    'city': mapelement.mappoint.city,
                    'state': mapelement.mappoint.state,
                    'zipcode': mapelement.mappoint.zipcode,
                    'county': mapelement.mappoint.county}
        return {}

    def get_data(self, mapelement):
        data = {}
        child = mapelement.mappoint if hasattr(mapelement, 'mappoint') else mapelement.mappolygon
        dataset = Dataset.objects.get(id=mapelement.dataset_id)
        dataelements = DataElement.objects.filter(mapelement_id=mapelement.id)
        if dataset.names is not None:
            if dataset.names.field1_name != '' and (child.field1 != '' or child.field1 is not None):
                data[dataset.names.field1_en] = child.field1
            if dataset.names.field2_name != '' and (child.field2 != '' or child.field2 is not None):
                data[dataset.names.field2_en] = child.field2
            if hasattr(mapelement, 'mappoint') and dataset.names.field3_name != '' and (child.field3 != '' or child.field3 is not None):
                data[dataset.names.field3_en] = child.field3

        params = self.context.get('request', None).query_params
        if 'data' in params and params['data'] == 'all':
            for de in dataelements:
                for ft, field_name in {DataField.INTEGER: 'int_data', DataField.FLOAT: 'float_data', DataField.STRING: 'char_data'}.iteritems():
                    if de.datafield.field_type == ft:
                        data[de.datafield.field_en] = getattr(de, field_name)

        return data

    def get_tags(self, mapelement):
        # build nested distinct list
        return Tag.objects.filter(approved=True,
                                  tagindiv__mapelement=mapelement) \
               .distinct('tag').values_list('tag', flat=True)

    def get_geom(self, mapelement):
        if hasattr(mapelement, 'mappolygon'):
            return json.loads(GEOSGeometry(mapelement.mappolygon.mpoly).geojson)
        return json.loads(GEOSGeometry(mapelement.point).geojson)

    class Meta:
        id_field = 'id'
        geo_field = 'geom'
        model = MapElement
        fields = ('dataset', 'id', 'name', 'address', 'data', 'tags')


class MapPolygonSerializer(gis_serializers.GeoFeatureModelSerializer):
    latitude = serializers.DecimalField(source='mappolygon.lat',
                                        max_digits=18,
                                        decimal_places=15)
    longitude = serializers.DecimalField(source='mappolygon.lon',
                                         max_digits=18,
                                         decimal_places=15)
    field1 = serializers.CharField(source='mappolygon.field1')
    field2 = serializers.CharField(source='mappolygon.field2')

    mpoly = gis_serializers.GeometryField(source='mappolygon.mpoly')

    tags = serializers.SerializerMethodField(get_function('get_tags'))

    def get_tags(self, mappolygon):
        # build nested distinct list
        return Tag.objects.filter(approved=True,
                                  tagindiv__mapelement=mappolygon) \
               .distinct('id', 'tag').values_list('tag', flat=True)

    class Meta:
        id_field = False
        geo_field = 'mpoly'
        model = MapPolygon
        fields = ('id', 'dataset', 'remote_id', 'name',
                  'latitude', 'longitude', 'field1', 'field2', 'tags')


class CountPointsSerializer(serializers.ModelSerializer):
    polygon_id = serializers.IntegerField(source='remote_id')
    count = serializers.SerializerMethodField(get_function('get_count'))

    class Meta:
        model = MapPolygon
        fields = ('polygon_id', 'count')

    def get_count(self, mappolygon):
        request = self.context.get('request', None)
        params = copy.deepcopy(request.query_params)
        for key in ['max_lat', 'min_lat', 'max_lon', 'min_lon', 'state']:
            try:
                del params[key]
            except Exception:
                pass  # no big deal

        c = {mappolygon.dataset.names.field1_en: mappolygon.mappolygon.field1,
             mappolygon.dataset.names.field2_en: mappolygon.mappolygon.field2}

        datafields = DataField.objects.filter(dataset=mappolygon.dataset)
        # get other data
        for df in datafields:
            data = None
            if df.field_type == DataField.INTEGER:
                element = DataElement.objects.filter(datafield=df) \
                                             .filter(mapelement=mappolygon)
                if element:
                    data = element[0].int_data
            elif df.field_type == DataField.FLOAT:
                element = DataElement.objects.filter(datafield=df) \
                                             .filter(mapelement=mappolygon)
                if element:
                    data = element[0].float_data
            else:
                element = DataElement.objects.filter(datafield=df) \
                                             .filter(mapelement=mappolygon)
                if element:
                    data = element[0].char_data
            if data:
                c[df.field_en] = data

        points = filter_request(params, 'mappoint').filter(point__intersects=mappolygon.mappolygon.mpoly)
        all_tags = None
        if 'tag' in params:
            all_tags = params['tag']
        elif 'tags' in params:
            all_tags = params['tags']
        if all_tags:
            tags = all_tags.split(',')
            if type(tags) is not list:
                tags = [tags]
            all_tags = all_tags.replace(',', ', ')
        else:
            tags = []

        # counts in polygons
        if 'match' not in params or params['match'] != 'all':
            all_tag_filter = points
            for tag in tags:
                try:
                    num = int(tag)
                    tag_obj = Tag.objects.get(num)
                    all_tag_filter = all_tag_filter.filter(tagindiv__tag=tag_obj)
                    c[tag_obj.tag + " count"] = points.filter(tagindiv__tag=tag_obj).count()
                except Exception:
                    all_tag_filter = all_tag_filter.filter(tagindiv__tag__tag=tag)
                    c[tag + " count"] = points.filter(tagindiv__tag__tag=tag).count()
            if len(tags) > 1:
                c[all_tags + " count (match any)"] = points.count()
                c[all_tags + " count (match all)"] = points.count()
        if len(tags) > 1:
            c[all_tags + " count (match all)"] = points.count()

        return c


class AnalyzeAreaSerializer(serializers.ModelSerializer):
    street = serializers.CharField(source='mappoint.street')
    city = serializers.CharField(source='mappoint.city')
    state = serializers.CharField(source='mappoint.state')
    zipcode = serializers.CharField(source='mappoint.zipcode')
    county = serializers.CharField(source='mappoint.county')
    field1 = serializers.CharField(source='mappoint.field1')
    field2 = serializers.CharField(source='mappoint.field2')
    field3 = serializers.CharField(source='mappoint.field3')

    tags = serializers.SerializerMethodField(get_function('get_tags'))
    areaAroundPoint = serializers.SerializerMethodField(get_function('get_areaAroundPoint'))

    class Meta:
        model = MapPoint
        fields = ('street', 'city', 'state', 'zipcode', 'county',
                  'field1', 'field2', 'field3', 'tags', 'areaAroundPoint')

    def get_tags(self, mappoint):
        # build nested distinct list
        return Tag.objects.filter(approved=True,
                                  tagindiv__mapelement=mappoint) \
               .distinct('tag').values('tag')

    def get_areaAroundPoint(self, mappoint):
        request = self.context.get('request', None)

        years = request.GET.getlist('year')
        datasets = Dataset.objects.filter(name__icontains='census')
        if len(years) > 0:
            d = Dataset.objects.none()
            for y in years:
                d = d | datasets.filter(name__contains=y.strip())
            datasets = d
        if len(datasets) == 0:
            return {}
        else:
            dataset_id = datasets[0].id

        # DISTANCES
        distances = request.GET.getlist('distance')
        unit = request.GET.getlist('unit')
        if len(unit) > 1:
            return HttpResponseBadRequest('No more than one unit may be specified.')
        elif len(unit) == 0:
            unit = 'mi'
        elif unit[0] in ['m', 'km', 'mi']:
            unit = unit[0]
        else:
            return HttpResponseBadRequest('Accepted units: m, km, mi')
        if len(distances) == 0:
            distances = [1, 3, 5]
            unit = 'km'
        else:
            distances.sort()

        dist_objs = []
        for dist in distances:
            kwargs = {unit: dist}
            dist_objs.append(Distance(**kwargs))

        all_points = neighboring_points(mappoint,
                                        MapPoint.objects
                                        .filter(dataset_id=mappoint.dataset_id),
                                        dist_objs[-1])

        data_sums = {'point id(s)': '', 'view url(s)': []}
        for p in all_points:
            data_sums['point id(s)'] = data_sums['point id(s)'] + ',' + str(p.id)
            data_sums['view url(s)'].append('/around-point/%d/' % (p.id))
        data_sums['view url(s)'] = str(data_sums['view url(s)'])
        data_sums['point id(s)'] = data_sums['point id(s)'].strip(',')
        already_accounted = set()
        boundary = unite_radius_bubbles(all_points, dist_objs)
        for dist in dist_objs:
            if unit == 'm':
                dist_str = '%f m' % (dist.m)
            elif unit == 'km':
                dist_str = '%f km' % (dist.km)
            elif unit == 'mi':
                dist_str = '%f mi' % (dist.mi)
            poly = set(MapPolygon.objects
                       .filter(dataset_id__exact=dataset_id)
                       .filter(mpoly__covers=boundary[dist])
                       .exclude(remote_id__in=already_accounted)
                       .values_list('remote_id', flat=True))
            maybe_polys = MapPolygon.objects.filter(dataset_id__exact=dataset_id) \
                                            .exclude(mpoly__covers=boundary[dist]) \
                                            .exclude(remote_id__in=already_accounted) \
                                            .filter(mpoly__intersects=boundary[dist])
            for polygon in maybe_polys:
                if polygon.mpoly.intersection(boundary[dist]).area > .5 * polygon.mpoly.area:
                    poly.add(polygon.remote_id)
            already_accounted = already_accounted | poly
            data_sums[dist_str] = {}
            data_sums[dist_str]['polygon count'] = len(poly)
            data_sums[dist_str]['land area (m2)'] = sum([int(i)
                                                        for i in MapPolygon.objects
                                                        .filter(dataset_id__exact=dataset_id,
                                                                remote_id__in=poly)
                                                        .values_list('field1', flat=True)])
            if data_sums[dist_str]['polygon count'] > 0:
                data_sums[dist_str]['polygons'] = str(list(poly))
                datafields = DataField.objects.filter(dataset_id__exact=dataset_id).exclude(field_type__exact=DataField.STRING)
                for field in datafields:
                    if field.field_longname not in data_sums[dist_str]:
                        data_sums[dist_str][field.field_longname] = {}
                    if field.field_type == DataField.INTEGER:
                        data = DataElement.objects \
                               .filter(datafield_id=field.id,
                                       mapelement__remote_id__in=poly) \
                               .aggregate(sum=Sum('int_data'),
                                          dsum=Sum('denominator__int_data'))
                        # print data['sum'], data['dsum']
                    elif field.field_type == DataField.FLOAT:
                        data = DataElement.objects \
                               .filter(datafield_id=field.id,
                                       mapelement__remote_id__in=poly) \
                               .aggregate(sum=Sum('float_data'),
                                          dsum=Sum('denominator__float_data'))
                    else:
                        continue
                    data_sums[dist_str][field.field_longname][field.field_en] = data['sum']
                    data_sums[dist_str][field.field_longname]['total'] = data['dsum']

        return data_sums

    def get_areaAroundPoint2(self, mappoint):
        request = self.context.get('request', None)

        years = request.GET.getlist('year')
        year = years[0]
        datasets = Dataset.objects.filter(name__icontains='census')
        if len(years) > 0:
            d = Dataset.objects.none()
            for y in years:
                d = d | datasets.filter(name__contains=y.strip())
            datasets = d
        if len(datasets) == 0:
            return {}
        else:
            dataset_id = datasets[0].id

        # DISTANCES
        distances = request.GET.getlist('distance')
        unit = request.GET.getlist('unit')
        if len(unit) > 1:
            return HttpResponseBadRequest(
                   'No more than one unit may be specified.')
        elif len(unit) == 0:
            unit = 'mi'
        elif unit[0] in ['m', 'km', 'mi']:
            unit = unit[0]
        else:
            return HttpResponseBadRequest('Accepted units: m, km, mi')
        if len(distances) == 0:
            distances = [1, 3, 5]
            unit = 'km'
        else:
            distances.sort()

        dist_objs = []
        for dist in distances:
            kwargs = {unit: dist}
            dist_objs.append(Distance(**kwargs))

        all_points = neighboring_points(mappoint,
                                        MapPoint.objects.filter(dataset=mappoint.dataset_id),
                                        dist_objs[-1])
        # print all_points

        # variables = ['Total Population','Area (km2)','Total (Race)', 'White Only', 'African American', 'Hispanic','Asian/Pacific Islander', 'Native American','Total (Poverty)','below 1.00', 'weighted mean of median household income','Mean Housing Value']
        # variables = {'B02001_001E':{},'B02001_002E':{},'B02009_001E':{},'B03001_001E':{},'B03001_003E':{},'B02011_001E':{}, 'B02012_001E':{},'B02010_001E':{},'B05010_001E':{},'B05010_002E':{},'B19061_001E':{},'B25105_001E':{},'B25077_001E':{},'B25077_001E':{}}
        variables = {'B00001_001E': {}, 'B02001_001E': {}, 'B02001_002E': {},
                     'B02001_003E': {}, 'B02001_004E': {}, 'B02001_005E': {},
                     'B02001_006E': {}, 'B02001_007E': {}, 'B02001_008E': {},
                     'B03001_001E': {}, 'B03001_003E': {}, 'C17002_001E': {},
                     'C17002_002E': {}, 'C17002_003E': {}}
        for v in variables:
            request = 'http://api.census.gov/data/2010/acs5/variables/%s.json?key=%s' \
                      % (v, CENSUS_API_KEY)
            try:
                data = json.loads(urllib.urlopen(request).read())
            except Exception as e:
                print 'variable info for %s failed to load: %s' % (v, request)
                print e
                continue
            variables[v] = data

        data_sums = {'point id(s)': '', 'view url(s)': []}
        for p in all_points:
            data_sums['point id(s)'] = data_sums['point id(s)'] + ',' + str(p.id)
            data_sums['view url(s)'].append('/around-point/%d/' % (p.id))
        data_sums['point id(s)'] = data_sums['point id(s)'].strip(',')
        already_accounted = set()

        boundary = unite_radius_bubbles(all_points, dist_objs)
        for dist in dist_objs:
            if unit == 'm':
                dist_str = '%f m' % (dist.m)
            elif unit == 'km':
                dist_str = '%f km' % (dist.km)
            elif unit == 'mi':
                dist_str = '%f mi' % (dist.mi)
            poly = set(MapPolygon.objects.filter(dataset_id__exact=dataset_id)
                       .filter(mpoly__covers=boundary[dist])
                       .exclude(remote_id__in=already_accounted)
                       .values_list('remote_id', flat=True))
            maybe_polys = MapPolygon.objects.filter(dataset_id__exact=dataset_id) \
                                            .exclude(mpoly__covers=boundary[dist]) \
                                            .exclude(remote_id__in=already_accounted) \
                                            .filter(mpoly__intersects=boundary[dist])
            for polygon in maybe_polys:
                if polygon.mpoly.intersection(boundary[dist]).area > .5 * polygon.mpoly.area:
                    poly.add(polygon.remote_id)
            already_accounted = already_accounted | poly
            data_sums[dist_str] = {}
            data_sums[dist_str]['polygon count'] = len(poly)
            data_sums[dist_str]['land area (m2)'] = sum([int(i) for i in
                                                         MapPolygon.objects
                                                         .filter(dataset_id__exact=dataset_id,
                                                                 remote_id__in=poly)
                                                         .values_list('field1', flat=True)])
            if data_sums[dist_str]['polygon count'] > 0:
                data_sums[dist_str]['polygons'] = str(list(poly))
                if year == '2010':
                    get = ''
                    for e in variables:
                        get = get + ',' + e
                    get = get.strip(',')
                    tracts = {}
                    for e in poly:
                        if e[:2] not in tracts:
                            tracts[e[:2]] = {}
                        if e[2:5] not in tracts[e[:2]]:
                            tracts[e[:2]][e[2:5]] = ''
                        tracts[e[:2]][e[2:5]] = tracts[e[:2]][e[2:5]] + ',' + e[-6:]
                    for state in tracts:
                        for county in tracts[state]:
                            request = 'http://api.census.gov/data/2010/acs5?key=%s&get=%s,NAME&for=tract:%s&in=state:%s,county:%s' \
                                      % (CENSUS_API_KEY, get, tracts[state][county].strip(','), state, county)
                            try:
                                url = urllib.urlopen(request).read()
                                data = json.loads(url)
                            except Exception as e:
                                print e
                                print url
                                print request
                                continue
                            line = data[0]
                            locations = {}
                            for i in range(len(line)):
                                locations[line[i]] = i
                                if line[i] not in data_sums[dist_str] and line[i] in variables:
                                    data_sums[dist_str][line[i]] = copy.deepcopy(variables[line[i]])
                                    data_sums[dist_str][line[i]]['sum'] = 0

                            for line in data[1:]:
                                # get area
                                for v in variables:
                                    try:
                                        data_sums[dist_str][v]['sum'] = data_sums[dist_str][v]['sum'] + int(line[locations[v]])
                                    except Exception:
                                        continue

        return data_sums


class DataPointSerializer(serializers.ModelSerializer):
    value = serializers.DecimalField(max_digits=30, decimal_places=15)
    time = serializers.DateTimeField()

    class Meta:
        model = DataPoint
        fields = ('value', 'time')

    def create(self, attrs, instance=None):
        datapointModel = DataPoint(value=attrs['value'])
        datapointModel.save()
        return datapointModel


class SensorSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100)
    supplier = serializers.CharField(max_length=100)
    model_number = serializers.CharField(max_length=100)
    metric = serializers.CharField(max_length=100)
    accuracy = serializers.CharField(max_length=100)
    datapoints = DataPointSerializer(many=True, read_only=True)
    mappoint = MapPointSerializer(read_only=True)

    class Meta:
        model = Sensor
        fields = ('name', 'supplier', 'model_number', 'metric', 'accuracy')
        read_only_fields = ('datapoints', 'mappoint')

    def create(self, attrs, instance=None):
        thisUser = self.context['request'].user
        sensorModel = Sensor(name=attrs['name'].strip(),
                             supplier=attrs['supplier'].strip(),
                             model_number=attrs['model_number'],
                             metric=attrs['metric'],
                             accuracy=attrs['accuracy'],
                             user=thisUser)
        sensorModel.save()
        if 'datapoints' in attrs:
            for dp in attrs['datapoints']:
                sensorModel.datapoints.add(DataPoint.objects.get(pk=dp))
                sensorModel.save()
        if 'mappoint' in attrs:
            sensorModel.mappoint = MapPoint.objects.get(pk=attrs['mappoint'])
            sensorModel.save()
        return sensorModel


class AnalyzeAreaNoValuesSerializer(serializers.ModelSerializer):
    point_id = serializers.CharField(source='mappoint.id')
    areaAroundPoint = serializers.SerializerMethodField(get_function('get_areaAroundPoint'))

    class Meta:
        model = MapPoint
        fields = ('point_id', 'areaAroundPoint')

    def get_tags(self, mappoint):
        # build nested distinct list
        return Tag.objects.filter(approved=True,
                                  tagindiv__mapelement=mappoint) \
               .distinct('tag').values('tag')

    def get_areaAroundPoint(self, mappoint):
        request = self.context.get('request', None)
        years = request.GET.getlist('year')
        datasets = Dataset.objects.filter(name__icontains='census')
        if len(years) > 0:
            d = Dataset.objects.none()
            for y in years:
                d = d | datasets.filter(name__contains=y.strip())
            datasets = d
        if len(datasets) == 0:
            return {}
        else:
            dataset_id = datasets[0].id

        # DISTANCES
        distances = request.GET.getlist('distance')
        unit = request.GET.getlist('unit')
        if len(unit) > 1:
            return HttpResponseBadRequest('No more than one unit may be specified.')
        elif len(unit) == 0:
            unit = 'mi'
        elif unit[0] in ['m', 'km', 'mi']:
            unit = unit[0]
        else:
            return HttpResponseBadRequest('Accepted units: m, km, mi')
        if len(distances) == 0:
            distances = [1, 3, 5]
            unit = 'km'
        else:
            distances.sort()

        # method is containment or apportionment?
        method = request.GET.getlist('method')
        if len(method) > 0 and method[0] == 'apportionment':
            apportionment = True
        else:
            apportionment = False

        dist_objs = []
        for dist in distances:
            kwargs = {unit: dist}
            dist_objs.append(Distance(**kwargs))

        all_points = neighboring_points(mappoint, MapPoint.objects
                                        .filter(dataset_id=mappoint.dataset_id),
                                        dist_objs[-1])
        # print len(all_points), all_points
        data_sums = {'points': [],
                     'view url': 'http://127.0.0.1:8000/around-point/%d/'
                     % (all_points[0].id)}
        for p in all_points:
            data_sums['points'].append({'id': p.id,
                                        'name': p.name,
                                        'street': p.mappoint.street,
                                        'city': p.mappoint.city,
                                        'state': p.mappoint.state,
                                        'zipcode': p.mappoint.zipcode,
                                        'county': p.mappoint.county,
                                        'field1': p.mappoint.field1,
                                        'field2': p.mappoint.field2,
                                        'field3': p.mappoint.field3,
                                        'tags': Tag.objects.filter(approved=True, tagindiv__mapelement=mappoint).distinct('tag').values('tag')})
        already_accounted = set()
        boundary = unite_radius_bubbles(all_points, dist_objs)
        for dist in dist_objs:
            if unit == 'm':
                dist_str = '%f m' % (dist.m)
            elif unit == 'km':
                dist_str = '%f km' % (dist.km)
            elif unit == 'mi':
                dist_str = '%f mi' % (dist.mi)
            temp_qs = MapPolygon.objects.filter(dataset_id__exact=dataset_id) \
                                        .filter(mpoly__coveredby=boundary[dist]) \
                                        .exclude(remote_id__in=already_accounted) \
                                        .distinct()
            poly = {x: 1. for x in temp_qs.values_list('remote_id', flat=True)}
            try:
                land_area = sum([int(x) for x in temp_qs.values_list('field1', flat=True)])
            except Exception:
                continue
            # print 'poly', poly
            maybe_polys = MapPolygon.objects.filter(dataset_id__exact=dataset_id) \
                                            .exclude(remote_id__in=poly) \
                                            .exclude(remote_id__in=already_accounted) \
                                            .filter(mpoly__intersects=boundary[dist]) \
                                            .distinct()
            # print 'maybes', maybe_polys.values_list('remote_id',flat=True)
            for polygon in maybe_polys:
                intersection_area = polygon.mpoly.intersection(
                                    boundary[dist]).area / polygon.mpoly.area
                if apportionment or intersection_area > .5:
                    poly[polygon.remote_id] = intersection_area \
                                              if apportionment else 1.
                    try:
                        land_area += intersection_area*int(polygon.field1) \
                                     if apportionment else int(polygon.field1)
                    except Exception:
                        continue

            already_accounted = already_accounted | set(poly.keys())
            data_sums[dist_str] = {}
            # data_sums[dist_str]['polygon count'] = len(poly)
            # data_sums[dist_str]['land area (m2)'] = sum([int(i)
            #                                              for i in MapPolygon.objects
            #                                              .filter(dataset_id__exact=dataset_id
            #                                                      ,remote_id__in=poly)
            #                                              .values_list('field1',flat=True)])
            if len(poly) > 0:
                data_sums[dist_str]['polygons'] = poly
                data_sums[dist_str]['land_area'] = land_area
        return data_sums
