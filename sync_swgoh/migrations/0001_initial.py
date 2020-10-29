# Generated by Django 3.1.2 on 2020-10-29 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseAbility',
            fields=[
                ('ability_id', models.CharField(db_index=True, max_length=100, primary_key=True, serialize=False, verbose_name='Ability ID')),
                ('ability_name', models.CharField(max_length=100, verbose_name='Ability Name')),
                ('unit_id', models.CharField(db_index=True, max_length=100, verbose_name='Unit ID')),
                ('tier_max', models.PositiveSmallIntegerField(verbose_name='Max Tier')),
                ('is_zeta', models.BooleanField(db_index=True, verbose_name='is Zeta')),
                ('is_omega', models.BooleanField(verbose_name='is Omega')),
                ('url_image', models.CharField(editable=False, max_length=255, verbose_name='URL Image')),
            ],
            options={
                'verbose_name': 'Ability',
                'verbose_name_plural': 'Abilities',
            },
        ),
        migrations.CreateModel(
            name='BaseUnit',
            fields=[
                ('unit_id', models.CharField(db_index=True, max_length=100, primary_key=True, serialize=False, verbose_name='Unit ID')),
                ('unit_name', models.CharField(max_length=100, verbose_name='Unit Name')),
                ('max_power', models.PositiveIntegerField(verbose_name='Max Power')),
                ('url_image', models.CharField(editable=False, max_length=255, verbose_name='URL Image')),
                ('combat_type', models.PositiveSmallIntegerField(choices=[(1, ''), (2, '')], editable=False, verbose_name='Combat Type')),
            ],
            options={
                'verbose_name': 'Unit',
                'verbose_name_plural': 'Units',
            },
        ),
    ]
