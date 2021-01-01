"""GoodVillages URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path,include
from django.contrib.auth import views as auth_views
from app import views

app_name='app'
urlpatterns = [
    path('', views.dashboard,name='dashboard'),
    path('edit/',views.edit, name = 'edit'),
    path('login/',auth_views.LoginView.as_view(),name='login'),
    path('logout/', auth_views.LogoutView.as_view(),{'next_page': '/'}, name='logout'),
    path('register/',views.register,name='register'),
    path('create_task/',views.create_task,name = 'create_task'),
    path('task_list/', views.task_list, name='task_list'),
    path('task_edit/<int:year>/<int:month>/<int:day>/<slug:task>/', views.task_edit, name='task_edit'), #編輯主任務
    path('sub_task_add/<int:year>/<int:month>/<int:day>/<slug:task>/', views.sub_task_add, name='sub_task_add'),  # 編輯主任務
    path('invalidTask/<int:year>/<int:month>/<int:day>/<slug:task>/<int:vaild>', views.invalidTask, name='invalidTask'),  # 任務失效
    path('invalidTask/<int:year>/<int:month>/<int:day>/<slug:task>/<int:vaild>', views.invalidTask, name='invalidTask'),  # 任務生效
    path('personal_task_add/', views.persontask_add, name='personal_task_add'),
    path('generate_qr_code/<int:id>/<slug:task>', views.generate_qr_code, name='generate_qr_code'),
    path('update_personal_task/<int:id>/<slug:task>', views.update_personal_task, name='update_personal_task'),
    path('scan_qrcode/', views.scan_qrcode, name='scan_qrcode'),
    path('my_personal_tasks/', views.my_personal_tasks, name='my_personal_tasks'),
    path('my_team_tasks_link/', views.my_team_tasks_link, name='my_team_tasks_link'),
    path('create_team_tasks/', views.my_team_tasks_link, name='create_team_tasks'),
    path('create_group/', views.create_group, name='create_group'),
    path('add_team_task/<int:user_id>/<int:group_id>',views.add_team_task,name='add_team_task'),
    path('manage_team_task/<int:task_id>/<int:group_id>/<int:user_id>/', views.manage_team_task, name='manage_team_task'),
    #懸賞任務
    path('manage_award_task/', views.manage_award_task, name='manage_award_task'),#懸賞主頁
    path('create_award_task',views.create_award_task, name= 'create_award_task'),# 發布任務
    path('release_award_task', views.release_award_task, name='release_award_task'),#管理者approve 任務
    path('approve_award_task/<int:award_task_id>', views.approve_award_task, name='approve_award_task'),
    path('accept_award_task/<int:award_task_id>/<int:user_id>', views.accept_award_task, name='accept_award_task'),#接受任務
    path('depoly_award_task/', views.depoly_award_task, name='depoly_award_task'),
    path('my_award_task/<int:user_id>',views.my_award_task,name = 'my_award_task'),#我的任務
    #工作任務
    path('manage_work_task/',views.manage_work_task,name ='manage_work_task'),
    path('create_work_task/', views.create_work_task, name='create_work_task'),
    path('accept_work_task/<int:task_id>/<slug:task>', views.accept_work_task, name='accept_work_task'),
    path('worktask_start_count/<slug:task>',views.worktask_start_count,name='worktask_start_count'),
    path('worktask_end_count/<slug:task>',views.worktask_end_count,name='worktask_end_count'),
    path('worktask_vaildation/<slug:task>', views.worktask_vaildation, name='worktask_vaildation'),

    #個人點數
    path('manage_account_value/', views.manage_account_value, name='manage_account_value'),
    path('account_list/<int:id>/<slug:account_slug>',views.account_list,name='account_list'),
    #個人行事曆
    path('', views.CalendarView.as_view(), name='calendar'),
    path('event/<int:event_id>/details/', views.event_details, name='event-detail'),
    path('event/new/', views.create_event, name='event_new'),
    path('event/edit/<int:pk>/', views.EventEdit.as_view(), name='event_edit'),

    #園區行事曆
    path('manage_calendar/',views.manage_calendar,name='manage_calendar')


]
