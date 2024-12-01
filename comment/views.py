from django.shortcuts import render,get_object_or_404, redirect
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from comment.models import Article,Comment

def post_detail(request, post_url):
    post = get_object_or_404(Article, id=post_url)
    comments = post.comments.all()
    
    if request.method == 'ARTICLE':
        form = CommentForm(request.ARTICLE)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('arcicle_detail', post_url=post.id)
    else:
        form = CommentForm()

    return render(request, 'article_detail.html', {
        'post': post,
        'comments': comments,
        'form': form,
    })

def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    comment.delete()
    return redirect('article_detail', post_id=post_id)

