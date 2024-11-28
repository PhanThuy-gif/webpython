from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    
    def __init__(self,*args, **kwargs):
        self.author = kwargs.pop('user',None)
        self.post = kwargs.pop('article',None)
        super().__init__(*args,**kwargs)
    def save(self,commit = True):
        comment = super().save(commit=False)
        comment.user = self.user
        comment.article = self.article
        comment.save()
        
    class Meta:
        model = Comment
        fields = ["body"]