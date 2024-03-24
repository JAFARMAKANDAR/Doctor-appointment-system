# In forms.py

from django import forms
from .models import HealthHistory

class HealthHistoryForm(forms.ModelForm):
    class Meta:
        model = HealthHistory
        fields = ['medical_history', 'family_medical_history', 'social_history']
