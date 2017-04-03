# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

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
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
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


class Author(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'author'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
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


class LiveRadioDictionary(models.Model):
    type = models.CharField(max_length=45, blank=True, null=True)
    name = models.CharField(max_length=45, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'live_radio_dictionary'


class LiveRadioPlayList(models.Model):
    radio_id = models.IntegerField()
    play_date = models.DateTimeField()
    program = models.CharField(max_length=255)
    play_time = models.CharField(max_length=45)
    link_url = models.CharField(max_length=1024, blank=True, null=True)
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'live_radio_play_list'


class LiveTelecastRadio(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    area = models.CharField(max_length=45, blank=True, null=True)
    type = models.CharField(max_length=45, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    url_playlist = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'live_telecast_radio'




class ProgramTopn(models.Model):
    programid = models.CharField(db_column='programID', max_length=50)  # Field name made lowercase.
    programtype = models.CharField(db_column='programType', max_length=45)  # Field name made lowercase.
    count = models.BigIntegerField()
    time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'program_topn'


class RadioProgram(models.Model):
    title = models.CharField(max_length=255)
    type = models.IntegerField(blank=True, null=True)
    subject = models.CharField(max_length=50, blank=True, null=True)
    key_words = models.CharField(max_length=255, blank=True, null=True)
    block = models.CharField(max_length=255, blank=True, null=True)
    compere = models.CharField(max_length=45, blank=True, null=True)
    guests = models.CharField(max_length=255, blank=True, null=True)
    file_name = models.CharField(max_length=45)
    server_name = models.CharField(max_length=45)
    share_name = models.CharField(max_length=45)
    directory = models.CharField(max_length=255)
    duration = models.IntegerField(blank=True, null=True)
    published_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'radio_program'


class RbcProgram(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    subjects = models.CharField(max_length=45, blank=True, null=True)
    block_name = models.CharField(max_length=255, blank=True, null=True)
    radio_id = models.IntegerField(blank=True, null=True)
    play_date = models.DateTimeField(blank=True, null=True)
    duration = models.FloatField(blank=True, null=True)
    file_name = models.CharField(max_length=255, blank=True, null=True)
    rbc_play_link = models.CharField(max_length=255, blank=True, null=True)
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'rbc_program'


class SubjectUserProgram(models.Model):
    shortening = models.CharField(max_length=255)
    code = models.IntegerField()
    describe = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'subject_user_program'


class Test(models.Model):
    test_id = models.IntegerField(blank=True, null=True)
    test_name = models.CharField(max_length=55, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'test'


class Tmp(models.Model):
    program_id = models.IntegerField(blank=True, null=True)
    program_duration = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tmp'


class UserCount(models.Model):
    count = models.BigIntegerField()
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_count'


class UserProgramCollect(models.Model):
    user_id = models.IntegerField()
    program_id = models.IntegerField(blank=True, null=True)
    dir_type = models.IntegerField(blank=True, null=True)
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_program_collect'


class UserProgramExplicitBehavior(models.Model):
    user_id = models.IntegerField()
    program_id = models.IntegerField()
    star = models.IntegerField(blank=True, null=True)
    share = models.IntegerField(blank=True, null=True)
    collect = models.IntegerField(blank=True, null=True)
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_program_explicit_behavior'


class UserProgramScore(models.Model):
    user_id = models.IntegerField()
    program_id = models.IntegerField()
    play_count = models.IntegerField(blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_program_score'


class UserRecommendPlayList(models.Model):
    user_id = models.IntegerField()
    play_time = models.CharField(max_length=45, blank=True, null=True)
    program_id = models.IntegerField()
    dir_type = models.IntegerField(blank=True, null=True)
    is_played = models.IntegerField(blank=True, null=True)
    generate_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'user_recommend_play_list'


class UserStationCollect(models.Model):
    user_id = models.IntegerField()
    radio_id = models.IntegerField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_station_collect'


class UserStationExplicitBehavior(models.Model):
    user_id = models.IntegerField()
    radio_id = models.IntegerField()
    collect = models.IntegerField(blank=True, null=True)
    insert_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'user_station_explicit_behavior'


class Users(models.Model):
    name = models.CharField(max_length=45)
    password = models.CharField(max_length=45, blank=True, null=True)
    login_type = models.IntegerField()
    weibo_id = models.CharField(max_length=255, blank=True, null=True)
    sex = models.IntegerField(blank=True, null=True)
    birth = models.CharField(max_length=255, blank=True, null=True)
    occupation = models.CharField(max_length=45, blank=True, null=True)
    tastes = models.CharField(max_length=255, blank=True, null=True)
    subjects = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
