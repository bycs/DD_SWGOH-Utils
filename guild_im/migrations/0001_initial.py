# Generated by Django 3.1.2 on 2020-11-04 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sync_swgoh', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IMData',
            fields=[
                ('ally_code', models.PositiveIntegerField(db_index=True, primary_key=True, serialize=False, verbose_name='Ally Code')),
                ('player_name', models.CharField(max_length=100, verbose_name='Player Name')),
                ('gp_chars', models.PositiveIntegerField(verbose_name='GP Characters')),
                ('gp_ships', models.PositiveIntegerField(verbose_name='GP Ships')),
                ('gp_total', models.PositiveIntegerField(verbose_name='GP Total')),
                ('last_updated', models.DateTimeField(verbose_name='Last Updated')),
                ('chars_average_rank', models.PositiveSmallIntegerField(verbose_name='Chars Arena')),
                ('ships_average_rank', models.PositiveSmallIntegerField(verbose_name='Ships Arena')),
            ],
            options={
                'verbose_name': 'Guild Data',
                'verbose_name_plural': 'Guild Data',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IMShip',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ally_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_im.imdata')),
                ('unit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sync_swgoh.baseunit')),
                ('rarity', models.PositiveSmallIntegerField(verbose_name='Rarity')),
                ('power', models.PositiveIntegerField(verbose_name='Power')),
            ],
            options={
                'verbose_name': 'Guild Ship',
                'verbose_name_plural': 'Guild Ships',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='IMCharacter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('ally_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guild_im.imdata')),
                ('unit_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sync_swgoh.baseunit')),
                ('rarity', models.PositiveSmallIntegerField(verbose_name='Rarity')),
                ('gear_level', models.PositiveSmallIntegerField(verbose_name='Gear Level')),
                ('relic_tier', models.PositiveSmallIntegerField(verbose_name='Relic Tier')),
                ('power', models.PositiveIntegerField(verbose_name='Power')),
                ('health', models.PositiveIntegerField(verbose_name='Health')),
                ('protection', models.PositiveIntegerField(verbose_name='Protection')),
                ('speed', models.PositiveSmallIntegerField(verbose_name='Speed')),
                ('physical_damage', models.PositiveSmallIntegerField(verbose_name='Physical Damage')),
                ('critical_damage', models.FloatField(verbose_name='Critical Damage')),
                ('critical_chance', models.FloatField(verbose_name='Critical Chance')),
                ('potency', models.FloatField(verbose_name='Potency')),
                ('tenacity', models.FloatField(verbose_name='Tenacity')),
            ],
            options={
                'verbose_name': 'Guild Character',
                'verbose_name_plural': 'Guild Characters',
                'abstract': False,
            },
        ),
    ]
