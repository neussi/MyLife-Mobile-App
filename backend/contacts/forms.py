from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'first_name', 'last_name', 'phone_number', 'email', 
            'address', 'company', 'relationship_type', 'birthday', 
            'notes', 'avatar'
        ]
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'resize-none'}),
        }
