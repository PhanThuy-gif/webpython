from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()  # Lấy tất cả bình luận liên quan đến bài báo

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.article = article
                comment.author = request.user
                comment.save()
                return redirect('article_detail', pk=pk)
        else:
            return redirect('login')  # Chuyển hướng đến trang đăng nhập nếu người dùng chưa đăng nhập
    else:
        form = CommentForm()
    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })

    
