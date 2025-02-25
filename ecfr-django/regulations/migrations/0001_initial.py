# Generated by Django 5.1.6 on 2025-02-09 18:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Title',
            fields=[
                ('number', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('latest_amended_on', models.DateField(blank=True, null=True)),
                ('latest_issue_date', models.DateField(blank=True, null=True)),
                ('up_to_date_as_of', models.DateField(blank=True, null=True)),
                ('reserved', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Agency',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('short_name', models.CharField(blank=True, max_length=63, null=True)),
                ('display_name', models.CharField(max_length=255)),
                ('sortable_name', models.CharField(max_length=255)),
                ('slug', models.SlugField(max_length=255, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='regulations.agency')),
            ],
            options={
                'verbose_name_plural': 'agencies',
                'ordering': ['sortable_name'],
            },
        ),
        migrations.CreateModel(
            name='CFRReference',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chapter', models.CharField(blank=True, max_length=25, null=True)),
                ('subtitle', models.CharField(blank=True, max_length=25, null=True)),
                ('part', models.CharField(blank=True, max_length=25, null=True)),
                ('subchapter', models.CharField(blank=True, max_length=25, null=True)),
                ('section', models.CharField(blank=True, max_length=20)),
                ('agency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cfr_references', to='regulations.agency')),
                ('title', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regulations.title')),
            ],
            options={
                'ordering': ['title', 'chapter'],
                'unique_together': {('agency', 'title', 'chapter', 'subtitle', 'part', 'subchapter')},
            },
        ),
    ]
