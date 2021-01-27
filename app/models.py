from datetime import datetime
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django_extensions.db.fields import RandomCharField


class UserProfile(models.Model):
    AUTHORITY_CHOICE = (('admin', '管理者'),
                        ('employee', '照服員'),
                        ('resident', '住民'),
                        ('family', '家屬'),
                        ('vendor', '廠商'),
                        )
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    actual_name = models.CharField(max_length=10, verbose_name='姓名')
    authority = models.CharField(max_length=20, verbose_name='身分', choices=AUTHORITY_CHOICE, default='resident')
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', null=True, blank=True, verbose_name='照片')


    def __str__(self):
        return self.actual_name


#個人帳戶
class Account(models.Model):
    Memo_CHOICE = (('家屬購買', '家屬購買'),
                        ('task', '任務所得'),
                        ('other', '其他'),
                        )
    user = models.ForeignKey(UserProfile,models.CASCADE,related_name='account_user',verbose_name='住民名字')
    transaction_date  = models.DateField(default=timezone.now,verbose_name='交易日期')
    transaction_memo = models.CharField(default=' ',max_length=40,verbose_name='交易內容',choices=Memo_CHOICE)
    slug =  RandomCharField(length=32, unique=True, unique_for_date='transaction_date')
    deposit = models.IntegerField(verbose_name='入賬',default=0,null=False)
    withdraw = models.IntegerField(verbose_name='提款',default=0,null=False)
    processor = models.ForeignKey(UserProfile,models.CASCADE,related_name='account_processor',verbose_name='處理者',default=1)

    def __str__(self):
        return self.user

    def get_account_url(self):
        return reverse('app:account_list',args=(self.id,self.slug))

# 任務
class Task(models.Model):
    TASK_CHOICE = (('daily_task', '每日任務')
                   # , ('team_task', '團隊任務')
                   # , ('reward_task', '懸賞任務')
                   , ('work_task', '工作任務'))
    task_name = models.CharField(max_length=32, verbose_name='任務名稱')
    task_content = RichTextField(verbose_name='任務內容')
    slug = RandomCharField(length=32, unique=True, unique_for_date='publish')
    publish = models.DateField(default=timezone.now, verbose_name='任務發布時間')
    task_type = models.CharField(max_length=12, choices=TASK_CHOICE, default='daily_task', verbose_name='任務型別')
    is_vaild  = models.BooleanField(default=True)
    point = models.IntegerField(verbose_name='點數')

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return self.task_name

    #編輯主任務
    def task_edit(self,url):
        return reverse('app:task_edit', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def absolute_url(self):
        return reverse('app:task_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    #新增次要任務
    def addSubTask_url(self):
        return reverse('app:sub_task_add', args=[self.publish.year, self.publish.month, self.publish.day, self.slug])

    def invalidTask_url(self):
        if self.is_vaild == True:
            return reverse('app:invalidTask', args=[self.publish.year, self.publish.month, self.publish.day, self.slug, 0])
        else:
            return reverse('app:invalidTask',
                           args=[self.publish.year, self.publish.month, self.publish.day, self.slug, 1])


# 每日子任務、團隊子任務
class SubTask(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, )
    sub_task_title = models.CharField(max_length=20)
    sub_task_content = models.TextField()

    def __str__(self):
        return self.sub_task_title


# 管理個人任務中,完成日是否有空值
class PersonalTaskManager(models.Manager):
    def get_queryset(self):
        return super(PersonalTaskManager, self).get_queryset().filter(finish_date = None)


# 個人任務中是否領取獎勵
class PersonTaskAwardManage (models.Manager):
    def get_queryset(self):
        return super(PersonTaskAwardManage, self).get_queryset()\
            .filter(finish_date__isnull=False)
            # .filter(is_award=False)


# 個人任務
class PersonalTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name='人員')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='任務')
    assign_date = models.DateField(default=datetime.now,verbose_name='指派日期')
    finish_date = models.DateField(auto_now_add=False,verbose_name='完成日期',blank=True,null = True)
    slug = RandomCharField(length=32, unique=True, unique_for_date='assign_date')
    is_award =  models.BooleanField(default=False,verbose_name='是否獎勵過')
    point = models.IntegerField(default=0,verbose_name='點數')
    objects = models.Manager()
    personalTaskManager = PersonalTaskManager()
    personal_task_award = PersonTaskAwardManage()

    class Meta:
        ordering = ['-assign_date']

    def __str__(self):
        return self.user.username

    def generate_qr_code(self):
        return reverse('app:generate_qr_code', args=[self.id, self.slug])

    def update_personal_task(self):
        return reverse('app:update_personal_task', args=[self.id, self.slug])


# 管理員發布的團隊任務
class TeamTask(models.Model):
    task_name = models.CharField(max_length=32, verbose_name='任務名稱',null=True)
    task_content = RichTextField(verbose_name='任務內容',null=True)
    slug = RandomCharField(length=32, unique=True, unique_for_date='publish')
    publish = models.DateField(default=timezone.now, verbose_name='任務發布時間')
    start_date = models.DateField(auto_now_add=False,verbose_name='活動開始時間',null=True)
    end_date = models.DateField(auto_now_add=False,verbose_name='活動結束時間',null=True)
    point = models.IntegerField(default=0,verbose_name='點數')

    def __str__(self):
       return self.task_name


#
class Group(models.Model):
    owner = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='owner',verbose_name='隊長')
    slug = RandomCharField(length=32, unique=True, unique_for_date='publish')
    group_name = models.CharField(max_length=32,verbose_name='隊名',null=True,default='')
    task = models.ForeignKey(TeamTask,models.CASCADE,verbose_name='團隊任務',null=True)
    is_active =  models.BooleanField(default=True,verbose_name='隊伍有效')

    def __str__(self):
        return self.group_name


class Donate(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='捐款人')
    group = models.ForeignKey(Group,models.CASCADE,verbose_name='群組')
    donate_date = models.DateField(default=timezone.now,verbose_name='捐款日期')
    donate_points = models.IntegerField(verbose_name='團隊所得點數')

    def __str__(self):
        return self.group


#加入團隊活動的個人
class MyTeamTask(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='user',verbose_name='名字')
    group = models.ManyToManyField(Group,related_name='group')
    is_award =  models.BooleanField(default=False,verbose_name='是否獎勵過')
    point = models.IntegerField(default=0,verbose_name='點數')

    def __str__(self):
        return self.user.userprofile.actual_name


#懸賞任務
class MyAwardTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='awardtask_user', verbose_name='名字')
    task_name = models.CharField(max_length=32, verbose_name='任務名稱', null=True)
    task_content = RichTextField(verbose_name='任務內容', null=True)
    slug = RandomCharField(length=32, unique=True, unique_for_date='publish')
    publish = models.DateField(default=timezone.now, verbose_name='任務發布時間')
    point = models.IntegerField(default=0,verbose_name='支付點數')
    approve_man = models.ForeignKey(User,models.CASCADE,related_name='approve_man',verbose_name='任務核可人',null = True)
    approve_time = models.DateField(auto_now_add=False,verbose_name='任務核可時間',null=True)
    accept_man = models.ForeignKey(User,models.CASCADE,related_name='accept_man',verbose_name='任務接受人',null = True)
    accept_time = models.DateField(auto_now_add=False,verbose_name='任務接受時間',null=True)
    photo = models.ImageField(upload_to='Award/%Y/%m/%d/', null=True, blank=True, verbose_name='懸賞任務')



    def __str__(self):
        return self.task_name


#工作任務
class WorkTask(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='worktask_assigner', verbose_name='任務發布者')
    task_name = models.CharField(max_length=32, verbose_name='任務名稱', null=True)
    task_content = RichTextField(verbose_name='任務內容', null=True)
    slug = RandomCharField(length=32, unique=True, unique_for_date='publish')
    publish = models.DateField(default=timezone.now, verbose_name='任務發布時間')
    point = models.IntegerField(default=0,verbose_name='獲得點數')
    photo = models.ImageField(upload_to='Award/%Y/%m/%d/', null=True, blank=True, verbose_name='懸賞任務')


    def getUrl(self):
        return reverse('app:accept_work_task', args=[self.id, self.slug])

    def __str__(self):
        return self.task_name

#我的工作任務
class MyWorkTask(models.Model):
    user = models.ForeignKey(UserProfile,on_delete=models.CASCADE,related_name='myworktask_accepter',verbose_name='任務接受者')
    task = models.ForeignKey(WorkTask,on_delete=models.CASCADE,related_name='myworktask',verbose_name='任務名稱')
    slug = RandomCharField(length=32, unique=True, unique_for_date='publish')
    date = models.DateField(auto_created=True,null=True)
    start_time = models.DateTimeField(auto_now_add=False,verbose_name='任務開始時間',null=True)
    end_time = models.DateTimeField(auto_now_add=False,verbose_name='任務結束時間',null=True)
    isfinish = models.BooleanField(default=False)
    point = models.IntegerField(default=0, verbose_name='獲得點數')

    def __str__(self):
        return  self.task.task_name


    def startCount(self):
        return reverse('app:worktask_start_count',args=[self.slug])

    def endCount(self):
        return reverse('app:worktask_end_count',args=[self.slug])

    def vaildation(self):
        return reverse('app:worktask_vaildation',args=[self.slug])


# 以下為行事曆
# 2020/12/31

class Event(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True,verbose_name='主題')
    description = models.TextField(verbose_name='描述')
    start_time = models.DateTimeField(verbose_name='開始時間')
    end_time = models.DateTimeField(verbose_name='結束時間')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('app:event-detail', args=(self.id,))

    @property
    def get_html_url(self):
        url = reverse('app:event-detail', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'


# 行事曆
class Calendars(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='calendar_owner',verbose_name='發起人')
    title = models.CharField(max_length=64, verbose_name='標題')
    content = RichTextField(verbose_name='說明')
    photo = models.ImageField(upload_to='calendars/%Y/%m/%d/', null=True, blank=True, verbose_name='照片')
    slug = RandomCharField(length=8, unique=True, unique_for_date='publish')
    start_time = models.DateTimeField(verbose_name='開始時間')
    end_time = models.DateTimeField(verbose_name='結束時間')
    publish = models.DateField(auto_now=True, verbose_name='發布日期')

    class Meta:
        ordering = ['-publish']

    def __str__(self):
        return f'{self.title}'


