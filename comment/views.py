from django.shortcuts import render, get_object_or_404, redirect
from .models import Article, Comment
from .forms import CommentForm

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comments = article.comments.all()  # Lấy tất cả bình luận liên quan đến bài viết
    form = CommentForm()

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid(): #Kiểm tra form có hợp lệ không
            comment = form.save(commit=False)
            comment.article = article # gắn bài viết vào bình luận
            comment.user = request.user  # Gắn bình luận với người dùng hiện tại
            comment.save()
            return redirect('article_detail', pk=article.pk)
        else:
            print(form.errors) #in ra lỗi form

    return render(request, 'comment/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form,
    })
