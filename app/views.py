from datetime import datetime,date, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views import generic
from app.forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, TaskForm, SubTaskForm, \
    PersonalTaskForm, CreateTeamTaskForm, CreateGroupForm, MyAwardTaskForm, WorkTaskForm, AccountForm, EventForm
from app.models import UserProfile, Task, SubTask, PersonalTask, TeamTask, Group, MyTeamTask, MyAwardTask, WorkTask, \
    MyWorkTask, Account, Event
import random
import logging
import calendar


# from .utils import Calendar
from app.utils import Calendar

logger = logging.getLogger(__name__)
log = logger.info
stherr = 'Something Err.'
today = datetime.today().date()


def index(request):
    return render(request, 'account/index.html')


###
# 首頁
#
@login_required
def dashboard(request):
    authority = request.user.userprofile.authority
    request.session['authority'] = authority
    request.session['user'] = request.user.id
    user_id = request.user.id

    personal_tasks = PersonalTask.objects.filter(user=user_id).filter(assign_date=datetime.today().date())

    # 今天沒有每日任務
    # 今天 如果沒有 每日任務，由系統產生一個
    #
    if personal_tasks.count() == 0:
        tasks = Task.objects.filter(is_vaild=True).all()
        logger.info(tasks.count())

    d = get_date(request.GET.get('month', None))
    cal = Calendar(d.year, d.month)
    html_cal = cal.formatmonth(user_id=user_id,withyear=True)
    context = {
    'section': 'dashboard',
     'authority': authority,
     'personal_tasks': personal_tasks,
     'calendar': html_cal,
     'prev_month':  prev_month(d),
     'next_month':next_month(d)
     }



    return render(request,
                  'account/dashboard.html',
                   context

                  )


# 處理user 登入介面
def user_login(request):
    form: LoginForm()
    user: User
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                username=cd['username'],
                                password=cd['password']
                                )
            if user is not None:
                if user.is_active:
                    login(request, user)
                    authority = user.userprofile.authority
                    return HttpResponse("登入")
                    # return render(request, 'account/register.html', {'form': form, 'authority': authority})
            else:
                return HttpResponse("帳號不存在")

    else:
        form = LoginForm()
        return render(request, 'account/login.html', {'form': form})


def register(request):
    user_form: UserRegistrationForm
    profile_form: ProfileEditForm  # profile form
    new_user: User
    user_profile: UserProfile  # profile instance

    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileEditForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():

            new_user = user_form.save()  # 產生user instance
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()  # 儲存密碼
            user_profile = profile_form.save(commit=False)  # 產生profile 實體
            user_profile.user = new_user
            profile_form.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            return render(request, 'account/register_done.html', {'new_user': new_user})
        else:
            return HttpResponse("兩次密碼不一致")  # 兩次密碼不一致
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileEditForm()
        return render(request, 'account/register.html',
                      {'user_form': user_form,
                       'profile': profile_form})


@login_required
def edit(request):
    user_form: UserEditForm
    profile_form: ProfileEditForm

    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.userprofile,
                                       data=request.POST,
                                       files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.userprofile)
        return render(request, 'account/edit.html', {'user_form': user_form,
                                                     'profile_form': profile_form})


# 創建任務
def create_task(request):
    task_form: TaskForm
    new_task: Task
    if request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            new_task = task_form.save()
            return redirect('app:task_list')
    else:
        task_form = TaskForm()
        return render(request, 'account/create_task.html', {'task_form': task_form})


# 任務列表
def task_list(request):
    task_form: TaskForm
    tasks_list = Task.objects.all()
    paginator = Paginator(tasks_list, 10)  # 每頁10筆
    page = request.GET.get('page')
    try:
        tasks = paginator.page(page)
    except PageNotAnInteger:
        tasks = paginator.page(1)
    except EmptyPage:
        tasks = paginator.page(paginator.num_pages)
    return render(request, 'account/task_list.html', {'page': page, 'tasks': tasks})


# 編輯主任務
def task_edit(request, year, month, day, task):
    task = get_object_or_404(Task, slug=task, publish__year=year,
                             publish__month=month,
                             publish__day=day)
    task_form: TaskForm
    task: Task
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=task)
        if task_form.is_valid():
            task = task_form.save()
            return redirect(reverse('app:task_list'))

    else:
        task_form = TaskForm(instance=task)
        return render(
            request, 'account/task_edit.html', {'task_form': task_form}
        )


# 新增個人任務，
def persontask_add(request):
    person_task_form: PersonalTaskForm
    person_task: PersonalTask
    if request.method == 'POST':
        person_task_form = PersonalTaskForm(request.POST)
        if person_task_form.is_valid():
            person_task = person_task_form.save()
            tasks = PersonalTask.objects.all()
            return render(request, 'account/person_task.html', {'tasks': tasks})
        else:
            return HttpResponse(stherr)
    else:
        person_task_form = PersonalTaskForm()
        context = {'person_task_form': person_task_form}
        return render(request, 'account/person_task_add.html', context)


# 新增次要任務
def sub_task_add(request, year, month, day, task):
    task = get_object_or_404(Task, slug=task, publish__year=year,
                             publish__month=month,
                             publish__day=day)
    sub_task_form: SubTaskForm
    sub_task: SubTask
    if request.method == 'POST':
        sub_task_form = SubTaskForm(request.POST)
        sub_task = sub_task_form.save(commit=False)
        sub_task.task = task
        sub_task.save()
        return HttpResponseRedirect(reverse('app:manage_award_task'))

    else:
        sub_task_form = SubTaskForm()
        return render(request, 'account/sub_task_form.html', {'sub_task_form': sub_task_form})


# 任務生效或失效
def invalidTask(request, year, month, day, task, vaild):
    task = get_object_or_404(Task, slug=task, publish__year=year,
                             publish__month=month,
                             publish__day=day)
    task.is_vaild = vaild
    task.save()
    return redirect(reverse('app:task_list'))


# 產生QR_CODE
def generate_qr_code(request, id, task):
    tasks = get_object_or_404(PersonalTask, id=id, slug=task)
    site = str(get_current_site(request))
    url = 'http://' + site + tasks.update_personal_task()
    return render(request, 'account/person_task_qr_code.html', {'tasks': tasks, 'url': url})


# 掃QR_CODE 網址，認證工作達成
#
def update_personal_task(request, id, task):

    tasks = get_object_or_404(PersonalTask, id=id, slug=task)
    tasks.finish_date = datetime.today().date()
    tasks.save()
    return HttpResponse(task)


# 工作人員掃描QR_CODE的工具程式
# todo html5 scan qrcode wait process
def scan_qrcode(request):
    return render(request, 'account/scan_qr_code.html')


# 我的個人任務
# 抓取personal_task 中
# .filter(finish_date__isnull=False) \
#     .filter(is_award=False)　
# 同一天累積多項，個人任務只算一次
# 發布每日任務
def my_personal_tasks(request):
    user_id = request.session.get('user')
    authority = request.user.userprofile.authority
    request.session['authority'] = authority
    request.session['user'] = request.user.id
    user = request.user

    personal_tasks = PersonalTask.objects.filter(user=user_id).filter(assign_date=datetime.today().date())

    # 今天沒有每日任務
    # 今天 如果沒有 每日任務，由系統產生一個
    #
    if personal_tasks.count() == 0:
        tasks = Task.objects.filter(is_vaild=True).all()
        logger.info(tasks.count())
        count = tasks.count()
        ids = []
        i = 0
        #  隨機挑選不重複的每日任務
        while i < 3:
            id = random.randint(1, count - 1)
            if id not in ids:
                ids.append(id)
                task = Task.objects.get(id=id)
                personal_task = PersonalTask()
                personal_task.user = request.user.userprofile
                personal_task.task = task
                personal_task.point = task.point
                personal_task.save()
                i = i + 1
        personal_tasks = PersonalTask.objects.filter(user=user.userprofile).filter(assign_date=datetime.today().date())

    finish_date = []
    points = 0
    #計算點數，完成工作所得點數
    person_tasks = list(PersonalTask.objects.filter(finish_date=datetime.today()).filter(user = user_id).values())
    for person_task in person_tasks:
        points += int(person_task['point'])
        if person_task['finish_date'] not in finish_date:
            finish_date.append(person_task['finish_date']) #秀點數

    #點數轉入個人帳戶.
    ptasks = list(PersonalTask.personal_task_award.filter(is_award=False).filter(user = user_id).values())
    for pt in ptasks:
        task_id = person_task['id']
        # 把personal is_award update 為True
        task = PersonalTask.objects.get(id=task_id)
        task.is_award = True
        task.save()
        #新增至個人帳號
        account = Account.objects.create(user = user.userprofile,deposit=int(person_task['point']),transaction_date=datetime.now(),
                                         transaction_memo='工作任務')
        account.save()

    context = {'finish_task_date': len(finish_date), 'points': points,
               'section': 'dashboard',
               'authority': authority,
               'personal_tasks': personal_tasks}

    return render(request,
                  'account/my_personal_task.html', context

                  )


def my_team_tasks_link(request):
    user_id = request.session.get('user')
    team_tasks = TeamTask.objects.filter(end_date__gte=today)

    task_list = []
    # task : 目前未結案的團隊任務
    for task in team_tasks:
        group_ids = task.group_set.values().filter(is_active=True)
        task_name = task.task_name
        task_id = task.id
        group_list = []
        for group_set in group_ids:
            users = []
            group_name = group_set['group_name']
            id = group_set['id']
            group = Group.objects.get(id=id)
            _ids = Group.objects.filter(id=id).values('group__user_id')
            for _id in _ids:
                user = User.objects.filter(id=_id['group__user_id']).values('userprofile__actual_name')[0]
                users.append(user['userprofile__actual_name'])
            result_set = {'group': group_name, 'group_id': id, 'users': users}
            group_list.append(result_set)
        task_set = {'task_name': task_name, 'task_id': task_id, 'group_list': group_list}
        task_list.append(task_set)

    context = {'user_id': user_id, 'tasks': task_list}
    return render(request, 'account/my_team_task.html', context)


# #我的團隊任務
# def my_team_tasks_link(request):
#     user_id = request.session.get('user')
#     team_tasks = TeamTask.objects.filter(end_date__gte=today)
#
#     task_list=[]
#     # task : 目前未結案的團隊任務
#     for task in team_tasks:
#         group_ids = task.group_set.values().filter(is_active=True)
#         task_name = task.task_name
#
#         group_list = []
#         for group_set in group_ids:
#             users = []
#             group_name = group_set['group_name']
#             id = group_set['id']
#             group = Group.objects.get(id=id)
#
#             # 經由through 找到foregin key
#             # group.group.through.objects.filter(group_id=id) ==>找到對應的table my_teamtask_group
#             # ...filter(group_id=id).values('myteamtask_id') ==>找到對應的myteamtask_id key值
#             myteamtask_ids = group.group.through.objects.filter(group_id=id).values('myteamtask_id')
#             for myteamtask_id in myteamtask_ids:
#                 # logger.info(myteamtask_id)
#                 user = MyTeamTask.objects.get(id = myteamtask_id.get('myteamtask_id')).user.userprofile.actual_name
#                 users.append(user)
#             result_set={'group':group_name,'group_id':id,'users':users}
#             group_list.append(result_set)
#         # logger.info(group_list)
#         task_set={'task_name':task_name,'group_list':group_list}
#         task_list.append(task_set)
#     logger.info(task_list)
#     context = {'user_id':user_id,'tasks':task_list}
#     return render(request,'account/my_team_task.html',context)


# user 點選我要加入
# user_id -->request.session
# group_id --> myteamtask_id

def add_team_task(request, user_id, group_id):
    user = User.objects.get(id=user_id)
    my_team_tasks = MyTeamTask.objects.filter(user_id=user_id)
    task_id = my_team_tasks.values('group__task_id')
    group_names = my_team_tasks.values('group__group_name')
    group_set = my_team_tasks.values('group__id')
    group_ids = []
    for group in group_set:
        group_ids.append(group['group__id'])

    team_task_ids = my_team_tasks.values('id')
    # log(team_task_ids)

    # if QuerySet:[]
    # -->create new_team_task ,
    # -->Create new_group_record,
    # t1(through).save
    if not my_team_tasks:
        new_team_tasks = MyTeamTask.objects.create(user_id=user_id, point=0, is_award=0)
        new_team_tasks.save()
        new_group = Group.objects.get(id=group_id)
        t1 = new_team_tasks.group.through.objects.create(myteamtask=new_team_tasks, group=new_group)
        t1.save()
        message = '已新增'
        logger.info('已新增')
    elif group_id not in group_ids:
        new_team_tasks = MyTeamTask.objects.create(user_id=user_id, point=0, is_award=0)
        new_team_tasks.save()
        new_group = Group.objects.get(id=group_id)
        t1 = new_team_tasks.group.through.objects.create(myteamtask=new_team_tasks, group=new_group)
        t1.save()
        message = '已新增'
        logger.info('已新增')
    else:
        log('已在群組中')

    return redirect('app:my_team_tasks_link')


# 我要組隊
def create_group(request):
    group_form: CreateGroupForm()
    user_id = request.session.get('user')
    group = Group()
    if request.method == 'POST':
        group_form = CreateGroupForm(request.POST)
        if group_form.is_valid():
            group = group_form.save()
            new_team_tasks = MyTeamTask.objects.create(user_id=user_id, point=0, is_award=0)
            new_team_tasks.save()
            t1 = new_team_tasks.group.through.objects.create(myteamtask=new_team_tasks, group=group)
            t1.save()
            return redirect('app:my_team_tasks_link')
    else:
        user = User.objects.get(id=user_id)
        userprofile = user.userprofile
        group_form = CreateGroupForm(initial={'userprofile': userprofile})
    return render(request, 'account/create_group.html', {'group_form': group_form})


def manage_team_task(request, task_id, group_id, user_id):
    tasks = TeamTask.objects.filter(id=task_id).all()
    group = Group.objects.filter(id=group_id)
    ids = group.values('group__user_id')
    users = []
    for id in ids:
        useranme = User.objects.get(id=id['group__user_id']).userprofile
        users.append(useranme)

    context = {'tasks': tasks, 'group_id': group_id, 'user_id': user_id, 'users': users}
    return render(request, 'account/manage_group.html', context)


def manage_award_task(request):
    # wait_release_tasks =  MyAwardTask.objects.filter(approve_man_id__isnull=False).all()
    wait_release_tasks =  MyAwardTask.objects.filter(approve_man_id__isnull=True).all()
    wait_accept_tasks = MyAwardTask.objects.filter(approve_man_id__isnull=False).filter(accept_man__isnull=True)
    accept_tasks = MyAwardTask.objects.filter(approve_man_id__isnull=False).filter(accept_man__isnull=False)
    context = {'wait_release_tasks':wait_release_tasks,'wait_accept_tasks':wait_accept_tasks,'accept_tasks':accept_tasks}
    return render(request, 'account/manage_award_task.html', context)


# 　20201208 由住民發布懸賞任務
# 　只有approve_man　欄位不是空白的情境下才允許陳列在工作列表中
def create_award_task(request):
    user_id = request.session.get('user')
    award_form: MyAwardTaskForm()
    if request.method == 'POST':
        award_form = MyAwardTaskForm(request.POST)
        if award_form.is_valid():
            cd = award_form.cleaned_data
            mytask = MyAwardTask.objects.create(**cd)
            mytask.user = UserProfile.objects.get(id=user_id)
            mytask.save()
            tasks = MyAwardTask.objects.filter(approve_man_id__isnull=True).all()
            context = {'tasks': tasks}
            return redirect(reverse('app:manage_award_task'))

            # return render(request, 'account/manage_award_task.html', context)
    else:
        user = User.objects.get(id=user_id)
        userprofile = user.userprofile
        award_form = MyAwardTaskForm(initial={'user': userprofile})
        context = {'award_form': award_form}

    return render(request, 'account/create_award_task.html', context)


#在base.html 中尋找可由管理者、照服員release　的懸賞任務
def release_award_task(request):
    #待核可懸賞任務
    wait_release_tasks =  MyAwardTask.objects.filter(approve_man_id__isnull=True).all()
    #
    wait_accept_tasks = MyAwardTask.objects.filter(approve_man_id__isnull=False).filter(accept_man__isnull=True)
    context = {'wait_release_tasks':wait_release_tasks,'wait_accept_tasks':wait_accept_tasks}
    return render(request,'account/release_award_lists.html',context)


def approve_award_task(request,award_task_id):
    # 登入的人的id
    user_id = request.session.get('user')
    user = User.objects.get(id = user_id)
    task :MyAwardTask = MyAwardTask.objects.get(id = award_task_id)
    task.approve_man = user
    task.approve_time = datetime.now()
    task.save()
    wait_release_tasks = MyAwardTask.objects.filter(approve_man_id__isnull=True).all()
    wait_accept_tasks = MyAwardTask.objects.filter(approve_man_id__isnull=False).filter(accept_man__isnull=True).all()

    context = {'wait_release_tasks': wait_release_tasks, 'wait_accept_tasks': wait_accept_tasks}
    return render(request, 'account/release_award_lists.html', context)


#接受懸賞任務
def accept_award_task(request,award_task_id,user_id):
    user = User.objects.get(id = user_id)
    #從MyAwardTask 中找出approve_man不為空的
    task: MyAwardTask = MyAwardTask.objects.filter(approve_man_id__isnull=False).all().get(id=award_task_id)
    if not task :
       return  HttpResponse('未經授權')
    task.accept_man = user
    task.accept_time = datetime.now()
    task.save()
    wait_release_tasks = MyAwardTask.objects.filter(approve_man_id__isnull=True).all()
    wait_accept_tasks = MyAwardTask.objects.filter(approve_man_id__isnull=False).filter(accept_man__isnull=True).all()
    context = {'wait_release_tasks': wait_release_tasks, 'wait_accept_tasks': wait_accept_tasks}
    return render(request, 'account/manage_award_task.html', context)


# 已所有發布任務
def depoly_award_task(request):
    tasks: MyAwardTask = MyAwardTask.objects.filter(approve_man_id__isnull=False).all()
    context = {'tasks': tasks }
    log(context)
    return render(request, 'account/my_award_task.html', context)

    # return render(request, 'account/depoly_award_task.html', context)


#我的任務，含我發布的任務及我接收的任務
def my_award_task(request,user_id):
    my_depoly_tasks = MyAwardTask.objects.filter(user_id = user_id)
    my_accept_tasks = MyAwardTask.objects.filter(accept_man_id=user_id)
    context={'my_depoly_tasks':my_depoly_tasks,'my_accept_tasks':my_accept_tasks}
    return render(request, 'account/my_award_task.html', context)


def manage_work_task(request):
    tasks = WorkTask.objects.all()
    context = {'tasks': tasks}
    return render(request, 'account/manage_work_task.html', context)



def create_work_task(request):
    user_id = request.session.get('user')
    work_form : WorkTaskForm()
    if request.method == 'POST':
        work_form = WorkTaskForm(request.POST)
        work_form.save()
        return redirect(reverse('app:manage_work_task'))
    else:
        user = User.objects.get(id=user_id)
        userprofile = user.userprofile
        worktask_form = WorkTaskForm(initial={'userprofile': userprofile})
        context = {'worktask_form':worktask_form}
    return render(request,'account/create_work_task.html',context)


def accept_work_task(request,task_id,task):
    user_id = request.session.get('user')
    tasks = get_object_or_404(WorkTask,id=task_id, slug=task)
    user = UserProfile.objects.get(id = user_id)

    date = datetime.now()
    worktasks,created = MyWorkTask.objects.get_or_create(user_id=user_id,task_id=task_id
                                                         ,isfinish =False
                                                         )
    log(created)
    if created :
       worktasks.date =date
       worktasks.save()

    context = {'worktasks':worktasks}
    return render(request, 'account/accept_worktask.html',context)


def worktask_start_count(request,task):
    worktasks = get_object_or_404(MyWorkTask,slug=task)
    worktasks.start_time = datetime.now()
    worktasks.save()
    context = {'worktasks': worktasks}
    return render(request, 'account/accept_worktask.html',context)


def worktask_end_count(request,task):
    worktasks = get_object_or_404(MyWorkTask, slug=task)
    worktasks.end_time = datetime.now()
    worktasks.isfinish =True
    worktasks.save()
    log(worktasks.end_time)
    log(worktasks.start_time)
    diff_time = (worktasks.end_time-worktasks.start_time)
    hours,remainer = divmod(diff_time.total_seconds(),3600)
    minutes,seconds = divmod(remainer,60)
    total_time = f'{int(hours)} 小時 {int(minutes)} 分'
    context = {'worktasks': worktasks,'total_time':total_time}
    return render(request, 'account/accept_worktask.html', context)


def worktask_vaildation(request,task):
    worktasks = get_object_or_404(MyWorkTask, slug=task)
    worktasks.isfinish =True
    worktasks.save()
    context = {'worktasks': worktasks}
    return render(request, 'account/accept_worktask.html', context)


def account_list(request,id,account_slug):
    accounts = get_object_or_404(Account,id=id,slug=account_slug)
    context = {'accounts':accounts}
    return render(request,'account/account_value_list.html',context)




def manage_account_value(request):
    accountForm: AccountForm
    user_id = request.session.get('user')

    if request.method =='POST':
        accountForm = AccountForm(request.POST)
        if accountForm.is_valid():
            cd = accountForm.cleaned_data
            account = Account.objects.create(**cd)
            account.processor = UserProfile.objects.get(id=user_id)
            account.save()
            return redirect(account.get_account_url(),id=account.id,slug=account.slug)
    else:
        user = User.objects.get(id=user_id)
        userprofile = user.userprofile
        accountForm =  AccountForm(initial={'userprofile': userprofile})
        context = {'accountForm':accountForm}
    return render(request, 'account/create_account_value.html',context)

#2020/12/31 以下為行事曆
def get_date(req_day):
    if req_day:
        year, month = (int(x) for x in req_day.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

#CalendarView

class CalendarView(LoginRequiredMixin, generic.ListView):
    login_url = 'signup'
    model = Event
    template_name = 'calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

@login_required(login_url='signup')
def create_event(request):
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data['title']
        description = form.cleaned_data['description']
        start_time = form.cleaned_data['start_time']
        end_time = form.cleaned_data['end_time']
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time
        )
        return HttpResponseRedirect(reverse('app:calendar'))
    return render(request, 'event.html', {'form': form})


class EventEdit(generic.UpdateView):
    model = Event
    fields = ['title', 'description', 'start_time', 'end_time']
    template_name = 'event.html'

@login_required(login_url='signup')
def event_details(request, event_id):
    event = Event.objects.get(id=event_id)
    # eventmember = EventMember.objects.filter(event=event)
    context = {
        'event': event,
        # 'eventmember': eventmember
    }
    return render(request, 'account/event-details.html', context)


def manage_calendar(request):



    return None


