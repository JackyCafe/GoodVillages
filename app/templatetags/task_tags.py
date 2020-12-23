from django import template
from  ..models import PersonalTask
register = template.Library()


@register.simple_tag
def total_task():

    return PersonalTask.personalTask.count()


@register.inclusion_tag('account/person_task.html')
def show_personal_tasks(request):
    user = request.user.id
    tasks =  PersonalTask.personalTask.filter(user=user)
    return {'tasks':tasks}


@register.filter('get_value_from_dict')
def get_value_from_dict(dict_data, key):
    """
    usage example {{ your_dict|get_value_from_dict:your_key }}
    """
    if key:
        return dict_data.get(key)