# Generated by Django 3.2.16 on 2022-11-19 05:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('notes', '0002_alter_note_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='note_groups', related_query_name='note_group', to='auth.user'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='owner',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='notes', related_query_name='note', to='auth.user'),
            preserve_default=False,
        ),
    ]