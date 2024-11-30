from django.shortcuts import render,get_object_or_404, redirect
from comment.models import Post
from comment.models import Comment
from comment.forms import CommentForm
from django.contrib.auth.decorators import login_required
from urllib.parse import unquote

def article_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # Lấy bài viết theo ID
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)  # Tạo comment nhưng chưa lưu vào DB
            comment.post = post  # Gán bài viết
            comment.user = request.user  # Gán người dùng
            comment.save()  # Lưu vào DB
            return redirect('article_detail', post_id=post.id)  # Redirect đến trang chi tiết bài viết
    else:
        form = CommentForm()  # Hiển thị form trống nếu không phải POST
    return render(request, 'article_detail.html', {'form': form, 'post': post})