# Generated by Django 3.1.2 on 2020-10-13 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Extension',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('extension_name', models.CharField(max_length=100)),
                ('icon_name', models.CharField(default='nonpic.png', max_length=100)),
                ('displayed', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='SavedData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('field_name', models.CharField(max_length=100)),
                ('content', models.CharField(max_length=1000)),
                ('extension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.extension')),
            ],
        ),
        migrations.CreateModel(
            name='ConfigEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('config_key', models.CharField(max_length=100)),
                ('config_value', models.CharField(max_length=100)),
                ('extension', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='web.extension')),
            ],
        ),
    ]
