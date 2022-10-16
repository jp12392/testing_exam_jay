from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from accounts.decorators import unauthenticated_user

from accounts.forms import *
from django.utils import timezone

from accounts.models import QuestionSet
from accounts.serialziers import QuestionSetSerializer
User = get_user_model()




### signup_page
@unauthenticated_user
def signup_page(request):
    form = RegistrationForm()
    
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'You have registered successfully. Please login here.')
            return redirect(settings.LOGIN_URL)
        else:
            if form.errors:
                for field in form:
                    for error in field.errors:
                        messages.error(request, error)
            form = RegistrationForm(request.POST)

            
    context = {'title': 'Register', 'form':form}
    return render(request, 'accounts/register.html', context)
    

### Login Page.
@unauthenticated_user
def login_page(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            now = timezone.now()
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # print('user', user)
                login(request, user)
               
                return redirect(settings.LOGIN_REDIRECT_URL)  # change expected_url in your project
            else:
                messages.error(request, 'Incorrect email or password')
        elif form.errors:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    context = {'title': 'Login','form':form}
    return render(request, 'accounts/login.html', context)


## logout_view
def logout_view(request):
    logout(request)
    return redirect(settings.LOGOUT_REDIRECT_URL)

### Dashboard Page
@login_required
def home(request):
    user_count = User.objects.filter(roles_id=2).count()
    qs_set = QuestionSet.objects.count()
    question_count = Question.objects.count()
    qs_option = QuestionOptions.objects.count()

    question_set_list = QuestionSet.objects.all()
    context = {'title': 'Admin','user_count':user_count,'qs_set':qs_set,'question_count':question_count,'qs_option':qs_option,'question_set_list':question_set_list}
    return render(request, 'accounts/dashboard/index.html', context)


## Question Set Views.
@login_required
def question_set(request):
    if request.user.roles.role != 'Admin':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
        
        
    form = QuestionSetForm()
    if request.method == 'POST':
        form = QuestionSetForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record has been added successfully.')
            return redirect('/dashboard/question-set/')

        elif form.errors:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    context = {'title': 'Question Set','form':form}
    return render(request, 'accounts/questionset/index.html', context)

@login_required
def questions_set_list(request):
    if request.user.roles.role != 'Admin':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)

    question_set = QuestionSet.objects.all()
    print('question_set', question_set)
    context = {'title': 'Question Set List','question_set':question_set}
    return render(request, 'accounts/questionset/view.html', context)

@login_required
def add_question(request):
    if request.user.roles.role != 'Admin':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)

    form = QuestionForm()
    if request.method == 'POST':
        form = QuestionForm(request.POST, request.FILES)

        # print('form', form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question has been added successfully.')
            return redirect('/dashboard/add_question/')

        elif form.errors:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    context = {'title': 'Add New Questions','form':form}
    return render(request, 'accounts/questions/index.html', context)

@login_required
def question_list(request):
    if request.user.roles.role != 'Admin':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)

    question = Question.objects.all()
    print('question', question)
    context = {'title': 'Question List','question':question}
    return render(request, 'accounts/questions/view.html', context)

#### Add Question Options #####.
@login_required
def add_question_options(request):
    if request.user.roles.role != 'Admin':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)

    form = QuestionOptionsForm()
    if request.method == 'POST':
        form = QuestionOptionsForm(request.POST, request.FILES)

        # print('form', form)
        if form.is_valid():
            form.save()
            messages.success(request, 'Question option has been added successfully.')
            return redirect('/dashboard/add_question_options/')

        elif form.errors:
            for field in form:
                for error in field.errors:
                    messages.error(request, error)

    context = {'title': 'Add New Questions Option','form':form}
    return render(request, 'accounts/question_options/add.html', context)

@login_required
def question_option_list(request):
    if request.user.roles.role != 'Admin':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)

    options_list = QuestionOptions.objects.all()
    context = {'title': 'Question Option List','options_list':options_list}
    return render(request, 'accounts/question_options/view.html', context)


### Exam Detail Page SHow All Question List Options.
@login_required
def exam_detail_page(request, id, slug):
    if request.method == 'POST':
        return redirect('/')
        

    question_set_check = QuestionSet.objects.filter(id=id, slug=slug).last()
    if question_set_check:
        serializer = QuestionSetSerializer(question_set_check, many=False)

        print('>>>>>>>>>', serializer.data)
        context = {'title': 'Exam Detail Page','data':serializer.data}
        return render(request, 'accounts/exam/index.html', context)
    else:
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
    
### User Management Start Here.
@login_required
def users_list(request):
    if request.user.roles.role != 'Admin':
        logout(request)
        return redirect(settings.LOGOUT_REDIRECT_URL)
        
    users = User.objects.filter(roles_id=2)
    context = {'title': 'Users List','users':users}
    return render(request, 'accounts/users/index.html', context)



    
    