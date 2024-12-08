from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def UserHomePage(request):
    return render(request,  'userapp/UserHomePage.html')
def module_details(request, module_id):
    return render(request, 'userapp/module_details.html', {'module_id': module_id})
def start_training(request, module_id):
    return render(request, 'userapp/start_training.html', {'module_id': module_id})
from django.shortcuts import render, redirect, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm
@login_required
def user_profile(request):
    try:
        employee_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        employee_profile = None
        if request.method == 'POST':
            form = UserProfileForm(request.POST, request.FILES, instance=employee_profile)
        else:
            form = UserProfileForm(request.POST, request.FILES)

        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('userapp:employee_dashboard')
    else:
        form = UserProfileForm(instance=employee_profile)

    return render(request, 'userapp/profile.html', {'form': form})

def user_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        employee_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        return redirect('userapp:employee_profile')  # Redirect to profile creation if not found

    context = {
        'employee_profile': employee_profile,
    }
    return render(request, 'userapp/dashboard.html', context)

# In your view function to display marks
from adminapp.models import Marks

def view_mark(request):
    user = request.user
    marks = Marks.objects.filter(student=user).select_related('course')
    return render(request, 'userapp/view_marks.html', {'marks': marks})


from django.shortcuts import render
from adminapp.models import Progress, Certificate


def my_progress_and_certificates(request):
    # Get the logged-in user
    user = request.user

    # Retrieve the progress records for this user
    progress_records = Progress.objects.filter(user=user)

    # Retrieve the certificates for this user
    certificates = Certificate.objects.filter(user=user)

    context = {
        'progress_records': progress_records,
        'certificates': certificates,
    }
    return render(request, 'userapp/my_progress_and_certificates.html', context)
from django.shortcuts import render
from adminapp.models import Assessment

def assessment_descriptions(request):
    # Retrieve all assessments along with the course title and description
    assessments = Assessment.objects.select_related('cou'
                                                    'rse').values('description', 'course__title')
    return render(request, 'userapp/assessment_descriptions.html', {'assessments': assessments})
from trainerapp.models import Meeting
@login_required
def registered_meetings(request):
    # Get the meetings where the logged-in user is a participant or the trainer
    meetings = Meeting.objects.filter(participants=request.user) | Meeting.objects.filter(trainer=request.user)

    return render(request, 'userapp/registered_meetings.html', {
        'meetings': meetings,
    })
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import FeedbackForm
from django.contrib import messages

@login_required
def give_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('userapp:UserHomePage')  # Redirect to the home page or a relevant page
    else:
        form = FeedbackForm()
    return render(request, 'userapp/feedback_form.html', {'form': form})
from django.shortcuts import render
from trainerapp.models import TrainingSession

def session_list(request):
    sessions = TrainingSession.objects.all()
    return render(request, 'userapp/session_list.html', {'sessions': sessions})


# user/views.py
from django.shortcuts import render, redirect, get_object_or_404
from adminapp.models import Module
from .models import UserModuleProgress
from django.utils.timezone import now

def module_list(request, course_id):
    modules = Module.objects.filter(course_id=course_id)
    user_progress = UserModuleProgress.objects.filter(user=request.user)
    completed_modules = user_progress.filter(is_completed=True).values_list('module_id', flat=True)

    return render(request, 'user/module_list.html', {
        'modules': modules,
        'completed_modules': completed_modules,
    })

def mark_module_complete(request, module_id):
    module = get_object_or_404(Module, id=module_id)
    progress, created = UserModuleProgress.objects.get_or_create(user=request.user, module=module)
    progress.is_completed = True
    progress.completed_at = now()
    progress.save()
    return redirect('user:module_list', course_id=module.course.id)
# In your views.py (user views)
from django.shortcuts import render
from trainerapp.models import Module

def user_dashboard(request):
    modules = Module.objects.all()
    return render(request, 'userapp/user_dashboard.html', {'modules': modules})

def start_training(request, module_id):
    module = Module.objects.get(id=module_id)
    return render(request, 'userapp/start_training.html', {'module': module})
# userapp/views.py
from django.shortcuts import render
from adminapp.models import UserCourse

def user_assigned_courses(request):
    # Fetch all assigned courses for the logged-in user
    assigned_courses = UserCourse.objects.filter(user=request.user)

    return render(request, 'userapp/assigned_courses.html', {
        'assigned_courses': assigned_courses,
    })
