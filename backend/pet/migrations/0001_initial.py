# Generated by Django 5.1.6 on 2025-02-19 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualPet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='KickPet', max_length=100)),
                ('hunger', models.IntegerField(default=50)),
                ('energy', models.IntegerField(default=50)),
                ('happiness', models.IntegerField(default=50)),
                ('health', models.IntegerField(default=100)),
                ('mood', models.CharField(default='neutral', max_length=50)),
                ('last_updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
