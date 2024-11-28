from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from .forms import CommentForm

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()  # Lấy tất cả bình luận liên quan đến bài viết
    form = CommentForm()

    if request.method == 'Article':
        form = CommentForm(request.Article)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.user = request.user  # Gắn bình luận với người dùng hiện tại
            comment.save()
            return redirect('article_detail', pk=article.pk)

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })
