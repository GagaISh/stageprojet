# Generated by Django 5.0.7 on 2024-07-17 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_reservation_alter_salle_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='salle',
            name='disponibilite',
            field=models.BooleanField(default=False),
        ),
    ]
