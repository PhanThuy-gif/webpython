from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from .forms import CommentForm
def article_detail(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    comments = article.comments.all() #lấy all bình luận của bài viết
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.save()
            return redirect('article_detail', article_id=article.id)
    else:
        form = CommentForm()

    return render(request, 'article_detail.html', {'article': article, 'comments': comments, 'form': form})