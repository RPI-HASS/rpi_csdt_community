from django.contrib.gis.db import models
from datetime import datetime
from django.utils.timezone import utc
from django.conf import settings
from django.contrib.auth import get_user_model

import decimal
import json
import urllib


# Field classes for Dataset
class Location(models.Model):
    street_field = models.CharField(max_length=50, default='street',
                                    blank=True)
    city_field = models.CharField(max_length=50, default='city', blank=True)
    state_field = models.CharField(max_length=50, default='state', blank=True)
    zipcode_field = models.CharField(max_length=50, default='zip', blank=True)
    county_field = models.CharField(max_length=50, default='county',
                                    blank=True)

    def __unicode__(self):
        return self.street_field + ", " + self.county_field + ", " \
               + self.city_field + " " + self.state_field \
               + '\n' + self.zipcode_field


class GeoCoordinates(models.Model):
    lat_field = models.CharField(max_length=50, default='latitude', blank=True)
    lon_field = models.CharField(max_length=50, default='longitude',
                                 blank=True)

    def __unicode__(self):
        return "latitude: " + self.lat_field + ", longitude: " + self.lon_field


class DatasetNameField(models.Model):
    field1_en = models.CharField(blank=True, max_length=150)
    field1_name = models.CharField(blank=True, max_length=50)
    field2_en = models.CharField(blank=True, max_length=150)
    field2_name = models.CharField(blank=True, max_length=50)
    field3_en = models.CharField(blank=True, max_length=150)
    field3_name = models.CharField(blank=True, max_length=50)

    def __unicode__(self):
        return self.field1_name + ", " + self.field1_en + ";\n" \
               + self.field2_name + ", " + self.field2_en + ";\n" \
               + self.field3_name + ", " + self.field3_en + ";"


BATCH_SIZE = 5000


class Dataset(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField(blank=True, max_length=300)
    cached = models.DateTimeField(null=True, blank=True)
    cache_max_age = models.IntegerField('age when cache should be replaced in days',
                                        default=1)
    # field names
    remote_id_field = models.CharField('column name of key field on the remote server',
                                       blank=True, max_length=50, default='id')
    name_field = models.CharField(max_length=50, default='name')
    needs_geocoding = models.BooleanField(default=False)

    location = models.ForeignKey(Location, blank=True, null=True)
    coordinates = models.ForeignKey(GeoCoordinates, blank=True, null=True)
    names = models.ForeignKey(DatasetNameField, blank=True, null=True)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.name

    # recurses through structure of fields and the json
    # , = level
    # + = concatenation of 2 or more fields.
    def reach_field(self, json_item, location):
        result = ''
        if len(location) > 1:
            for field in location[0]:
                if field in json_item:
                    result += self.reach_field(json_item[field],
                                               location[1:]) + ' '
        elif len(location) == 1:
            for field in location[0]:
                if field in json_item:
                    result += json_item[field].strip() + ' '
        return result.strip()

    '''
    def update_mappoints(self):
        if self.url == '': #this can only be done through manual updates
            return
        if self.should_update():
            self.loop_thru_cache()
        elif self.needs_geocoding:
            for point in MapPoint.objects.filter(dataset_id = self.pk).order_by('remote_id'):
                if not point.geocoded:
                    r = point.geocode()
                    if r['status'] == 'OVER_QUERY_LIMIT':
                        return # ENDS FUNCTION
                    point.save()
            self.needs_geocoding = False
            self.save()

    def loop_thru_cache(self):
        added = 0
        geocoded = 0

        points = MapPoint.objects.filter(dataset_id = self.pk).order_by('remote_id')
        if self.remote_id_field == '':
            plus = ''
        else:
            plus = '?$order=' + self.remote_id_field
        json_in = json.loads(urllib.urlopen(self.url + plus).read())
        if plus == '':
            plus = '?'
        else:
            plus += '&'
        #if json_in['error']:

        #dictionary to hold structure of data in remote dataset
        fields = {}
        fields['remote_id'] = [x.split('+')
                               for x in self.remote_id_field.split(',')]
        fields['name'] = [x.split('+') for x in self.name_field.split(',')]
        fields['lat'] = [x.split('+') for x in self.lat_field.split(',')]
        fields['lon'] = [x.split('+') for x in self.lon_field.split(',')]
        fields['street'] = [x.split('+') for x in self.street_field.split(',')]
        fields['city'] = [x.split('+') for x in self.city_field.split(',')]
        fields['state'] = [x.split('+') for x in self.state_field.split(',')]
        fields['zipcode'] = [x.split('+')
                             for x in self.zipcode_field.split(',')]
        fields['county'] = [x.split('+') for x in self.county_field.split(',')]
        fields['field1'] = [x.split('+') for x in self.field1_name.split(',')]
        fields['field2'] = [x.split('+') for x in self.field2_name.split(',')]
        fields['field3'] = [x.split('+') for x in self.field3_name.split(',')]

        # if there's no remote id,
        # there's no easy way to compare cached with current
        # so just chuck it all and start again
        # if self.remote_id_field == '':
        #	points.delete()
        # err....what about the tags?

        try_geocoding = self.needs_geocoding
        rec_read = len(json_in)
        i = 0
        while len(json_in) > 0:
            for item in json_in:
                if i < len(points) and self.remote_id_field != '':
                    if points[i].remote_id == str(item[self.remote_id_field]):
                        if try_geocoding and not points[i].geocoded:
                            r = points[i].geocode()
                            if r['status'] == 'OVER_QUERY_LIMIT':
                                try_geocoding = False
                                print '--%d geocoded--' %(geocoded)
                            else:
                                geocoded += 1
                        i += 1
                        continue
                    elif points[i].remote_id < str(item[self.remote_id_field]):
                        print points[i].remote_id,
                              str(item[self.remote_id_field])
                        try:
                            print 'Deleting point:', points[i],
                            points[i].delete()
                        except Exception as e:
                            print '...failed to delete point %s:%s' \
                                  %(points[i],e)
                            # not a huge deal if it fails
                            i += 1
                            continue
                        print '...deleted'
                        continue
                new_point = MapPoint(dataset = self, lat=0,lon=0)
                for field in fields:
                    temp = self.reach_field(item, fields[field]).strip()
                    if field in ['lat','lon']:
                        l = len(temp)
                        if l > 18 and temp[0] == '-':
                            temp = temp[:18]
                        elif l > 17:
                            temp = temp[:17]
                        try:
                            temp = decimal.Decimal(temp)
                        except:
                            print 'invalid decimal: %s' %(temp)
                            continue
                    elif len(temp) > MapPoint._meta.get_field(field).max_length:
                        temp = temp[0:MapPoint._meta.get_field(field).max_length]
                    setattr(new_point, field, temp)
                if try_geocoding:
                    r = new_point.geocode()
                    if r['status'] == 'OVER_QUERY_LIMIT':
                        try_geocoding = False
                    else:
                        geocoded += 1
                new_point.save()
                try:
                    new_point.point = Point(float(new_point.lon),
                                            float(new_point.lat))
                    new_point.save()
                except:
                    pass
                added += 1
                if added >= BATCH_SIZE:
                    if try_geocoding:
                        print '--%d added, %d geocoded--' %(added, geocoded)
                    else:
                        print '--%d added--' %(added)
                    return
            json_in = json.loads(urllib.urlopen(self.url + plus
                                 + '$offset=' + str(rec_read)).read())
            rec_read += len(json_in)

        self.cached = datetime.utcnow().replace(tzinfo=utc)
        if try_geocoding: #if still able to geocode, must have completed set
            self.needs_geocoding = False
        print '--%d added, %d geocoded--' %(added,geocoded)
        self.save()
    '''

    def should_update(self):
        if self.cached is None or self.cached == '':
            return True
        since = datetime.utcnow().replace(tzinfo=utc) - self.cached
        if since.days < self.cache_max_age or since.seconds < 60:
            return False
        return True


class MapElement(models.Model):
    dataset = models.ForeignKey(Dataset, blank=True, null=True)
    remote_id = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=150)
    point = models.PointField(srid=4326, blank=True, null=True)
    objects = models.GeoManager()

    def __unicode__(self):
        return self.name

    def polygon_id(self):
        try:
            self.mappolygon
            return self.id
        except Exception:
            return None

    def point_id(self):
        try:
            self.mappoint
            return self.id
        except Exception:
            return None

    # class Meta:
    # abstract = True


# class SensorReading(MapElement)
    # time = DateTimeField()
    # node = name?


class MapPoint(MapElement):
    lat = models.DecimalField(max_digits=18, decimal_places=15)
    lon = models.DecimalField(max_digits=18, decimal_places=15)
    field1 = models.CharField(blank=True, max_length=200)
    field2 = models.CharField(blank=True, max_length=200)
    field3 = models.CharField(blank=True, max_length=200)

    street = models.CharField(blank=True, max_length=200)
    city = models.CharField(blank=True, max_length=100)
    state = models.CharField(blank=True, max_length=2)
    zipcode = models.CharField(blank=True, max_length=5)
    county = models.CharField(blank=True, max_length=75)
    geocoded = models.BooleanField(blank=True, default=False)

    # must be included in children too
    objects = models.GeoManager()

    def geocode(self, unknown_count=0):
        key = settings.GOOGLE_API_KEY
        location = urllib.quote_plus(self.street + ', ' + self.city
                                     + ', ' + self.state + ', ' + self.zipcode)
        request = 'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s&sensor=false' % (location, key)
        # print request
        j = json.loads(urllib.urlopen(request).read())
        if j['status'] == 'OK':
            try:
                self.lat = decimal.Decimal(
                           j['results'][0]['geometry']['location']['lat'])
                self.lon = decimal.Decimal(
                           j['results'][0]['geometry']['location']['lng'])
                self.geocoded = True
            except Exception:
                return {'status': 'conversion_error', 'request': request}
        # this error type means the request can be retried
        elif j['status'] == 'UNKNOWN_ERROR' and unknown_count < 5:
            return self.geocode(unknown_count + 1)
        # want to debug other errors
        assert (j['status'] == 'OK'
                or j['status'] == 'OVER_QUERY_LIMIT'
                or j['status'] == 'ZERO_RESULTS')
        if j['status'] == 'OVER_QUERY_LIMIT':
            print 'Hit Google Maps API daily query limit'
        return {'status': j['status'], 'request': request}


class MapPolygon(MapElement):
    lat = models.CharField(max_length=17)
    lon = models.CharField(max_length=17)
    field1 = models.FloatField()
    field2 = models.FloatField()

    mpoly = models.MultiPolygonField(srid=4326)
    # must be included in children too
    objects = models.GeoManager()


class DataField(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='dataFields')
    field_en = models.CharField(blank=True, max_length=100)
    field_longname = models.CharField(blank=True, max_length=400)
    field_name = models.CharField(blank=True, max_length=50)

    INTEGER = 'I'
    FLOAT = 'F'
    STRING = 'C'
    type_choices = ((INTEGER, 'integer'),
                    (FLOAT, 'floating point'), (STRING, 'string'))
    field_type = models.CharField(max_length=1,
                                  choices=type_choices, default=STRING)

    def __unicode__(self):
        return self.field_en + ', id:' + str(self.id) + \
               ', dataset:' + str(self.dataset_id)


class DataElement(models.Model):
    datafield = models.ForeignKey(DataField, related_name='dataElements')
    mapelement = models.ForeignKey(MapElement)
    denominator = models.ForeignKey('self', null=True)
    error = models.FloatField(null=True)
    int_data = models.IntegerField(null=True)
    float_data = models.FloatField(null=True)
    char_data = models.CharField(blank=True, null=True, max_length=200)

    def __unicode__(self):
        return '[' + self.datafield.field_en + '] for [' + \
               self.mapelement.name + '], id:' + str(self.id) \
               + ', datafield:' + str(self.datafield_id)


class Tag(models.Model):
    dataset = models.ForeignKey(Dataset, related_name='tags')
    tag = models.CharField(max_length=100)
    approved = models.BooleanField(default=False)
    count = models.IntegerField(default=0)

    def __unicode__(self):
        return self.tag

    # not necessary, but would rather have the code centralized
    def increment_count(self, save=True):
        self.count += 1
        if save:
            self.save()

    def recount(self, save=True):
        self.count = TagIndiv.objects.filter(tag=self).filter(
                     mapelement__dataset_id=self.dataset_id).count()
        if save:
            self.save()


class TagIndiv(models.Model):
    tag = models.ForeignKey(Tag)
    mapelement = models.ForeignKey(MapElement)

    def __unicode__(self):
        return self.mapelement.name + ' tagged as "' + self.tag.tag + '"'

    class Meta:
        unique_together = (("tag", "mapelement"),)

    '''
    def save(self, *args, **kwargs):
        exists = self.id is not null
        if not exists:
            matches = TagIndiv.objects.filter(tag = self.tag,
                                              mappoint = self.mappoint,
                                              mappolygon = self.mappolygon)
        if exists or len(matches) == 0:
            super(TagIndiv, self).save(*args, **kwargs)
        elif self.approved and matches.filter(approved=True).count() == 0:
            matches[0].approved = True
            matches[0].save()
    '''


class DataPoint(models.Model):
    value = models.DecimalField(max_digits=30, decimal_places=15)
    time = models.DateTimeField(blank=True, null=True)
    # To add later to tie into django_team
    # team = models.ForeignKey(Team)

    def __unicode__(self):
        return "value: " + str(self.value) + " time: " + str(self.time)


class Sensor(models.Model):
    name = models.CharField(max_length=100, default='name', unique=True)
    supplier = models.CharField(max_length=100, default='supplier')
    model_number = models.CharField(max_length=100, default='model_number')
    metric = models.CharField(max_length=100, default='metric')
    accuracy = models.CharField(max_length=100, default='accuracy')
    user = models.ForeignKey(get_user_model(), blank=True, null=True)
    datapoints = models.ManyToManyField(DataPoint, blank=True)
    mappoint = models.ForeignKey(MapPoint, related_name='points', null=True)

    def __unicode__(self):
        return 'id: ' + str(self.name)


class PhoneNumber(models.Model):
    phone_number = models.BigIntegerField(null=False)
    user = models.ForeignKey(get_user_model(), null=False)
