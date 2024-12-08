from django import forms

class ChatbotForm(forms.Form):
    query = forms.CharField(label='Ask the chatbot', max_length=255)
# trainerapp/forms.py

from django import forms
from .models import TrainerProfile

class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['trainer_name', 'department', 'salary', 'contact_number', 'email', 'biography', 'photo']

from django import forms
from .models import Meeting, User
class MeetingForm(forms.ModelForm):
    participants = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  # Make it optional
    )
    class Meta:
        model = Meeting
        fields = ['title', 'description', 'start_time', 'end_time', 'trainer', 'participants']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
from django import forms
from .models import TrainingSession

class TrainingSessionForm(forms.ModelForm):
    class Meta:
        model = TrainingSession
        fields = ['title', 'description', 'date', 'start_time', 'end_time', 'resources']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }
