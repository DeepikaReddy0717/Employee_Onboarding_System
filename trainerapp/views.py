from sqlite3 import OperationalError
from adminapp.models import User
from adminapp.forms import CertificateForm
from django.conf import settings
from adminapp.models import Course

def TrainerHomePage(request):
    courses = Course.objects.filter(created_by=request.user)
    modules = Module.objects.all()
    return render(request, 'trainerapp/TrainerHomePage.html', {'courses': courses, 'modules': modules})
from django.http import JsonResponse, HttpResponse
from django.http import JsonResponse
from .models import FAQ
import json
from django.shortcuts import render

def chatbot(request):
    """
    View to render the chatbot page with Botpress webchat integration.
    """
    return render(request, 'trainerapp/chatbot.html')

from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
def custom_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            if hasattr(user, 'trainerprofile'):
                return redirect('trainerapp:trainer_dashboard')
            else:
                return redirect('trainerapp:trainer_profile')
    else:
        form = AuthenticationForm()
    return render(request, 'trainerapp/login.html', {'form': form})
from .forms import TrainerProfileForm
def trainer_profile(request):
    try:
        trainer_profile = TrainerProfile.objects.get(user=request.user)
    except TrainerProfile.DoesNotExist:
        trainer_profile = None
    if request.method == 'POST':
        if trainer_profile:
            form = TrainerProfileForm(request.POST, request.FILES, instance=trainer_profile)
        else:
            form = TrainerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('trainerapp:trainer_dashboard')  # Redirect after saving
    else:
        form = TrainerProfileForm(instance=trainer_profile)
    return render(request, 'trainerapp/profile.html', {'form': form})
from django.shortcuts import render, redirect, get_object_or_404
from .models import TrainerProfile
def trainer_dashboard(request):
    if not request.user.is_authenticated:
        return redirect('login')
    try:
        trainer_profile = TrainerProfile.objects.get(user=request.user)
    except TrainerProfile.DoesNotExist:
        return redirect('trainerapp:trainer_profile')
    context = {
        'trainer_profile': trainer_profile,
    }
    return render(request, 'trainerapp/dashboard.html', context)
def user_list(request):
    users = User.objects.all()
    user_data = []
    for user in users:
        roles = ', '.join([group.name for group in user.groups.all()])
        user_data.append({
            'user': user,
            'is_admin': user.is_staff,
            'roles': roles
        })
    return render(request, 'trainerapp/user_list.html', {'user_data': user_data})
def add_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        roles = request.POST.getlist('roles')
        for role in roles:
            group, created = Group.objects.get_or_create(name=role)
            user.groups.add(group)
        messages.success(request, "User added successfully!")
        return redirect('trainerapp:user_list')
    return render(request, 'trainerapp/add_user.html')
from django.contrib.auth.models import User, Group
from adminapp.forms import UserForm, ModuleForm, QuestionForm
def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = 'is_staff' in request.POST
            user.save()
            user.groups.clear()
            roles = request.POST.getlist('role')
            for role in roles:
                try:
                    group = Group.objects.get(name=role)
                    group.user_set.add(user)
                except Group.DoesNotExist:
                    messages.error(request, f"Group '{role}' does not exist. Please check the role name.")
            messages.success(request, "User updated successfully.")
            return redirect('trainerapp:user_list')
    else:
        form = UserForm(instance=user)
    user_roles = user.groups.values_list('name', flat=True)
    return render(request, 'trainerapp/edit_user.html', {
        'form': form,
        'user': user,
        'user_roles': user_roles
    })
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                user.delete()
            messages.success(request, "User deleted successfully.")
            return redirect('adminapp:user_list')
        except OperationalError:
            messages.error(request, "Error deleting user. Please try again later.")
    return render(request, 'trainerapp/delete_user.html', {'user': user})
from adminapp.models import Course
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'trainerapp/course_list.html', {'courses': courses})

from adminapp.models import Course, UserCourse
def assign_course(request):
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        user = User.objects.get(id=user_id)
        course = Course.objects.get(id=course_id)
        UserCourse.objects.get_or_create(user=user, course=course)
        messages.success(request, f'Successfully assigned {course.title} to {user.username}.')
        return redirect('trainerapp:assign_course')
    users = User.objects.all()
    courses = Course.objects.filter(is_active=True)
    users_with_courses = User.objects.prefetch_related('usercourse_set').all()
    return render(request, 'trainerapp/assign_courses.html', {
        'users': users,
        'courses': courses,
        'users_with_courses': users_with_courses,
    })
from django.shortcuts import render, redirect
from django.contrib import messages
from adminapp.forms import CourseForm, ResourceFormSet
from adminapp.models import Course, Resource

def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        formset = ResourceFormSet(request.POST, request.FILES)
        if form.is_valid() and formset.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()

            # Save the resources
            resources = formset.save(commit=False)
            for resource in resources:
                resource.course = course
                resource.save()

            messages.success(request, "Course and resources added successfully!")
            return redirect('adminapp:course_list')
    else:
        form = CourseForm()
        formset = ResourceFormSet(queryset=Resource.objects.none())  # Empty formset

    return render(request, 'adminapp/course_form.html', {'form': form, 'formset': formset})
from django.http import JsonResponse
from adminapp.models import Course

def get_course_resources(request, course_id):
    try:
        course = Course.objects.get(id=course_id)
        resources = course.resources.all()
        resources_data = [{'name': resource.name, 'url': resource.file.url} for resource in resources]

        return JsonResponse({'resources': resources_data})
    except Course.DoesNotExist:
        return JsonResponse({'error': 'Course not found'}, status=404)

def edit_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        formset = ResourceFormSet(request.POST, request.FILES, instance=course)
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            messages.success(request, "Course and resources updated successfully!")
            return redirect('adminapp:course_list')
    else:
        form = CourseForm(instance=course)
        formset = ResourceFormSet(instance=course)
    return render(request, 'adminapp/course_form.html', {'form': form, 'formset': formset, 'course': course})

from django.db import transaction, OperationalError
def delete_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        try:
            with transaction.atomic():
                course.delete()
            messages.success(request, "Course deleted successfully.")
            return redirect('adminapp:course_list')
        except OperationalError:
            messages.error(request, "Error deleting course. Please try again later.")
    return render(request, 'adminapp/delete_course.html', {'course': course})
from django.contrib.auth.decorators import login_required
@login_required
def add_assessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.created_by = request.user
            assessment.save()
            messages.success(request, "Assessment added successfully!")
            return redirect('trainerapp:assessment_list')
        else:
            messages.error(request, "There was an error with your submission.")
    else:
        form = AssessmentForm()
    return render(request, 'trainerapp/assessment_form.html', {'form': form})
from adminapp.forms import AssessmentForm
def edit_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    if request.method == 'POST':
        form = AssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            updated_assessment = form.save(commit=False)
            updated_assessment.created_by = request.user
            updated_assessment.save()
            messages.success(request, "Assessment updated successfully.")
            return redirect('trainerapp:dashboard')
        else:
            messages.error(request, "There was an error updating the assessment.")
            print(form.errors)
    else:
        form = AssessmentForm(instance=assessment)
    return render(request, 'trainerapp/assessment_form.html', {
        'form': form,
        'assessment': assessment
    })
def delete_assessment(request, assessment_id):
    assessment = get_object_or_404(Assessment, id=assessment_id)
    if request.method == 'POST':
        try:
            assessment.delete()
            messages.success(request, "Assessment deleted successfully.")
            return redirect('trainerapp:assignment_dashboard')
        except OperationalError:
            messages.error(request, "Error deleting assessment. Please try again later.")
    return render(request, 'trainerapp/delete_assessment.html', {'assessment': assessment})
def view_results(request):
    results = EmployeeResult.objects.all()
    return render(request, 'trainerapp/view_results.html', {'results': results})
from adminapp.models import Assessment
def assignment_dashboard(request):
    assessments = Assessment.objects.all()
    return render(request, 'trainerapp/assignment_dashboard.html', {'assessments': assessments})
def assessment_list(request):
    assessments = Assessment.objects.all()
    return render(request, 'trainerapp/assessment_list.html', {'assessments': assessments})
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from adminapp.models import Course, Marks
from adminapp.forms import MarksForm
def post_marks(request):
    if request.method == "POST":
        form = MarksForm(request.POST)
        if form.is_valid():
            try:
                marks_instance = form.save()
                student = marks_instance.student
                user_email = student.email
                subject = 'Marks Entered'
                message = (f'Hello {student.username},\n\n'
                           f'Your marks for the course "{marks_instance.course.title}" have been recorded. '
                           f'Marks: {marks_instance.marks}')
                from_email = 'deepikareddymandapati@gmail.com'
                recipient_list = [user_email]
                send_mail(subject, message, from_email, recipient_list)
                messages.success(request,
                                 f'Marks for {student.username} in {marks_instance.course.title} have been successfully entered.')
                return redirect('trainerapp:post_marks')
            except Exception as e:
                messages.error(request, f"An error occurred while saving marks: {str(e)}")
    else:
        form = MarksForm()
    users = User.objects.all()
    courses = Course.objects.filter(is_active=True)
    marks_list = Marks.objects.select_related('student', 'course').all()
    return render(request, 'trainerapp/post_marks.html', {
        'form': form,
        'users': users,
        'courses': courses,
        'marks_list': marks_list,
    })
from django.shortcuts import get_object_or_404
def edit_marks(request, mark_id):
    mark_instance = get_object_or_404(Marks, id=mark_id)
    if request.method == "POST":
        form = MarksForm(request.POST, instance=mark_instance)
        if form.is_valid():
            form.save()
            messages.success(request, f"Marks for {mark_instance.student.username} in {mark_instance.course.title} have been successfully updated.")
            return redirect('trainerapp:post_marks')
    else:
        form = MarksForm(instance=mark_instance)
    return render(request, 'trainerapp/edit_marks.html', {
        'form': form,
        'mark_instance': mark_instance,
    })
def delete_marks(request, mark_id):
    mark_instance = get_object_or_404(Marks, id=mark_id)
    if request.method == "POST":
        mark_instance.delete()
        messages.success(request, f"Marks for {mark_instance.student.username} in {mark_instance.course.title} have been successfully deleted.")
        return redirect('trainerapp:post_marks')
    return render(request, 'trainerapp/delete_marks.html', {
        'mark_instance': mark_instance,
    })
from adminapp.models import Progress, Course
from django.contrib.auth.models import User
def track_progress(request):
    users = User.objects.all()
    courses = Course.objects.all()
    if request.method == 'POST':
        user_id = request.POST.get('user')
        course_id = request.POST.get('course')
        progress_percentage = request.POST.get('progress_percentage')
        completion_date = request.POST.get('completion_date')
        progress = Progress(
            user_id=user_id,
            course_id=course_id,
            progress_percentage=progress_percentage,
            completion_date=completion_date
        )
        progress.save()
        return redirect('trainerapp:track_progress')
    progress_reports = Progress.objects.all()
    context = {
        'users': users,
        'courses': courses,
        'progress_reports': progress_reports,
    }
    return render(request, 'trainerapp/track_progress.html', context)
def edit_progress(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    users = User.objects.all()
    courses = Course.objects.all()
    if request.method == 'POST':
        progress.user_id = request.POST.get('user')
        progress.course_id = request.POST.get('course')
        progress.progress_percentage = request.POST.get('progress_percentage')
        progress.completion_date = request.POST.get('completion_date')
        progress.save()
        return redirect('trainerapp:track_progress')
    context = {
        'progress': progress,
        'users': users,
        'courses': courses,
    }
    return render(request, 'trainerapp/edit_progress.html', context)
def delete_progress(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    if request.method == 'POST':
        progress.delete()
        return redirect('trainerapp:track_progress')
    context = {
        'progress': progress,
    }
    return render(request, 'trainerapp/delete_progress.html', context)
def issue_certificate(request):
    if request.method == "POST":
        form = CertificateForm(request.POST)
        if form.is_valid():
            certificate = form.save()
            return redirect('trainerapp:generate_certificate', progress_id=certificate.progress.id)
    else:
        form = CertificateForm()
    return render(request, 'trainerapp/issue_certificate.html', {'form': form})
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from adminapp.models import Progress
def generate_certificate(request, progress_id):
    progress = get_object_or_404(Progress, id=progress_id)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="certificate_{progress.user.username}_{progress.course.title}.pdf"'
    doc = SimpleDocTemplate(response, pagesize=letter)
    content = []
    logo = Image('media/logo/img.png', width=2 * inch, height=1 * inch)
    logo.hAlign = 'CENTER'
    content.append(logo)
    content.append(Spacer(1, 0.5 * inch))
    styles = getSampleStyleSheet()
    title = Paragraph("Certificate of Completion", styles['Title'])
    content.append(title)
    content.append(Spacer(1, 0.5 * inch))
    certifying_statement = Paragraph("This certifies that", styles['Normal'])
    content.append(certifying_statement)
    content.append(Spacer(1, 0.2 * inch))
    user_name = Paragraph(f"<b>{progress.user.username}</b>", styles['Heading1'])
    content.append(user_name)
    content.append(Spacer(1, 0.5 * inch))
    course_completion = Paragraph("has completed the course", styles['Normal'])
    content.append(course_completion)
    content.append(Spacer(1, 0.2 * inch))
    course_title = Paragraph(f"<b>{progress.course.title}</b>", styles['Heading1'])
    content.append(course_title)
    content.append(Spacer(1, 0.5 * inch))
    progress_statement = Paragraph(f"with a progress of <b>{progress.progress_percentage} %</b>.", styles['Normal'])
    content.append(progress_statement)
    content.append(Spacer(1, 0.5 * inch))
    issued_date = Paragraph(f"Issued on: {progress.completion_date.strftime('%B %d, %Y')}", styles['Normal'])
    content.append(issued_date)
    p = canvas.Canvas(response, pagesize=letter)
    p.setStrokeColor(colors.black)
    p.setLineWidth(5)
    p.rect(30, 30, 550, 730, fill=0)
    p.save()
    doc.build(content)
    return response

from django.shortcuts import render, get_object_or_404
from .models import Meeting

from django.shortcuts import render, redirect
from .models import User
from .forms import MeetingForm

def create_meeting(request):
    # Create or process the meeting form
    form = MeetingForm(request.POST or None)

    participants = User.objects.all()
    if form.is_valid():
        meeting = form.save()  # Save the meeting to the database
        selected_participants = form.cleaned_data.get('participants')
        # Prepare the email content
        subject = f"New Meeting: {meeting.title}"
        message = (
            f"Hello,\n\n"
            f"You have been registered for the meeting: {meeting.title}\n"
            f"Description: {meeting.description}\n"
            f"Start Time: {meeting.start_time}\n"
            f"End Time: {meeting.end_time}\n\n"
            f"Please make sure to join the meeting on time.\n\n"
            f"Best regards,\nThe Training Team"
        )

        # Send the email to all participants
        for participant in selected_participants:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,  # Sender email
                [participant.email],  # Recipient email
                fail_silently=False,
            )

        # Redirect to the meeting list page
        return redirect('trainerapp:meeting_list')

    # Render the form with the participants list
    return render(request, 'trainerapp/create_meeting.html', {
        'form': form,
        'participants': participants,  # Pass participants to the template
    })
def edit_meeting(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    if request.method == 'POST':
        form = MeetingForm(request.POST, instance=meeting)
        if form.is_valid():
            form.save()
            return redirect('trainerapp:meeting_list')
    else:
        form = MeetingForm(instance=meeting)
    return render(request, 'trainerapp/edit_meeting.html', {'form': form})

def delete_meeting(request, id):
    meeting = get_object_or_404(Meeting, id=id)
    if request.method == 'POST':
        meeting.delete()
        return redirect('trainerapp:meeting_list')
    return render(request, 'trainerapp/delete_meeting.html', {'meeting': meeting})

# View for listing all meetings
from django.core.paginator import Paginator

def meeting_list(request):
    meeting_list = Meeting.objects.all()
    paginator = Paginator(meeting_list, 10)  # Show 10 meetings per page
    page_number = request.GET.get('page')
    meetings = paginator.get_page(page_number)
    return render(request, 'trainerapp/meeting_list.html', {'meetings': meetings})
from django.shortcuts import render
from .models import Meeting


def meeting_details(request):
    # Retrieve the meeting by id
    meeting = Meeting.objects.all()

    # Pass the meeting to the template
    return render(request, 'trainerapp/meeting_detail.html', {
        'meeting': meeting,
    })

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TrainingSessionForm
@login_required
def upload_session(request):

    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, request.FILES)
        if form.is_valid():
            session = form.save(commit=False)
            session.trainer = request.user
            session.save()
            return redirect('trainerapp:session_list')  # Redirect after successful upload
    else:
        form = TrainingSessionForm()

    return render(request, 'trainerapp/upload_session.html', {'form': form})
from django.shortcuts import render
from .models import TrainingSession

def session_list(request):
    sessions = TrainingSession.objects.filter(trainer=request.user)
    return render(request, 'trainerapp/session_list.html', {'sessions': sessions})


from django.shortcuts import get_object_or_404, redirect, render
from .forms import TrainingSessionForm
from .models import TrainingSession


def edit_session(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id, trainer=request.user)

    if request.method == 'POST':
        form = TrainingSessionForm(request.POST, request.FILES, instance=session)
        if form.is_valid():
            form.save()  # Save the changes to the session
            return redirect('trainerapp:session_list')  # Redirect to the session list after updating
    else:
        form = TrainingSessionForm(instance=session)

    return render(request, 'trainerapp/edit_session.html', {'form': form})
from django.shortcuts import get_object_or_404, redirect
from .models import TrainingSession

def delete_session(request, session_id):
    session = get_object_or_404(TrainingSession, id=session_id, trainer=request.user)
    session.delete()  # Delete the session
    return redirect('trainerapp:session_list')  # Redirect to the session list after deletion


# In your views.py (trainer views)
from django.shortcuts import render
from adminapp.models import Course
from trainerapp.models import Module

def trainer_dashboard(request):
    courses = Course.objects.all()
    modules = Module.objects.all()  # Or filter by course
    return render(request, 'trainerapp/trainer_dashboard.html', {'courses': courses, 'modules': modules})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from adminapp.models import Module, Progress, Certificate, Course


# View for trainer to upload modules
@login_required
def upload_module(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        duration = request.POST.get('duration')
        Module.objects.create(course=course, title=title, content=content, duration=duration)
        return redirect('course_detail', course_id=course.id)
    return render(request, 'upload_module.html', {'course': course})


# View for user to retrieve modules and mark as complete
@login_required
def course_modules(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    modules = Module.objects.filter(course=course)
    progress, created = Progress.objects.get_or_create(user=request.user, course=course)

    if request.method == 'POST':
        module_id = request.POST.get('module_id')
        module = get_object_or_404(Module, id=module_id)
        completed_modules = Progress.objects.filter(user=request.user, course=course).count()
        total_modules = modules.count()

        # Update progress
        progress.progress_percentage = (completed_modules / total_modules) * 100
        progress.save()

        # Issue certificate if progress is 100%
        if progress.progress_percentage == 100:
            Certificate.objects.get_or_create(user=request.user, course=course, progress=progress)

        return JsonResponse({'success': True, 'progress': progress.progress_percentage})

    return render(request, 'course_modules.html', {'course': course, 'modules': modules, 'progress': progress})
