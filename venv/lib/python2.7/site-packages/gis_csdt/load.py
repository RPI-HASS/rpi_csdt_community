# This file includes functions to load basic information
# should be used from the shell

import csv
import ftplib
import json
import os
import urllib
import zipfile
from django.contrib.gis.utils import LayerMapping
from models import MapPolygon, MapElement, MapPoint, GeoCoordinates, Location, DatasetNameField, Dataset, DataField, DataElement, Tag, TagIndiv
from datetime import datetime
from django.utils.timezone import utc
from django.conf import settings
from django.contrib.gis.geos import Point
from django.db import IntegrityError
from django.db.models import Max
from django.core.exceptions import ObjectDoesNotExist
from settings import DEBUG
import re
import string


def run(verbose=True, year=2010, starting_state=1):
    yn = ''
    # https://docs.djangoproject.com/en/1.7/ref/contrib/gis/layermapping/
    while DEBUG and yn != 'y':
        yn = raw_input('This process can be memory-intensive if'
                       'DEBUG = True in settings as this logs all SQL. '
                       'DEBUG is currently True. Please set this to False'
                       'if you are experiencing issues. Continue (y/n)?') \
                       .lower().strip()
        if yn == 'n':
            return
    dataset_qs = Dataset.objects.filter(name__exact=str(year)+' Census Tracts')
    if len(dataset_qs) > 0:
        ds = dataset_qs[0]
        ds.cached = datetime.utcnow().replace(tzinfo=utc),
    else:
        coor = GeoCoordinates(lat_field='INTPTLAT'+str(year)[-2:],
                              lon_field='INTPTLON'+str(year)[-2:])
        coor.save()
        names = DatasetNameField(field1_en='Land Area',
                                 field1_name='ALAND'+str(year)[-2:],
                                 field2_en='Water Area',
                                 field2_name='AWATER'+str(year)[-2:])
        names.save()
        ds = Dataset(name=str(year)+' Census Tracts',
                     cached=datetime.utcnow().replace(tzinfo=utc),
                     cache_max_age=1000,
                     name_field='NAMELSAD'+str(year)[-2:],
                     coordinates=coor,
                     names=names)
        if year == 2010:
            ds.remote_id_field = 'GEOID00'
        elif year == 2000:
            ds.remote_id_field = 'CTIDFP00'
        ds.save()

    tract_mapping = {
        'remote_id': ds.remote_id_field,
        'name': ds.name_field,
        'lat': ds.coordinates.lat_field,
        'lon': ds.coordinates.lon_field,
        'field1': ds.names.field1_name,
        'field2': ds.names.field2_name,
        'mpoly': 'MULTIPOLYGON',
    }

    ftp = ftplib.FTP('ftp2.census.gov')
    ftp.login()
    ftp.cwd("/geo/tiger/TIGER2010/TRACT/" + str(year) + "/")
    files = ftp.nlst()

    MapPolygon.objects.filter(dataset_id__isnull=True).delete()
    max_state = MapPolygon.objects.filter(dataset_id__exact=ds.id).aggregate(Max('remote_id'))
    max_state = max_state['remote_id__max']
    if max_state is not None:
        try:
            max_state = int(max_state)/1000000000
            if max_state >= starting_state:
                starting_state = max_state + 1
        except Exception:
            pass

    for i in [format(x, '#02d') for x in range(starting_state, 100)]:
        short_name = 'tl_2010_' + i + '_tract' + str(year)[-2:]
        tract_shp = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                    'data/'+short_name))
        if (not os.path.isfile(tract_shp+'.shp')
            or not os.path.isfile(tract_shp+'.shx')
            or not os.path.isfile(tract_shp+'.shp.xml')
            or not os.path.isfile(tract_shp+'.prj')
            or not os.path.isfile(tract_shp+'.dbf')):

            if short_name + '.zip' not in files:
                continue
            if verbose:
                print short_name + '.shp does not exist locally.\n\tDownloading from Census FTP...'
            try:
                # download the file
                local_file = open(tract_shp+'.zip', 'wb')
                ftp.retrbinary('RETR '+short_name+'.zip', local_file.write)
                local_file.close()
                # open the zip
                zipped = zipfile.ZipFile(tract_shp+'.zip')
                for suffix in ['.shp', '.prj', '.dbf', '.shp.xml', '.shx']:
                    zipped.extract(short_name+suffix, os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
            except Exception as inst:
                if verbose:
                    print '\tException:', inst
                    print '\t'+short_name + '.shp did not download or unzip correctly. Moving on...'
                continue
        tract_shp = tract_shp + '.shp'
        if verbose:
            print '\tBegin layer mapping...'
        lm = LayerMapping(MapPolygon, tract_shp, tract_mapping, transform=False, encoding='iso-8859-1')

        while True:
            try:
                lm.save(strict=True, verbose=False)  # verbose)
                break
            # exception part is untested, error didn't happen again
            except Exception as inst:
                yn = ''
                while yn not in ['n', 'y']:
                    yn = raw_input('Error saving: ' + str(inst) + '\nContinue (y/n)?').strip().lower()
                if yn == 'y':
                    MapPolygon.objects.filter(dataset_id__isnull=True).filter(remote_id__startswith=i).delete()
                else:
                    break
        if verbose:
            print '\tLayer mapping done.'
        MapPolygon.objects.filter(dataset=None).update(dataset=ds)
        if verbose:
            print '\tLayer associated with dataset.'
    ftp.quit()

    if verbose:
        print 'All shapefiles added.'


'''def temp_switch():
    for poly in MapPolygon.objects.all():
        lat = poly.field1
        lon = poly.field2
        poly.field1 = poly.lat
        poly.field2 = poly.lon
        poly.lat = lat
        poly.lon = lon
        poly.save()'''


def recount():
    all_tags = Tag.objects.all()
    for tag in all_tags:
        tag.recount(save=True)


def get_income(year=2010, ds_id=0, to_process=None):
    try:
        # check the format
        if to_process is None:
            raise
        for v in to_process:
            if 'variable' not in v or 'variable_type' not in v:
                raise
    except Exception:
        # http://www.census.gov/data/developers/data-sets/acs-survey-5-year-data.html
        # http://api.census.gov/data/2010/acs5/variables.html
        #              median household income                                     Total population
        to_process = [{'variable': 'B19013_001E', 'variable_type': DataField.INTEGER},
                      {'variable': 'B01003_001E', 'variable_type': DataField.INTEGER}]
        '''to_process = [{'variable':'B02001_001E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_002E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_003E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_004E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_005E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_006E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_007E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_008E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_009E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B02001_010E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B17001_001E', 'variable_type':DataField.INTEGER},
                                    {'variable':'B17001_002E', 'variable_type':DataField.INTEGER}
                                    ]'''
    key = settings.CENSUS_API_KEY

    ds = Dataset.objects.filter(name__icontains='census').filter(name__contains=str(year)).all()
    if len(ds) == 0:
        print 'No Census dataset exists. Aborting'
        return
    elif len(ds) > 1:
        if ds_id > 0:
            ds = [ds.get(pk=ds_id)]
        else:
            print 'More than one 2010 Census dataset exists. Using ID %d' % (ds[0].id)

    dfs = []
    get = ''
    for item in to_process:
        try:
            dfs.append(DataField.objects.filter(dataset_id__exact=ds[0].id).get(field_name=item['variable']))
        except Exception:
            request = 'http://api.census.gov/data/2010/acs5/variables/%s.json' % (item['variable'])
            data = json.loads(urllib.urlopen(request).read())
            dfs.append(DataField(dataset=ds[0], field_en=data['label'],
                       field_longname=data['concept'][7:].strip(),
                       field_name=item['variable'],
                       field_type=item['variable_type']))
            if len(dfs[-1].field_en) > DataField._meta.get_field('field_en').max_length:
                dfs[-1].field_en = dfs[-1].field_en[:DataField._meta.get_field('field_en').max_length]
            if len(dfs[-1].field_longname) > DataField._meta.get_field('field_longname').max_length:
                dfs[-1].field_longname = dfs[-1].field_longname[:DataField._meta.get_field('field_longname').max_length]
            dfs[-1].save()
        get = get + ',' + item['variable']
    get = get.strip(', ')

    counties = json.loads(urllib.urlopen('http://api.census.gov/data/2010/acs5?key='+key+'&get=NAME&for=county:*').read())
    # i could technically call this once, but it's just too much data at once so i'm splitting by state
    for county in counties[1:]:
        # get the data
        request = 'http://api.census.gov/data/2010/acs5?key=%s&get=%s,NAME&for=tract:*&in=state:%s,county:%s' % (key, get, county[1], county[2])
        try:
            data = json.loads(urllib.urlopen(request).read())
        except Exception:
            continue
        converted = {}
        # locations of basic data in each list
        # format like:
        # [["B19013_001E","B01003_001E","NAME","state","county","tract"],
        # ["32333","2308","Census Tract 1, Albany County, New York","36","001","000100"],
        # ...]
        for col in range(len(data[0])):
            if data[0][col] == 'NAME':
                n = col
            elif data[0][col] == 'state':
                s = col
            elif data[0][col] == 'county':
                c = col
            elif data[0][col] == 'tract':
                t = col
        for d in data[1:]:
            census_tract = d[s] + d[c] + d[t]
            converted[census_tract] = {}
            for num in range(n):
                if d[num] is not None:
                    converted[census_tract][data[0][num]] = d[num].strip()
        # converted now looks like
        # {"36001000100": {"B19013_001E": "32333","B01003_001E": "2308"},
        #  "36001000200": {"B19013_001E": "25354","B01003_001E": "5506"},...}
        for poly in MapPolygon.objects.filter(dataset=ds[0]).filter(remote_id__startswith=county[1]+county[2]):
            if poly.remote_id in converted:
                recursive_link = {}
                for df in dfs:
                    if df.field_name in converted[poly.remote_id]:
                        de = DataElement(datafield=df, mapelement=poly)
                        if df.field_type == DataField.INTEGER:
                            try:
                                de.int_data = int(converted[poly.remote_id][df.field_name])
                            except Exception:
                                print 'integer conversion failed for census tract %s, field %s' % (poly.remote_id, df.field_name)
                                print 'value:', converted[poly.remote_id][df.field_name]
                        elif df.field_type == DataField.FLOAT:
                            try:
                                de.float_data = float(converted[poly.remote_id][df.field_name])
                            except Exception:
                                print 'float conversion failed for census tract %s, field %s' % (poly.remote_id, df.field_name)
                        elif df.field_type == DataField.STRING:
                            if len(converted[poly.remote_id][df.field_name]) > 200:
                                print 'string overload - string truncated as shown:'
                                print '%s[%s]' % (converted[poly.remote_id][df.field_name][:200], 
                                                  converted[poly.remote_id][df.field_name][200:])
                                de.char_data = converted[poly.remote_id][df.field_name][:200]
                            else:
                                de.char_data = converted[poly.remote_id][df.field_name]
                        if df.field_name[-4:] == '001E':
                            de.save()
                            recursive_link[df.field_name[:-4]] = de
                        try:
                            de.denominator = recursive_link[df.field_name[:-4]]
                        except Exception:
                            pass
                        de.save()

            else:
                print 'ERROR: Tract #%s is not in the dataset' % (poly.remote_id)


def add_denominator():
    for df_denom in DataField.objects.filter(field_name__contains='_001E'):
        for df in DataField.objects.filter(field_name__contains=df_denom.field_name[:-4]).filter(dataset_id__exact=df_denom.dataset_id):
            for de in DataElement.objects.filter(datafield_id__exact=df.id).filter(denominator__isnull=True):
                try:
                    de.denominator = DataElement.objects.filter(datafield_id__exact=df_denom.id).get(mapelement_id=de.id)
                    de.save()
                except Exception:
                    continue


def del_all():
    DataField.objects.all().delete()


def tag_by_keyword(keyword='pizza', dataset=2, tag='pizza'):
    tag_helper([{'keyword': keyword}], 'keyword', dataset, tag)


def tag_by_name(filename='fastfood.json', name_field='Company', dataset=2, tag='fast food'):
    data = json.loads(open(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/'+filename))).read())
    data = data['data']
    tag_helper(data, name_field, dataset, tag)


def tag_helper(data, name_field, dataset, tag):
    mps = MapPoint.objects.filter(dataset_id=dataset)
    tags = Tag.objects.filter(dataset_id=dataset).filter(tag=tag)
    if tags.count() > 1:
        appr_tags = tags.filter(approved=True)
        if appr_tags.count() > 0:
            tags = appr_tags
        tag = tags[0]
    elif tags.count() == 0:
        tag = Tag(dataset_id=dataset, tag=tag, approved=True)
        tag.save()
    else:
        tag = tags[0]

    regex = re.compile('[%s]' % re.escape(string.punctuation))
    for item in data:
        name = regex.sub(r'[\'\'\.-]*', item[name_field])
        print name
        for mp in mps.filter(name__iregex=name):
            print mp.name
            t = TagIndiv(tag=tag, mapelement=mp)
            try:
                t.save()
            except IntegrityError:
                # violate unique restraint so just don't save it
                pass


def add_point_to_mp(dataset=None):
    mps = MapPoint.objects.filter(point__isnull=True).exclude(lat__isnull=True).exclude(lon__isnull=True)
    if dataset is not None:
        mps = mps.filter(dataset_id__exact=dataset)
    for mp in mps:
        try:
            mp.point = Point(float(mp.lon), float(mp.lat))
            mp.save()
        except Exception:
            pass


def hazardous_waste(year=2011, verbose=True):
    try:
        dataset = Dataset.objects.get(name="Hazardous Waste Sites "+str(year))
        dataset.cached = datetime.utcnow().replace(tzinfo=utc)
    except ObjectDoesNotExist:
        coor = GeoCoordinates(lat_field="Latitude",
                              lon_field="Longitude")
        coor.save()
        names = DatasetNameField(field1_en="Generator Status",
                                 field1_name="Generator Status",
                                 field2_en="Biennial Report Link",
                                 field2_name="Biennial Report Link")
        names.save()
        location = Location(street_field="Address",
                            city_field="City",
                            state_field="State",
                            zipcode_field="ZIP Code",
                            county_field="County")
        dataset = Dataset(
            name="Hazardous Waste Sites "+str(year),
            url='/data/ej/'+str(year)+'/',
            cached=datetime.utcnow().replace(tzinfo=utc),
            cache_max_age=1000,
            remote_id_field="Handler ID",
            name_field="Handler Name",
            location=location,
            coordinates=coor,
            names=names
            needs_geocoding=False)
    dataset.save()

    MapPoint.objects.filter(dataset=dataset).delete()

    for state in ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE',
                  'DC', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA',
                  'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN',
                  'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM',
                  'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI',
                  'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA',
                  'WV', 'WI', 'WY']:
        short_name = 'Envirofacts_Biennial_Report_Search ' + state + '.CSV'
        path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/ej/'+str(year)+'/'+short_name))
        if not os.path.isfile(path):
            if verbose:
                print 'No file %s exists.' % (short_name)
            short_name = str(year)+' '+state+'.CSV'
            path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/ej/'+str(year)+'/'+short_name))
            if not os.path.isfile(path):
                if verbose:
                    print 'No file %s exists.' % (short_name)
                continue
        if verbose:
            print 'Opening file %s' % (short_name)
        readfile = csv.reader(open(path, 'rb'))
        # verify
        row = readfile.next()
        locs = {}
        for i in range(len(row)):
            if row[i] == dataset.remote_id_field:
                locs['remote_id'] = i
            elif row[i] == dataset.name_field:
                locs['name'] = i
            elif row[i] == dataset.location.street_field:
                locs['street'] = i
            elif row[i] == dataset.location.city_field:
                locs['city'] = i
            elif row[i] == dataset.location.state_field:
                locs['state'] = i
            elif row[i] == dataset.location.zipcode_field:
                locs['zipcode'] = i
            elif row[i] == dataset.location.county_field:
                locs['county'] = i
            elif row[i] == dataset.coordinates.lat_field:
                locs['lat'] = i
            elif row[i] == dataset.coordinates.lon_field:
                locs['lon'] = i
            elif row[i] == dataset.names.field1_name:
                locs['field1'] = i
            elif row[i] == dataset.names.field2_name:
                locs['field2'] = i
        for row in readfile:
            kwargs = {'dataset': dataset}
            for key in locs:
                if key in ['lat', 'lon']:
                    try:
                        kwargs[key] = float(row[locs[key]])
                    except Exception:
                        kwargs[key] = 0.
                elif MapPoint._meta.get_field(key).max_length < len(row[locs[key]]):
                    kwargs[key] = row[locs[key]][:MapPoint._meta.get_field(key).max_length]
                else:
                    kwargs[key] = row[locs[key]]
            try:
                kwargs['point'] = Point(kwargs['lon'], kwargs['lat'])
            except Exception:
                if verbose:
                    print '\tInvalid lat/long for row: %s' % (row)
                    print '\tLat: %f Lon: %f' % (kwargs['lat'], kwargs['lon'])
                continue
            mp = MapPoint(**kwargs)
            mp.save()
        if verbose:
            print 'File "%s" done processing' % (short_name)


def load_from_se(year=2000):
    flds = {'SE_T001_001': 'T1. Total Population',
            # 'SE_T014_001':'Total Population',
            # 'SE_T014_002':'White Alone',
            # 'SE_T014_003':'Black or African American Alone',
            # 'SE_T014_004':'American Indian and Alaska Native Alone',
            # 'SE_T014_005':'Asian Alone',
            # 'SE_T014_006':'Native Hawaiian and Other Pacific Islander Alone',
            # 'SE_T014_007':'Some other race Alone',
            # 'SE_T014_008':'Two or more races',
            # 'SE_T015_001':'Total Population',
            # 'SE_T015_002':'Not Hispanic or Latino',
            # 'SE_T015_003':'Not Hispanic or Latino: White Alone',
            # 'SE_T015_004':'Not Hispanic or Latino: Black or African American Alone',
            # 'SE_T015_005':'Not Hispanic or Latino: American Indian and Alaska Native Alone',
            # 'SE_T015_006':'Not Hispanic or Latino: Asian Alone',
            # 'SE_T015_007':'Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander Alone',
            # 'SE_T015_008':'Not Hispanic or Latino: Some other race Alone',
            # 'SE_T015_009':'Not Hispanic or Latino: Two or more races',
            # 'SE_T015_010':'Hispanic or Latino',
            # 'SE_T015_011':'Hispanic or Latino: White Alone',
            # 'SE_T015_012':'Hispanic or Latino: Black or African American Alone',
            # 'SE_T015_013':'Hispanic or Latino: American Indian and Alaska Native Alone',
            # 'SE_T015_014':'Hispanic or Latino: Asian Alone',
            # 'SE_T015_015':'Hispanic or Latino: Native Hawaiian and Other Pacific Islander Alone',
            # 'SE_T015_016':'Hispanic or Latino: Some other race Alone',
            # 'SE_T015_017':'Hispanic or Latino: Two or more races',
            'SE_T016_001': 'T16. Total Population',
            'SE_T016_002': 'T16. White Alone',
            'SE_T016_003': 'T16. Black or African American Alone',
            'SE_T016_004': 'T16. American Indian and Alaska Native Alone',
            'SE_T016_005': 'T16. Asian Alone',
            'SE_T016_006': 'T16. Native Hawaiian and Other Pacific Islander Alone',
            'SE_T016_007': 'T16. Some other race Alone',
            'SE_T016_008': 'T16. Two or more races',
            'SE_T017_001': 'T17. Total Population',
            'SE_T017_002': 'T17. Not Hispanic or Latino',
            # 'SE_T017_003': 'Not Hispanic or Latino: White Alone',
            # 'SE_T017_004': 'Not Hispanic or Latino: Black or African American Alone',
            # 'SE_T017_005': 'Not Hispanic or Latino: American Indian and Alaska Native Alone',
            # 'SE_T017_006': 'Not Hispanic or Latino: Asian Alone',
            # 'SE_T017_007': 'Not Hispanic or Latino: Native Hawaiian and Other Pacific Islander Alone',
            # 'SE_T017_008': 'Not Hispanic or Latino: Some other race Alone',
            # 'SE_T017_009': 'Not Hispanic or Latino: Two or more races',
            'SE_T017_010': 'T17. Hispanic or Latino',
            # 'SE_T017_011': 'Hispanic or Latino: White Alone',
            # 'SE_T017_012': 'Hispanic or Latino: Black or African American Alone',
            # 'SE_T017_013': 'Hispanic or Latino: American Indian and Alaska Native Alone',
            # 'SE_T017_014': 'Hispanic or Latino: Asian Alone',
            # 'SE_T017_015': 'Hispanic or Latino: Native Hawaiian and Other Pacific Islander Alone',
            # 'SE_T017_016': 'Hispanic or Latino: Some other race Alone',
            # 'SE_T017_017': 'Hispanic or Latino: Two or more races',
            # 'SE_T092_001': 'Households',
            # 'SE_T092_002': 'Household Income: Less than $10,000',
            # 'SE_T092_003': 'Household Income: $10,000 to $14,999',
            # 'SE_T092_004': 'Household Income: $15,000 to $19,999',
            # 'SE_T092_005': 'Household Income: $20,000 to $24,999',
            # 'SE_T092_006': 'Household Income: $25,000 to $29,999',
            # 'SE_T092_007': 'Household Income: $30,000 to $34,999',
            # 'SE_T092_008': 'Household Income: $35,000 to $39,999',
            # 'SE_T092_009': 'Household Income: $40,000 to $44,999',
            # 'SE_T092_010': 'Household Income: $45,000 to $49,999',
            # 'SE_T092_011': 'Household Income: $50,000 to $59,999',
            # 'SE_T092_012': 'Household Income: $60,000 to $74,999',
            # 'SE_T092_013': 'Household Income: $75,000 to $99,999',
            # 'SE_T092_014': 'Household Income: $100,000 to $124,999',
            # 'SE_T092_015': 'Household Income: $125,000 to $149,999',
            # 'SE_T092_016': 'Household Income: $150,000 to $199,999',
            # 'SE_T092_017': 'Household Income: $200,000 or more',
            # 'SE_T092A001': 'Households',
            # 'SE_T092A002': 'Less than $10,000',
            # 'SE_T092A003': 'Less than $15,000',
            # 'SE_T092A004': 'Less than $20,000',
            # 'SE_T092A005': 'Less than $25,000',
            # 'SE_T092A006': 'Less than $30,000',
            # 'SE_T092A007': 'Less than $35,000',
            # 'SE_T092A008': 'Less than $40,000',
            # 'SE_T092A009': 'Less than $45,000',
            # 'SE_T092A010': 'Less than $50,000',
            # 'SE_T092A011': 'Less than $60,000',
            # 'SE_T092A012': 'Less than $75,000',
            # 'SE_T092A013': 'Less than $100,000',
            # 'SE_T092A014': 'Less than $125,000',
            # 'SE_T092A015': 'Less than $150,000',
            # 'SE_T092A016': 'Less than $200,000',
            # 'SE_T092B001': 'Households',
            # 'SE_T092B002': 'More than $10,000',
            # 'SE_T092B003': 'More than $15,000',
            # 'SE_T092B004': 'More than $20,000',
            # 'SE_T092B005': 'More than $25,000',
            # 'SE_T092B006': 'More than $30,000',
            # 'SE_T092B007': 'More than $35,000',
            # 'SE_T092B008': 'More than $40,000',
            # 'SE_T092B009': 'More than $45,000',
            # 'SE_T092B010': 'More than $50,000',
            # 'SE_T092B011': 'More than $60,000',
            # 'SE_T092B012': 'More than $75,000',
            # 'SE_T092B013': 'More than $100,000',
            # 'SE_T092B014': 'More than $125,000',
            # 'SE_T092B015': 'More than $150,000',
            # 'SE_T092B016': 'More than $200,000',
            # 'SE_T093_001': 'Median household income In 1999 Dollars',
            # 'SE_T096_001': 'Average household income In 1999 Dollars',
            # 'SE_T162_001': 'Owner-occupied housing units',
            # 'SE_T162_002': 'Value For All Owner-occupied housing units: Less than $20,000',
            # 'SE_T162_003': 'Value For All Owner-occupied housing units: $20,000 to $49,999',
            # 'SE_T162_004': 'Value For All Owner-occupied housing units: $50,000 to $99,999',
            # 'SE_T162_005': 'Value For All Owner-occupied housing units: $100,000 to $149,999',
            # 'SE_T162_006': 'Value For All Owner-occupied housing units: $150,000 to $299,999',
            # 'SE_T162_007': 'Value For All Owner-occupied housing units: $300,000 to $499,999',
            # 'SE_T162_008': 'Value For All Owner-occupied housing units: $500,000 to $749,999',
            # 'SE_T162_009': 'Value For All Owner-occupied housing units: $750,000 to $999,999',
            # 'SE_T162_010': 'Value For All Owner-occupied housing units: $1,000,000 or more',
            # 'SE_T184_001': 'T184. Population for whom poverty status is determined:',
            # 'SE_T184_002': 'T184. Under .50',
            # 'SE_T184_003': 'T184. .50 to .74',
            # 'SE_T184_004': 'T184. .75 to .99',
            # 'SE_T184_005': 'T184. 1.00 to 1.49',
            # 'SE_T184_006': 'T184. 1.50 to 1.99',
            # 'SE_T184_007': 'T184. 2.00 and over'}
            }

    try:
        dataset = Dataset.objects.get(name=str(year)+' Census Tracts')
        # temp = DataElement.objects.filter(datafield__dataset_id=dataset.id).aggregate(max=Max('id'),min=Min('id'))
        # for i in range(temp['min']/10000*10000+10000,temp['max']/10000*10000+10000,10000):
        #     DataElement.objects.filter(datafield__dataset_id=dataset.id,id__lte=i).delete()
        # print 'dataelements deleted'
    except Exception as e:
        print e
        print 'Dataset "'+str(year), 'Census Tracts" does not exist'
        return
    for key in flds:
        try:
            df = DataField.objects.filter(dataset_id=dataset.id).get(field_name=key)
        except Exception:
            df = DataField(dataset=dataset, field_name=key,
                           field_en=flds[key], field_longname=flds[key],
                           field_type=DataField.INTEGER)
            df.save()
        flds[key] = df
    for i in range(1, 6):
        filename = 'part' + str(i) + ' tracts.csv'
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   'data/' + str(year) + '/' + filename))
        openfile = open(filename, 'rb')
        csv_file = csv.DictReader(openfile)
        for line in csv_file:
            geo = '0'*(11-len(line['Geo_FIPS'])) + line['Geo_FIPS']
            try:
                me = MapElement.objects.filter(dataset_id=dataset.id).get(remote_id=geo)
            except Exception:
                print 'GEOID:', line['Geo_FIPS'], 'does not exist'
                continue
            current = {}
            for key in line:
                if key in flds:
                    try:
                        de = DataElement(datafield=flds[key], mapelement=me, int_data=int(line[key]))
                    except Exception:
                        continue
                    de.save()
                    if key[-4:] == '_001':
                        current[key[:-4]] = de
                    try:
                        de.denominator = current[key[:-4]]
                        de.save()
                    except Exception:
                        pass
        print 'file', filename, 'processed'
