from django.shortcuts import render,get_object_or_404, redirect
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from comment.models import Article,Comment
from django.http import HttpResponseRedirect

def post_detail(request,pk):
    post = get_object_or_404(Article, pk=pk)
    form = CommentForm()
    if request.method == 'ARTICLE':
        form = CommentForm(request.ARTICLE,author=request.user,post=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(request.path)
    return render(request, "article_detail.html", {"post":post, "form":form})

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_url = comment.post.url
    comment.delete()
    return redirect('post_detail', post_url=post_url)

