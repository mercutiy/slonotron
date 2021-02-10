# Generated by Django 3.1.4 on 2020-12-16 00:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('st', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='is_applied',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='member',
            name='party',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='st.party'),
        ),
        migrations.AlterField(
            model_name='member',
            name='present_to',
            field=models.OneToOneField(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='st.member'),
        ),
        migrations.AlterField(
            model_name='score',
            name='from_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='from_score', to='st.member'),
        ),
        migrations.AlterField(
            model_name='score',
            name='to_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='to_score', to='st.member'),
        ),
    ]
