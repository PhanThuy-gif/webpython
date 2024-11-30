from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']  # Chỉ cho phép nhập nội dung bình luận
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Viết bình luận của bạn...'
            }),
        }
        labels = {
            'content': '',  # Ẩn nhãn "content"
        }