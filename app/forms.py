from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, DateInput
from django.utils.datastructures import MultiValueDict

from app.models import UserProfile, Task, SubTask, PersonalTask, TeamTask, Group, MyAwardTask, WorkTask, Account, Event, \
    Calendar


# Login
class LoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


# 使用者註冊
class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='輸入密碼', widget=forms.PasswordInput)
    password2 = forms.CharField(label='再次輸入密碼', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)



    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError("Password don't match ")
            return cd['password2']
            # return cd['password2']


# 修改基本資料
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


# 修改Profile
class ProfileEditForm(forms.ModelForm):
    authority = forms.ChoiceField(choices=UserProfile.AUTHORITY_CHOICE, label='身分')

    class Meta:
        model = UserProfile
        fields = ('actual_name', 'authority', 'photo')


# 創任務
class TaskForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
        task = super(TaskForm, self).save(commit=False)
        task.task_name = self.cleaned_data['task_name']
        task.task_content = self.cleaned_data['task_content']
        task.publish = self.cleaned_data['publish']
        task.task_type = self.cleaned_data['task_type']

        if commit:
            task.save()
        return task


    class Meta:
        model = Task
        fields = '__all__'


# 子任務
class SubTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubTaskForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = SubTask
        fields = '__all__'


class PersonalTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonalTaskForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = PersonalTask
        fields = '__all__'


#建立群組任務
class CreateTeamTaskForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):

        super(CreateTeamTaskForm,self).__init__(*args,**kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
        model = TeamTask
        fields = '__all__'


#開群組
class CreateGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial", {})
        userprofile = initial.get('userprofile')
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['owner'].initial = userprofile

    class Meta:
        model = Group
        fields = '__all__'


class MyAwardTaskForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        initial = kwargs.get("initial",{})
        user = initial.get('user')
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['user'].initial = user
        self.fields['user'].widget.attrs['disable'] = True
        # self.fields['approve_man'].initial = approve_man
        # self.fields['accept_man'].initial = accept_man

    class Meta:
        model = MyAwardTask
        fields = ('user','task_name','task_content','publish','point')


#定義工作任務
class WorkTaskForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        initial = kwargs.get("initial",{})
        user = initial.get('userprofile')
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['user'].initial = user

    class Meta:
        model = WorkTask
        fields = '__all__'


class AccountForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        initial = kwargs.get("initial",{})
        user = initial.get('userprofile')
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        self.fields['processor'].initial = user

    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['withdraw']


#20201231 以下為行事曆
class EventForm(ModelForm):
  class Meta:
    model = Event
    # datetime-local is a HTML5 input type, format to make date time show on fields
    widgets = {
      'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
      'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
    }
    exclude = ['user']

  def __init__(self, *args, **kwargs):
    super(EventForm, self).__init__(*args, **kwargs)
    # input_formats to parse HTML5 datetime-local input to datetime field
    self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
    self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)


#2021/01/01
class CalendarForm(ModelForm):
    def __init__(self, *args, **kwargs):
        initial = kwargs.get("initial", {})
        user = initial.get('userprofile')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Calendar
        # datetime-local is a HTML5 input type, format to make date time show on fields
        widgets = {
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        exclude = ['user']