from django.shortcuts import render, get_object_or_404, redirect
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from comment.models import Comment
from django.http import HttpResponseRedirect
from home.models import Article

def post_detail(request, article_link):
    post = get_object_or_404(Article, link=article_link)  
    comments = CommentForm()
    if request.method == 'POST':
        comments= CommentForm(request.POST, author=request.user, post=post) 
        if comments.is_valid():
            comments.save()
            return HttpResponseRedirect(request.path)
    return render(request, "article_detail.html", {"post": post, "comments": comments})
 