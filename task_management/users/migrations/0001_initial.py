# Generated by Django 4.1 on 2023-10-22 13:15

import core.utils
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.CharField(default=core.utils.Utils.uuid4, editable=False, max_length=36, primary_key=True, serialize=False)),
                ('created_on_datetime', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated_on_datetime', models.DateTimeField(auto_now=True, db_index=True)),
                ('max_tasks_per_day', models.IntegerField(default=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_on_datetime'],
                'abstract': False,
            },
        ),
    ]