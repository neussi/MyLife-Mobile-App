from django import forms
from .models import Habit, MoodEntry

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'icon', 'color', 'frequency']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Ex: Méditation, Sport, Lecture...'
            }),
            'icon': forms.TextInput(attrs={
                'class': 'field',
                'placeholder': 'Nom de l\'icône Lucide (ex: activity, heart, book)'
            }),
            'color': forms.TextInput(attrs={
                'class': 'field h-[46px] p-1 cursor-pointer',
                'type': 'color'
            }),
            'frequency': forms.Select(attrs={
                'class': 'field'
            }),
        }

class MoodForm(forms.ModelForm):
    class Meta:
        model = MoodEntry
        fields = ['score', 'note']
        widgets = {
            'score': forms.HiddenInput(),  # Will be handled by custom premium selector in template
            'note': forms.Textarea(attrs={
                'class': 'field',
                'rows': 3,
                'placeholder': 'Un petit mot sur votre journée...'
            }),
        }
