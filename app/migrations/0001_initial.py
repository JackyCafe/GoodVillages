# Generated by Django 3.1.1 on 2020-12-27 03:05

import ckeditor.fields
import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=32, unique=True, unique_for_date='publish')),
                ('group_name', models.CharField(default='', max_length=32, null=True, verbose_name='隊名')),
                ('is_active', models.BooleanField(default=True, verbose_name='隊伍有效')),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32, verbose_name='任務名稱')),
                ('task_content', ckeditor.fields.RichTextField(verbose_name='任務內容')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=32, unique=True, unique_for_date='publish')),
                ('publish', models.DateField(default=django.utils.timezone.now, verbose_name='任務發布時間')),
                ('task_type', models.CharField(choices=[('daily_task', '每日任務'), ('work_task', '工作任務')], default='daily_task', max_length=12, verbose_name='任務型別')),
                ('is_vaild', models.BooleanField(default=True)),
                ('point', models.IntegerField(verbose_name='點數')),
            ],
            options={
                'ordering': ['-publish'],
            },
        ),
        migrations.CreateModel(
            name='TeamTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32, null=True, verbose_name='任務名稱')),
                ('task_content', ckeditor.fields.RichTextField(null=True, verbose_name='任務內容')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=32, unique=True, unique_for_date='publish')),
                ('publish', models.DateField(default=django.utils.timezone.now, verbose_name='任務發布時間')),
                ('start_date', models.DateField(null=True, verbose_name='活動開始時間')),
                ('end_date', models.DateField(null=True, verbose_name='活動結束時間')),
                ('point', models.IntegerField(default=0, verbose_name='點數')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('actual_name', models.CharField(max_length=10, verbose_name='姓名')),
                ('authority', models.CharField(choices=[('admin', '管理者'), ('employee', '照服員'), ('resident', '住民'), ('family', '家屬'), ('vendor', '廠商')], default='resident', max_length=20, verbose_name='身分')),
                ('photo', models.ImageField(blank=True, null=True, upload_to='users/%Y/%m/%d/', verbose_name='照片')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='userprofile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='WorkTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32, null=True, verbose_name='任務名稱')),
                ('task_content', ckeditor.fields.RichTextField(null=True, verbose_name='任務內容')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=32, unique=True, unique_for_date='publish')),
                ('publish', models.DateField(default=django.utils.timezone.now, verbose_name='任務發布時間')),
                ('point', models.IntegerField(default=0, verbose_name='獲得點數')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='worktask_assigner', to='app.userprofile', verbose_name='任務發布者')),
            ],
        ),
        migrations.CreateModel(
            name='SubTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_task_title', models.CharField(max_length=20)),
                ('sub_task_content', models.TextField()),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.task')),
            ],
        ),
        migrations.CreateModel(
            name='PersonalTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assign_date', models.DateField(default=datetime.datetime.now, verbose_name='指派日期')),
                ('finish_date', models.DateField(blank=True, null=True, verbose_name='完成日期')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=32, unique=True, unique_for_date='assign_date')),
                ('is_award', models.BooleanField(default=False, verbose_name='是否獎勵過')),
                ('point', models.IntegerField(default=0, verbose_name='點數')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.task', verbose_name='任務')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.userprofile', verbose_name='人員')),
            ],
            options={
                'ordering': ['-assign_date'],
            },
        ),
        migrations.CreateModel(
            name='MyWorkTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_created=True)),
                ('start_time', models.DateField(verbose_name='任務開始時間')),
                ('end_time', models.DateField(verbose_name='任務結束時間')),
                ('point', models.IntegerField(default=0, verbose_name='獲得點數')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myworktask', to='app.worktask', verbose_name='任務名稱')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myworktask_accepter', to='app.userprofile', verbose_name='任務接受者')),
            ],
        ),
        migrations.CreateModel(
            name='MyTeamTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_award', models.BooleanField(default=False, verbose_name='是否獎勵過')),
                ('point', models.IntegerField(default=0, verbose_name='點數')),
                ('group', models.ManyToManyField(related_name='group', to='app.Group')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL, verbose_name='名字')),
            ],
        ),
        migrations.CreateModel(
            name='MyAwardTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task_name', models.CharField(max_length=32, null=True, verbose_name='任務名稱')),
                ('task_content', ckeditor.fields.RichTextField(null=True, verbose_name='任務內容')),
                ('slug', django_extensions.db.fields.RandomCharField(blank=True, editable=False, length=32, unique=True, unique_for_date='publish')),
                ('publish', models.DateField(default=django.utils.timezone.now, verbose_name='任務發布時間')),
                ('point', models.IntegerField(default=0, verbose_name='支付點數')),
                ('approve_time', models.DateField(null=True, verbose_name='任務核可時間')),
                ('accept_time', models.DateField(null=True, verbose_name='任務接受時間')),
                ('accept_man', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accept_man', to=settings.AUTH_USER_MODEL, verbose_name='任務接受人')),
                ('approve_man', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approve_man', to=settings.AUTH_USER_MODEL, verbose_name='任務核可人')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awardtask_user', to='app.userprofile', verbose_name='名字')),
            ],
        ),
        migrations.AddField(
            model_name='group',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='app.userprofile', verbose_name='隊長'),
        ),
        migrations.AddField(
            model_name='group',
            name='task',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.teamtask', verbose_name='團隊任務'),
        ),
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('donate_date', models.DateField(default=django.utils.timezone.now, verbose_name='捐款日期')),
                ('donate_points', models.IntegerField(verbose_name='團隊所得點數')),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.group', verbose_name='群組')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='捐款人')),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transaction_date', models.DateField(default=django.utils.timezone.now, verbose_name='交易日期')),
                ('deposit', models.IntegerField(default=0, verbose_name='入賬')),
                ('withdraw', models.IntegerField(default=0, verbose_name='提款')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='住民名字', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
