# Generated by Django 3.2.7 on 2021-10-16 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TimeField(blank=True, max_length=160, null=True),
        ),
    ]