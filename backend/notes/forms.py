from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'content', 'category', 'tags', 'color', 'is_pinned', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'class': 'resize-none', 'placeholder': 'Commencez à écrire votre note...'}),
            'color': forms.TextInput(attrs={'type': 'color'}),
            'tags': forms.TextInput(attrs={'placeholder': 'tag1, tag2, tag3'}),
        }
