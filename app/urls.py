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
    path('manage_award_task/', views.manage_award_task, name='manage_award_task'),
    path('create_award_task',views.create_award_task, name= 'create_award_task'),
    path('release_award_task', views.release_award_task, name='release_award_task'),
    path('approve_award_task/<int:award_task_id>', views.approve_award_task, name='approve_award_task'),
    path('accept_award_task/<int:award_task_id>/<int:user_id>', views.accept_award_task, name='accept_award_task'),
    path('depoly_award_task/', views.depoly_award_task, name='depoly_award_task'),
    path('my_award_task/<int:user_id>',views.my_award_task,name = 'my_award_task'),
    path('manage_work_task/',views.manage_work_task,name ='manage_work_task'),
    path('create_work_task/', views.create_work_task, name='create_work_task'),
    path('accept_work_task/<int:task_id>/<slug:task>', views.accept_work_task, name='accept_work_task'),

]
