from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

app_name = 'accounts'
urlpatterns = [
    path('accounts/signup/', signup_page, name='signup'),
    path('accounts/login/', login_page, name='login'),
    path('accounts/logout/', logout_view, name='logout'),
    path('', home, name='home'),
    path('dashboard/question-set/', question_set, name='question_set'),
    path('dashboard/question-set/view/', questions_set_list, name='question_set_view'),
    path('dashboard/add_question/', add_question, name='add_question'),
    path('dashboard/question_list/', question_list, name='question_list'),

    path('dashboard/add_question_options/', add_question_options, name='add_question_options'),
    path('dashboard/question_option_list/', question_option_list, name='question_option_list'),

    path('dashboard/exam_detail_page/<int:id>/<slug:slug>/', exam_detail_page, name='exam_detail_page'),


    path('dashboard/users/', users_list, name='users'),

]
