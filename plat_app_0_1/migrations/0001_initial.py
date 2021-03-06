# Generated by Django 3.0.6 on 2020-06-17 03:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ch_rete_dtl',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pday', models.IntegerField()),
                ('ch_id', models.IntegerField()),
                ('rete_1', models.FloatField()),
                ('rete_2', models.FloatField()),
                ('rete_3', models.FloatField()),
                ('rete_4', models.FloatField()),
                ('rete_5', models.FloatField()),
                ('rete_6', models.FloatField()),
                ('rete_7', models.FloatField()),
                ('rete_8', models.FloatField()),
                ('rete_9', models.FloatField()),
                ('rete_10', models.FloatField()),
                ('rete_11', models.FloatField()),
                ('rete_12', models.FloatField()),
                ('rete_13', models.FloatField()),
                ('rete_14', models.FloatField()),
                ('rete_15', models.FloatField()),
                ('rete_16', models.FloatField()),
                ('rete_17', models.FloatField()),
                ('rete_18', models.FloatField()),
                ('rete_19', models.FloatField()),
                ('rete_20', models.FloatField()),
                ('rete_21', models.FloatField()),
                ('rete_22', models.FloatField()),
                ('rete_23', models.FloatField()),
                ('rete_24', models.FloatField()),
                ('rete_25', models.FloatField()),
                ('rete_26', models.FloatField()),
                ('rete_27', models.FloatField()),
                ('rete_28', models.FloatField()),
                ('rete_29', models.FloatField()),
                ('dnu', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Dim_ch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ch', models.IntegerField()),
                ('ch_type', models.CharField(max_length=200)),
                ('ch_name', models.CharField(max_length=200)),
            ],
        ),
    ]
