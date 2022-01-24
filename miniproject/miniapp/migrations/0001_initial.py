
# Generated by Django 2.2.5 on 2022-01-24 11:20

from django.db import migrations, models
import django.db.models.deletion
import miniapp.utlils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True)),
            ],
            options={
                'db_table': 'auth_group',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthGroupPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_group_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codename', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'auth_permission',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.IntegerField()),
                ('username', models.CharField(max_length=150, unique=True)),
                ('first_name', models.CharField(max_length=150)),
                ('last_name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=254)),
                ('is_staff', models.IntegerField()),
                ('is_active', models.IntegerField()),
                ('date_joined', models.DateTimeField()),
            ],
            options={
                'db_table': 'auth_user',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_groups',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='AuthUserUserPermissions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_user_permissions',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoAdminLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action_time', models.DateTimeField()),
                ('object_id', models.TextField(blank=True, null=True)),
                ('object_repr', models.CharField(max_length=200)),
                ('action_flag', models.PositiveSmallIntegerField()),
                ('change_message', models.TextField()),
            ],
            options={
                'db_table': 'django_admin_log',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoContentType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_label', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'django_content_type',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
                ('applied', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DjangoSession',
            fields=[
                ('session_key', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('session_data', models.TextField()),
                ('expire_date', models.DateTimeField()),
            ],
            options={
                'db_table': 'django_session',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Cat',
            fields=[
                ('cat_id', models.AutoField(primary_key=True, serialize=False)),
                ('cat_name', models.CharField(max_length=20)),
                ('gender', models.CharField(max_length=20)),
                ('neutral', models.CharField(max_length=20)),
                ('appearance', models.CharField(blank=True, max_length=2000, null=True)),
                ('status', models.CharField(blank=True, max_length=2000, null=True)),
            ],
            options={
                'db_table': 'Cat',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('location1', models.CharField(max_length=50)),
                ('location2', models.CharField(max_length=50)),
                ('location3', models.CharField(max_length=50)),
                ('location4', models.CharField(max_length=50, primary_key=True, serialize=False)),
            ],
            options={
                'db_table': 'Location',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_no', models.AutoField(primary_key=True, serialize=False)),
                ('user_id', models.CharField(max_length=20, unique=True)),
                ('user_name', models.CharField(max_length=20)),
                ('user_email', models.CharField(max_length=60)),
                ('user_pw', models.CharField(max_length=20)),
                ('date_joined', models.DateField()),
            ],
            options={
                'db_table': 'User',
            },
        ),
        migrations.CreateModel(
            name='UserHasCat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.Cat')),
                ('user_no', models.ForeignKey(db_column='user_no', on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.User')),
            ],
            options={
                'db_table': 'User_has_Cat',
            },
        ),
        migrations.CreateModel(
            name='Feed',
            fields=[
                ('feed_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.Cat')),
                ('user_no', models.ForeignKey(db_column='user_no', on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.User')),
            ],
            options={
                'db_table': 'Feed',
            },
        ),
        migrations.CreateModel(
            name='CatPhoto',
            fields=[
                ('photo_id', models.AutoField(primary_key=True, serialize=False)),
                ('cat_photo', models.ImageField(upload_to=miniapp.utlils.upload_image)),
                ('date_time', models.DateTimeField()),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.Cat')),
                ('user_no', models.ForeignKey(db_column='user_no', on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.User')),
            ],
            options={
                'db_table': 'Cat_photo',
            },
        ),
        migrations.CreateModel(
            name='CatBoard',
            fields=[
                ('board_id', models.AutoField(primary_key=True, serialize=False)),
                ('date_time', models.DateTimeField()),
                ('board_text', models.TextField(blank=True, null=True)),
                ('cat', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.Cat')),
                ('user_no', models.ForeignKey(db_column='user_no', on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.User')),
            ],
            options={
                'db_table': 'Cat_board',
            },
        ),
        migrations.AddField(
            model_name='cat',
            name='location',
            field=models.ForeignKey(db_column='location', on_delete=django.db.models.deletion.DO_NOTHING, to='miniapp.Location'),
        ),
    ]
