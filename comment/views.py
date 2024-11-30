from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment  # Đảm bảo bạn có import các model
from .forms import CommentForm
from django.contrib.auth.decorators import login_required

def article_detail(request, article_id):
    article = get_object_or_404(Post, id=article_id)  # Lấy bài viết theo ID
    comments = article.comments.all()  # Lấy danh sách bình luận của bài viết
    form = CommentForm()

    # Xử lý khi người dùng gửi bình luận
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = article
            comment.user = request.user  # Gán người dùng hiện tại
            comment.save()
            return redirect('article_detail', article_id=article.id)

    return render(request, 'article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })
