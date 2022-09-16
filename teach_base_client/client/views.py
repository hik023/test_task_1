from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .utils.helpers import (
    get_or_update_token, 
    get_courses,
    get_course_detail,
    get_expiration_of_token,
    get_course_sessions,
    session_register,
    update_local_courses,
)
from .utils.exceptions import BadAPIAccess


def main_page(request):
    if request.user.is_authenticated:
        try:
            data = {'token_expiration': get_expiration_of_token(request.user)}
        except BadAPIAccess as e:
            return render(request, 'error_page.html', {'error': e.message})
        return render(request, 'client/home_page.html', context=data)
    else: 
        return redirect('login')


@login_required
def course_list(request):
    data = {}
    try:
        token = get_or_update_token(request.user)
        courses = get_courses(token)
        update_local_courses(courses)
    except BadAPIAccess as e:
            return render(request, 'error_page.html', {'error': e.message})
    data['courses_count'] = list(range(1, len(courses)))
    data['first_course'] = courses.pop(0)
    data['courses'] = courses
    return render(request, 'client/course_list.html', context=data)


@login_required
def course_detail(request, course_id):
    try:
        token = get_or_update_token(request.user)
        course_data = get_course_detail(token, course_id)
        data = {'course': course_data}
        course_sessions = get_course_sessions(token, course_id)
    except BadAPIAccess as e:
            return render(request, 'error_page.html', {'error': e.message})
    data['course_sessions'] = course_sessions
    return render(request, 'client/course_detail.html', context=data)


@login_required
def session_register_view(request, session_id):
    try:
        token = get_or_update_token(request.user)
        response = session_register(token, session_id, request.user)
    except BadAPIAccess as e:
            return render(request, 'error_page.html', {'error': e.message})

    return render(request, 'client/session_response.html', context={'response': response})
