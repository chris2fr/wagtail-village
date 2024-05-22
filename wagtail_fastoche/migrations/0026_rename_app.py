import django.db.models.deletion
import wagtail.blocks
import wagtail.documents.blocks
import wagtail.fields
import wagtail.images.blocks
from django.db import connection, migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("wagtail_fastoche", "0025_alter_contentpage_body"),
    ]

    operations = []
