"""Initial migration for calendar"""
from django./db import migrations, models
class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='',
            fields=[
                ('id', models.UUIDField(primary_key=True, default=models.UUIDField(default='__random__', editable=False))),
            ],
        ),
    ]
