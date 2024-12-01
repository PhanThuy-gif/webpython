from django.shortcuts import render, get_object_or_404, redirect
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from comment.models import Comment
from django.http import HttpResponseRedirect
from home.models import Article
@login_required
def post_detail(request, article_link):
    post = get_object_or_404(Article, link=article_link)  
    form = CommentForm()
    if request.method == 'POST':
        form= CommentForm(request.POST, author=request.user, post=post) 
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    return render(request, "article_detail.html", {"post": post,"form ":form})