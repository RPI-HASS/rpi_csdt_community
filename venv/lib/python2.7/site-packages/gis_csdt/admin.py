from django.contrib import admin
from gis_csdt.models import Location, GeoCoordinates, DatasetNameField, \
                            Dataset, MapPoint, PhoneNumber, Tag, MapPolygon, \
                            TagIndiv, DataField, DataElement, Sensor, DataPoint


class DatasetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,              {'fields': ['name', 'url', 'cache_max_age']}),
        ('Field Mapping',   {'fields': ['remote_id_field', 'name_field',
                                        'location', 'coordinates']}),
        ('Custom Field',    {'fields': ['names']}),
        ('Geocoding',       {'fields': ['needs_geocoding']})]


class SensorAdmin(admin.ModelAdmin):
    filter_horizontal = ('datapoints', )


admin.site.register(Dataset, DatasetAdmin)
# for testing
admin.site.register(MapPoint)
admin.site.register(Tag)
admin.site.register(MapPolygon)
admin.site.register(TagIndiv)
admin.site.register(DataField)
admin.site.register(DataElement)
admin.site.register(Sensor, SensorAdmin)
admin.site.register(DataPoint)
admin.site.register(PhoneNumber)
admin.site.register(Location)
admin.site.register(GeoCoordinates)
admin.site.register(DatasetNameField)
