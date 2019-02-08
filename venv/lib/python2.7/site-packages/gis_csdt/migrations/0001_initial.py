from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('error', models.FloatField(null=True)),
                ('int_data', models.IntegerField(null=True)),
                ('float_data', models.FloatField(null=True)),
                ('char_data', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_en', models.CharField(blank=True, max_length=100)),
                ('field_longname', models.CharField(blank=True, max_length=400)),
                ('field_name', models.CharField(blank=True, max_length=50)),
                ('field_type', models.CharField(choices=[(b'I', b'integer'), (b'F', b'floating point'), (b'C', b'string')], default=b'C', max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Dataset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('url', models.URLField(blank=True, max_length=300)),
                ('cached', models.DateTimeField(blank=True, null=True)),
                ('cache_max_age', models.IntegerField(default=1, verbose_name=b'age when cache should be replaced in days')),
                ('remote_id_field', models.CharField(blank=True, default=b'id', max_length=50, verbose_name=b'column name of key field on the remote server')),
                ('name_field', models.CharField(default=b'name', max_length=50)),
                ('lat_field', models.CharField(default=b'latitude', max_length=50)),
                ('lon_field', models.CharField(default=b'longitude', max_length=50)),
                ('street_field', models.CharField(default=b'street', max_length=50)),
                ('city_field', models.CharField(default=b'city', max_length=50)),
                ('state_field', models.CharField(default=b'state', max_length=50)),
                ('zipcode_field', models.CharField(default=b'zip', max_length=50)),
                ('county_field', models.CharField(default=b'county', max_length=50)),
                ('field1_en', models.CharField(blank=True, max_length=150)),
                ('field1_name', models.CharField(blank=True, max_length=50)),
                ('field2_en', models.CharField(blank=True, max_length=150)),
                ('field2_name', models.CharField(blank=True, max_length=50)),
                ('field3_en', models.CharField(blank=True, max_length=150)),
                ('field3_name', models.CharField(blank=True, max_length=50)),
                ('needs_geocoding', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='MapElement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remote_id', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(max_length=150)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(null=True)),
                ('accuracy', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ObservationValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50)),
                ('value', models.FloatField()),
                ('observation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='gis_csdt.Observation')),
            ],
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sensor_type', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('approved', models.BooleanField(default=False)),
                ('count', models.IntegerField(default=0)),
                ('dataset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='gis_csdt.Dataset')),
            ],
        ),
        migrations.CreateModel(
            name='TagIndiv',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('mapelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gis_csdt.MapElement')),
                ('lat', models.DecimalField(decimal_places=15, max_digits=18)),
                ('lon', models.DecimalField(decimal_places=15, max_digits=18)),
                ('field1', models.CharField(blank=True, max_length=200)),
                ('field2', models.CharField(blank=True, max_length=200)),
                ('field3', models.CharField(blank=True, max_length=200)),
                ('street', models.CharField(blank=True, max_length=200)),
                ('city', models.CharField(blank=True, max_length=100)),
                ('state', models.CharField(blank=True, max_length=2)),
                ('zipcode', models.CharField(blank=True, max_length=5)),
                ('county', models.CharField(blank=True, max_length=75)),
                ('geocoded', models.BooleanField(default=False)),
            ],
            bases=('gis_csdt.mapelement',),
        ),
        migrations.CreateModel(
            name='MapPolygon',
            fields=[
                ('mapelement_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='gis_csdt.MapElement')),
                ('lat', models.CharField(max_length=17)),
                ('lon', models.CharField(max_length=17)),
                ('field1', models.FloatField()),
                ('field2', models.FloatField()),
                ('mpoly', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
            ],
            bases=('gis_csdt.mapelement',),
        ),
        migrations.AddField(
            model_name='tagindiv',
            name='mapelement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis_csdt.MapElement'),
        ),
        migrations.AddField(
            model_name='tagindiv',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis_csdt.Tag'),
        ),
        migrations.AddField(
            model_name='observation',
            name='mapelement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='observations', to='gis_csdt.MapElement'),
        ),
        migrations.AddField(
            model_name='observation',
            name='sensor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis_csdt.Sensor'),
        ),
        migrations.AddField(
            model_name='mapelement',
            name='dataset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='gis_csdt.Dataset'),
        ),
        migrations.AddField(
            model_name='datafield',
            name='dataset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataFields', to='gis_csdt.Dataset'),
        ),
        migrations.AddField(
            model_name='dataelement',
            name='datafield',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dataElements', to='gis_csdt.DataField'),
        ),
        migrations.AddField(
            model_name='dataelement',
            name='denominator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='gis_csdt.DataElement'),
        ),
        migrations.AddField(
            model_name='dataelement',
            name='mapelement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gis_csdt.MapElement'),
        ),
        migrations.AlterUniqueTogether(
            name='tagindiv',
            unique_together=set([('tag', 'mapelement')]),
        ),
        migrations.AlterUniqueTogether(
            name='observationvalue',
            unique_together=set([('observation', 'name')]),
        ),
    ]