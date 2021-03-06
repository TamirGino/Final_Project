# Generated by Django 3.2.5 on 2022-05-15 09:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20220513_1502'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('name', models.CharField(max_length=20, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('name', models.CharField(max_length=5, primary_key=True, serialize=False)),
            ],
        ),
        migrations.AlterField(
            model_name='normtable',
            name='age',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='brand_ASOS',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='brand_HM',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='brand_PULL_BEAR',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='brand_ZARA',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='chest',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='fit_labels',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='height',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='size_labels',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='tummy_labels',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='waist',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='normtable',
            name='weight',
            field=models.FloatField(),
        ),
        migrations.CreateModel(
            name='Size_by_brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chest', models.CharField(max_length=20)),
                ('waist', models.CharField(max_length=20)),
                ('brand_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.brand')),
                ('item_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.item')),
                ('size_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.size')),
            ],
        ),
    ]
