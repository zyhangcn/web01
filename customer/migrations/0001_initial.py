# Generated by Django 2.2.17 on 2020-12-29 11:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('identify', models.SmallIntegerField(choices=[(0, '普通用户'), (2, '管理员'), (4, '超级管理员')], default=0)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('token', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('created_time', models.DateField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='customer.User')),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64, unique=True)),
                ('age', models.IntegerField()),
                ('professional', models.CharField(max_length=64)),
                ('province', models.CharField(max_length=32)),
                ('city', models.CharField(max_length=32)),
                ('join_time', models.DateField(auto_now_add=True)),
                ('update_time', models.DateField(auto_now=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('project', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='users', to='project.Project')),
            ],
            options={
                'ordering': ['username', 'age'],
            },
        ),
    ]
