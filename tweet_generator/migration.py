from django.contrib.postgres.operations import HStoreExtension
from django.db import migrations, models

class Migration(migrations.Migration):
    operations = [
        HStoreExtension()
    ]