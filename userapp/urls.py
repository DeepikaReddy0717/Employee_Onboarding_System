
from . import views
from django.conf.urls.static import static  # Make sure this is correct
from django.conf import settings
from django.urls import path, include
app_name = 'userapp'

urlpatterns = [
    path('UserHomePage/', views.UserHomePage, name='UserHomePage'),
    path('module/<int:module_id>/', views.module_details, name='module_details'),
    path('start_training/<int:module_id>/', views.start_training, name='start_training'),
    path('dashboard/', views.user_dashboard, name='employee_dashboard'),
    path('profile/', views.user_profile, name='employee_profile'),
    path('viewmarks/',views.view_mark,name='view_marks'),
    path('my-progress-certificates/', views.my_progress_and_certificates, name='my_progress_and_certificates'),
    path('assessment_descriptions/',views.assessment_descriptions,name='assessment_descriptions'),
    path('registered_meetings/', views.registered_meetings, name='registered_meetings'),
    path('feedback/', views.give_feedback, name='give_feedback'),
    path('session-list/', views.session_list, name='session_list'),
 path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('start_training/<int:module_id>/', views.start_training, name='start_training'),
path('assigned_courses/', views.user_assigned_courses, name='assigned_courses'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)