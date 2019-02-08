from django.contrib.gis.geos import Polygon, Point
from gis_csdt.geometry_tools import circle_as_polygon
from gis_csdt.models import MapElement
from django.contrib.gis.measure import Distance
from django.db.models import Q
from django.http import HttpResponseBadRequest


def filter_request(parameters, model_type):
    if 'tag' in parameters:
        tags = parameters['tag']
    elif 'tags' in parameters:
        tags = parameters['tags']
    else:
        tags = False

    if 'match' in parameters:
        matchall = parameters['match'] == 'all'
    else:
        matchall = False

    queryset = MapElement.objects.none()
    if tags:
        tags = tags.split(',')
        if type(tags) is not list:
            tags = [tags]
        if matchall:
            queryset = MapElement.objects
            for tag in tags:
                try:
                    num = int(tag)
                    queryset = queryset.filter(tagindiv__tag=num)
                except Exception:
                    queryset = queryset.filter(tagindiv__tag__tag=tag)
        else:
            for tag in tags:
                try:
                    num = int(tag)
                    queryset = queryset | MapElement.objects.filter(tagindiv__tag=num)
                except Exception:
                    queryset = queryset | MapElement.objects.filter(tagindiv__tag__tag=tag)
        queryset = queryset.filter(tagindiv__tag__approved=True)
    else:
        queryset = MapElement.objects

    if 'remote_id' in parameters:
        queryset = queryset.filter(remote_id=parameters['remote_id'])

    if 'dataset' in parameters:
        dataset_list = parameters['dataset'].strip().split(',')
        if type(dataset_list) is not list:
            dataset_list = [dataset_list]
        for dataset in dataset_list:
            try:
                r = int(dataset)
                queryset = queryset.filter(dataset__id__exact=r)
            except Exception:
                queryset = queryset.filter(dataset__name__icontains=dataset)

    # make it just one type now
    if model_type != 'mapelement':
        kwargs = {model_type: None}
        queryset = queryset.exclude(**kwargs)

    if model_type == 'mappoint':
        if 'street' in parameters:
            queryset = queryset.filter(mappoint__street__iexact=parameters['street'])
        if 'city' in parameters:
            queryset = queryset.filter(mappoint__city__iexact=parameters['city'])
        if 'state' in parameters:
            queryset = queryset.filter(mappoint__state__iexact=parameters['state'])
        if 'county' in parameters:
            queryset = queryset.filter(mappoint__county__iexact=parameters['county'])
        for key in ['zipcode', 'zip', 'zip_code']:
            if key in parameters:
                queryset = queryset.filter(mappoint__zipcode__iexact=parameters[key])

    bb = {}
    for key in ['max_lat', 'min_lat', 'max_lon', 'min_lon']:
        if key in parameters:
            try:
                r = float(parameters[key])
            except Exception:
                return HttpResponseBadRequest('Invalid radius. Only integers accepted.')
                continue
            bb[key] = r

    if 'max_lat' in bb and 'min_lat' in bb and 'max_lon' in bb and 'min_lon' in bb:
        geom = Polygon.from_bbox((bb['min_lon'], bb['min_lat'],
                                  bb['max_lon'], bb['max_lat']))
        if model_type == 'mappoint':
            queryset = queryset.filter(point__within=geom)
        elif model_type == 'mappolygon':
            queryset = queryset.filter(mappolygon__mpoly__bboverlaps=geom)
        elif model_type == 'mapelement':
            queryset = queryset.filter((~Q(mappoint=None) & Q(point__within=geom)) | (~Q(mappolygon=None) & Q(mappolygon__mpoly__bboverlaps=geom)))

    if 'radius' in parameters and 'center' in parameters:
        try:
            radius = int(parameters['radius'])
        except Exception:
            return HttpResponseBadRequest('Invalid radius. Only integers accepted.')
        temp = parameters['center'].split(',')
        try:
            if len(temp) != 2:
                raise
            temp[0] = float(temp[0])
            temp[1] = float(temp[1])
            center = Point(temp[0], temp[1])
        except Exception:
            return HttpResponseBadRequest('Invalid center. '
                                          'Format is: center=lon,lat')
        queryset = queryset.filter(point__distance_lte=(center, Distance(mi=radius)))
    elif 'radius' in parameters or 'center' in parameters:
        return HttpResponseBadRequest('If a center or radius is specified, '
                                      'the other must also be specified.')

    return queryset.distinct()


def neighboring_points(point, queryset, distance):
    distance = distance * 2
    all_points = queryset.filter(point__distance_lte=(point.point, distance)).distinct()
    point_set = list(all_points)  # .values_list('point', flat=True))
    print point_set
    for p in point_set:
        new_points = queryset.filter(point__distance_lte=(p.point, distance)) \
                     .exclude(id__in=[x.id for x in point_set]).distinct()
        all_points = all_points | new_points
        point_set.extend(list(new_points))  # .values_list('point',flat=True)))
    return all_points.distinct()


def unite_radius_bubbles(points, distances):
    geometry = {}
    for d in distances:
        geometry[d] = circle_as_polygon(lat=points[0].point.y,
                                        lon=points[0].point.x, distance=d)
        for p in points[1:]:
            geometry[d] = geometry[d].union(circle_as_polygon(lat=p.point.y,
                                                              lon=p.point.x,
                                                              distance=d))
    return geometry
