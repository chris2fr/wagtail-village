# Generated by Django 5.0.6 on 2024-06-21 07:03

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("wagtail_village_forms", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="formpage",
            name="intro",
        ),
    ]
