# Generated by Django 3.2.5 on 2022-05-22 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_delete_stdtable'),
    ]

    operations = [
        migrations.CreateModel(
            name='StdTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=5)),
                ('item', models.CharField(max_length=20)),
                ('cluster', models.IntegerField(null=True)),
                ('weight', models.FloatField()),
                ('age', models.FloatField()),
                ('height', models.FloatField()),
            ],
        ),
    ]
