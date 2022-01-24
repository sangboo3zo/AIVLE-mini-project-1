import datetime
from django.db import models
from miniapp.utlils import upload_image


class Cat(models.Model):
    cat_id = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=20)
    gender = models.CharField(max_length=20)
    neutral = models.CharField(max_length=20)
    location = models.ForeignKey('Location', models.DO_NOTHING, db_column='location')
    appearance = models.CharField(max_length=2000, blank=True, null=True)
    status = models.CharField(max_length=2000, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Cat'


class CatBoard(models.Model):
    board_id = models.AutoField(primary_key=True)
    cat = models.ForeignKey(Cat, models.DO_NOTHING)
    user_no = models.ForeignKey('User', models.DO_NOTHING, db_column='user_no')
    date_time = models.DateTimeField()
    board_text = models.TextField(blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'Cat_board'


class CatPhoto(models.Model):
    objects = models.Manager()
    photo_id = models.AutoField(primary_key=True)
    cat = models.ForeignKey(Cat, models.DO_NOTHING)
    user_no = models.ForeignKey('User', models.DO_NOTHING, db_column='user_no')
    cat_photo = models.ImageField(upload_to=upload_image)
    date_time = models.DateTimeField()

    class Meta:
        db_table = 'Cat_photo'


class Feed(models.Model):
    feed_id = models.AutoField(primary_key=True)
    user_no = models.ForeignKey('User', models.DO_NOTHING, db_column='user_no')
    cat = models.ForeignKey(Cat, models.DO_NOTHING)
    date_time = models.DateTimeField()

    class Meta:
        # managed = False
        db_table = 'Feed'


class Location(models.Model):
    location1 = models.CharField(max_length=50)
    location2 = models.CharField(max_length=50)
    location3 = models.CharField(max_length=50)
    location4 = models.CharField(primary_key=True, max_length=50)

    class Meta:
        # managed = False
        db_table = 'Location'


class User(models.Model):
    user_no = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=20, unique=True)
    user_name = models.CharField(max_length=20)
    user_email = models.CharField(max_length=60)
    user_pw = models.CharField(max_length=20)
    date_joined = models.DateField()
    class Meta:
        # managed = False
        db_table = 'User'


class UserHasCat(models.Model):
    user_no = models.ForeignKey(User, models.DO_NOTHING, db_column='user_no')
    cat = models.ForeignKey(Cat, models.DO_NOTHING)

    class Meta:
        # managed = False
        db_table = 'User_has_Cat'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'