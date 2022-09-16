from django.conf import settings 
from django.utils import timezone
from django.contrib.auth.models import User

import requests
from datetime import datetime, timedelta

from authorization.models import UserAPISession
from .exceptions import BadAPIAccess
from client.models import Course, CourseSection, CourseSectionMaterial


# Constants

EXPIRATION_TIMEOUT = timedelta(seconds=60)
COURSE_LIGHT_KEYS = ('id', 'name', 'description', 'bg_url')


def get_api_token():
    '''
    Send request to TeachBase auth API and returns tuple of access token and expiration time.
    '''
    body = {
        'client_id': '8bdf8070ca5eb1ee7565aa4722e9772a60612310f62f0a04ba4774e7527c836b',
        'client_secret': 'c2c76197cc8de37d0d04a9cc4127ef7bb5c0961d4f96eeec6fff403e30b304dd',
        'grant_type': 'client_credentials'
    }
    response = requests.post(settings.TB_AUTH_URL, data=body)
    if response.status_code == 200:
        r_data = response.json()
        token, expire_time = r_data['access_token'], int(r_data['expires_in'])
        return token, expire_time
    else:
        raise BadAPIAccess(response.status_code, settings.TB_AUTH_URL, response.content)

def create_user_api_session(user: User):
    '''
    Create record in db with token and expiration time assigned to User.
    '''
    token, expiration_time = get_api_token()
    user_api_session = UserAPISession.objects.create(
        user=user,
        expired_at=datetime.now() + timedelta(seconds=expiration_time),
        token=token
    )
    return user_api_session


def get_or_update_token(user: User):
    '''
    Take token from db, if expires request new from TeachBase API.
    '''
    user_api_session = UserAPISession.objects.filter(user=user.id).first()
    if user_api_session.expired_at.replace(tzinfo=None) - datetime.now() < EXPIRATION_TIMEOUT:
        token, expiration_time = get_api_token()
        user_api_session.token = token
        user_api_session.expired_at = datetime.now() + timedelta(seconds=expiration_time)
        user_api_session.save()
    
    return user_api_session.token


def get_expiration_of_token(user: User):
    '''
    Get expiration time of token by User localized by TZ.
    '''
    user_api_session = UserAPISession.objects.filter(user=user.id).first()
    return timezone.localtime(user_api_session.expired_at).strftime("%m/%d/%Y, %H:%M:%S")


def get_headers(token: str):
    '''
    Returns Auth header with access token.
    '''
    return {
        'Authorization': f'Bearer {token}'
    }


def update_local_courses(courses_api: list):
    '''
    Update local data with new courses from TeachBase API.
    '''
    local_courses = Course.objects.all().values_list('third_party_id', flat=True)
    for c in courses_api:
        if c['id'] not in local_courses:
            Course.objects.create(
                name=c['name'],
                description=c['description'],
                img_url=c['bg_url'],
                third_party_id=c['id']
            )


def get_courses(token: str):
    '''
    Get list of courses from TeachBase API.
    '''
    response = requests.get(f'{settings.TB_API_DOMAIN}courses', headers=get_headers(token))
    if response.status_code == 200:
        r_data = response.json()
        courses = []
        for c in r_data:
            course = {}
            for key in COURSE_LIGHT_KEYS:
                course[key] = c[key]
            courses.append(course) 

        return courses
    else:
        raise BadAPIAccess(response.status_code, f'{settings.TB_API_DOMAIN}courses', response.content)


def update_local_course_detail(course_api: dict):
    '''
    Update local data with new courses from TeachBase API.
    '''
    local_course = Course.objects.filter(third_party_id=course_api['id']).first()
    local_course_sections = CourseSection.objects.all().values_list('third_party_id', flat=True)
    for cs in course_api['sections']:
        if cs['id'] not in local_course_sections:
            new_course_section = CourseSection.objects.create(
                name=cs['name'],
                third_party_id=cs['id'],
                course=local_course
            )
            for csm in cs['materials']:
                CourseSectionMaterial.objects.create(
                    name=csm['name'],
                    description=csm['description'],
                    third_party_id=csm['id'],
                    course_section=new_course_section
            )


def get_course_detail(token: str, course_id: int):
    '''
    Get detail info about course from TeachBase API.
    '''
    response = requests.get(f'{settings.TB_API_DOMAIN}courses/{course_id}', headers=get_headers(token))
    if response.status_code == 200:
        update_local_course_detail(response.json())
        return response.json()
    else:
        raise BadAPIAccess(response.status_code, f'{settings.TB_API_DOMAIN}courses/{course_id}', response.content)


def get_course_sessions(token:str, course_id: int):
    '''
    Get sessions info assigned to course with <course_id> from TeachBase API.
    '''
    response = requests.get(f'{settings.TB_API_DOMAIN}courses/{course_id}/course_sessions', headers=get_headers(token))
    if response.status_code == 200:
        return response.json()
    else:
        raise BadAPIAccess(response.status_code, f'{settings.TB_API_DOMAIN}courses/{course_id}/course_sessions', response.content)


def session_register(token:str, session_id, user):
    '''
    Register User on session via TeachBase API.
    '''
    data = {
        "email": user.email
    }
    response = requests.post(f'{settings.TB_API_DOMAIN}course_sessions/{session_id}/register', data, headers=get_headers(token))
    if response.status_code == 200:
        return response.json()
    else:
        raise BadAPIAccess(response.status_code, f'{settings.TB_API_DOMAIN}course_sessions/{session_id}/register', response.content)
