from typing import List
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from course_mgt import Course
from .models import Users 


def Courses(request):
    template = "course/courses.html"

    course_obj = Course()

    courses = course_obj.get_courses()

    for course_id in range(len(courses)):
        courses[course_id]['sessions'] = course_obj.courses_course_id_course_sessions(courses[course_id].get('id'))

    context = {
        "courses": courses,       
    }

    return render(request, template, context)


def Course_id(request, id):
    template = "course/course.html"

    error = ''

    course_obj = Course()
    
    course = course_obj.get_course_id(id)
    course['sessions'] = course_obj.courses_course_id_course_sessions(course.get('id'))

    if request.user.is_authenticated:
        users = Users.objects.get(user_id=request.user.id)

        if request.method == 'POST': 

            unsign = request.POST.get('unsign')
            
            if unsign:
                error = course_obj.course_sessions_delete(request.POST.get('session_id'), users.user_id_teachbase)

                if not error.get('errors'):
                    error = ''

            else:
                error = register_user_in_session(request, course_obj)

        session_register_list = get_registred_sessions_user(course.get('id'), users.user_id_teachbase, course_obj)

        for session_register in session_register_list:
            for session_id in range(len(course['sessions'])):
                if course['sessions'][session_id].get('id') == session_register:
                    course['sessions'][session_id]['is_registred'] = True

    else:
        if request.method == 'POST': 
            error = 'Для записи необходимо авторизоваться!'


    context = {
        "course": course,  
        'error': error,   
    }

    return render(request, template, context)


def get_registred_sessions_user(course_id, user_id_teachbase, course_obj=None):

    if not course_obj:
        course_obj = Course()

    sessions = course_obj.courses_course_id_course_sessions(course_id)
    sessions_user = [course_obj.course_sessions_id_listeners_user_id(session.get('id'), user_id_teachbase) for session in sessions] 

    if type(sessions_user) == type({}):
        return []
    
    return [session.get('course_session_id') for session in sessions_user]


def register_user_in_session(request, course_obj=None):

    if not course_obj:
        course_obj = Course()

    session_id = request.POST.get('session_id')
    
    users = Users.objects.get(user_id=request.user.id)

    register = course_obj.course_sessions_register(sessions_id=session_id, user_id=users.user_id_teachbase, email=users.email, phone=users.phone)

    return_register = register.get('errors')

    if return_register == ['Пользователь уже участвует в событии']:
        return 'Вы уже записались на сессию!' 
    
    return ''


def Logout(request):
    ''' Для выхода и возвращения на ту же страницу '''
    
    if request.user.is_authenticated:
        logout(request)

    request_url = request.META.get('HTTP_REFERER')
    if not request_url:
        request_url = 'Courses'
      
    return redirect(request_url)


def Login(request):
    ''' Для входа и возвращения на ту же страницу '''

    error = ''

    if request.user.is_authenticated:
        return redirect('Courses')

    if request.method == 'POST':     
       

        form = request.POST

        login_f = form.get('login')
        password = form.get('password')
        
        user_auth = authenticate(username=login_f, password=password)
        if user_auth is not None:
            login(request, user_auth)
        else:
            error = 'Логин и пароль не подходят'

        request_url = request.META.get('HTTP_REFERER')
        if not request_url:
            request_url = 'Courses'

        if error == '':
            return redirect(request.META.get('HTTP_REFERER'))
      
    template = "account/login.html"

    return render(request, template, {'error': error})


def Register(request):
    ''' Создаём пользователя и у нас и по АПИ '''
    error = ''

    if request.user.is_authenticated:
        error = 'Для создания пользователя выйдите из текущего профиля!'

    if request.method == 'POST':         
        form = request.POST

        email = form.get('email')
        user_name = form.get('user')
        name = form.get('name')
        last_name = form.get('last_name')
        description = form.get('description')
        phone = form.get('phone')
        password = form.get('password')
        
        users_dict = {
            'email': email,
            'user': user_name,
            'name': name,
            'last_name': last_name,
            'description': description,
            'phone': phone,
            'password': password,
        }
        
        user_create = Create_user(request, users_dict)

        error = user_create.get('error', '')
        if error != '' :
            print(error)
        else:
            return redirect('Courses')
   
    template = "account/register.html"

    return render(request, template, {'error': error})


def Create_user(request, users_dict):

    # если мы уже в аккаунте, то ничего не надо делать
    if request.user.is_authenticated:
        return {'error' : 'Для создания юзера, необходима выйти из аккаунта!'}
    
    # пытаемся создать юзера на нашей стороне 
    user = User.objects.create_user(username=users_dict.get('user'),
                email=users_dict.get('email'),
                password=users_dict.get('password'))
    
    users_dict['user'] = user
    users = Users.objects.create(**users_dict)

    
    # пытаеися создать такого опльзователя на стороннем сервисе
    user_teachbase = Course().create_user(users)
    if (type(user_teachbase) == type({})) and (user_teachbase.get('error')):
        # если на удалённом сервере не удалось создать юзера, то удаляем у себя
        user.delete()

        return user_teachbase
    
    # указываем id юзера со стороннего сервиса
    users.user_id_teachbase = user_teachbase[0].get('id')
    users.save(update_fields=["user_id_teachbase"])

    # входим как новый юзер
    user_login = authenticate(username=user.username, password=users_dict.get('password'))
    if user_login is not None:
        login(request, user_login)

    return {}

