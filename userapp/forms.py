# employeeapp/forms.py
from django import forms
from .models import UserProfile
from .models import Feedback
from adminapp.models import User
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['employee_name', 'department', 'position', 'contact_number', 'email', 'biography', 'photo']
from django import forms
from .models import Feedback

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['trainer', 'comments', 'rating']
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'Write your feedback here...'}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
