# Generated by Django 5.1.6 on 2025-02-09 22:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regulations', '0003_cfrreference_full_text_cfrreference_last_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='cfr_word_count',
            field=models.BigIntegerField(blank=True, default=0, help_text='Total word count of all related CFR reference full texts', null=True),
        ),
        migrations.AlterField(
            model_name='cfrreference',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cfr_references', to='regulations.title'),
        ),
    ]
