# Generated by Django 3.1.4 on 2021-02-10 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('st', '0003_party_admin'),
    ]

    operations = [
        migrations.AlterField(
            model_name='party',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='party',
            name='start_game',
            field=models.DateTimeField(null=True),
        ),
    ]