from django.urls import path
from client.views import main_page, course_list, course_detail, session_register_view

urlpatterns = [
     path('', main_page, name='home'),
     path('course_list', course_list, name='course_list'),
     path('course/<int:course_id>', course_detail, name='course_detail'),
     path('session_register/<int:session_id>', session_register_view, name='session_register'),

]
