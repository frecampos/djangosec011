# Generated by Django 3.2.1 on 2021-05-13 02:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('misPerris', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mascota',
            fields=[
                ('nombre', models.CharField(max_length=25, primary_key=True, serialize=False)),
                ('edad', models.IntegerField()),
                ('descripion', models.TextField()),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='misPerris.categoria')),
            ],
        ),
    ]
