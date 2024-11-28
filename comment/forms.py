from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Viết bình luận...',
                'rows': 4,
                'class': 'form-control',
            }),
        }
